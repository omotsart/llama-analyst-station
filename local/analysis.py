import time
import torch
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from transformers import TextIteratorStreamer
from deep_translator import GoogleTranslator
import config
import models

_translator_executor = ThreadPoolExecutor(max_workers=1)

def _translate_async(text: str) -> str:
    try:
        return GoogleTranslator(source="en", target="ru").translate(text)
    except Exception:
        return text

def fix_grammar_llama(raw_text: str) -> str:
    if not raw_text.strip(): return "### ⚠️ No text to process."
    prompt = (
        "Fix grammar and punctuation only. Keep all details. "
        "Return only the corrected text:\n\n" + raw_text
    )
    messages = [{"role": "user", "content": prompt}]
    encoded = models.tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
    input_ids = encoded.to("cuda")
    
    with torch.no_grad():
        outputs = models.llm_model.generate(input_ids=input_ids, max_new_tokens=config.MAX_NEW_TOKENS_GRAMMAR)
    
    return models.tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)

def generate_analysis_stream(user_text: str, custom_query: str, target_lang: str, role: str):
    if not user_text.strip():
        yield "### ⚠️ No text found."
        return

    system_instr = config.ROLES.get(role, config.ROLES["📊 Analyst"])
    user_task = f"Provide analysis.\n\nTRANSCRIPT:\n{user_text}"
    
    if custom_query.strip():
        system_instr = "Answer the user's SPECIFIC QUESTION."
        user_task = f"Question: {custom_query}\n\nTranscript: {user_text}"

    messages = [{"role": "system", "content": system_instr}, {"role": "user", "content": user_task}]
    encoded = models.tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True)
    input_ids = encoded.to("cuda")

    streamer = TextIteratorStreamer(models.tokenizer, skip_prompt=True, skip_special_tokens=True)
    gen_kwargs = {"input_ids": input_ids, "streamer": streamer, "max_new_tokens": config.MAX_NEW_TOKENS_ANALYSIS, "temperature": 0.4, "do_sample": True}

    thread = Thread(target=models.llm_model.generate, kwargs=gen_kwargs)
    thread.start()

    full_en = ""
    tr_cache = ""
    last_tr_time = time.time()
    tr_future = None

    for new_chunk in streamer:
        full_en += new_chunk
        if target_lang == "en":
            yield full_en + " ▌"
            continue

        now = time.time()
        if (now - last_tr_time > config.TRANSLATION_INTERVAL_SEC) and (tr_future is None or tr_future.done()):
            tr_future = _translator_executor.submit(_translate_async, full_en)
            last_tr_time = now

        if tr_future and tr_future.done():
            tr_cache = tr_future.result()
        yield (tr_cache if tr_cache else full_en) + " ▌"
    
    yield _translate_async(full_en) if target_lang != "en" else full_en