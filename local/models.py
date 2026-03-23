import torch
import whisper
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from huggingface_hub import login
import config

def init_huggingface():
    if not config.HF_TOKEN:
        raise ValueError("❌ HF_TOKEN not found in .env file")
    login(config.HF_TOKEN)

def load_whisper_model():
    print(f"🔄 Loading Whisper '{config.WHISPER_MODEL_SIZE}'...")
    return whisper.load_model(config.WHISPER_MODEL_SIZE)

def load_llama_model():
    print(f"🔄 Loading {config.LLAMA_MODEL} (4-bit)...")
    
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(config.LLAMA_MODEL)
    tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        config.LLAMA_MODEL,
        device_map="auto",
        quantization_config=quant_config,
        torch_dtype=torch.float16,
        trust_remote_code=True,
    )
    return tokenizer, model

stt_model = None
tokenizer = None
llm_model = None



# Uncomment when pyannote is installed (Python 3.10/3.11)
# from pyannote.audio import Pipeline
# diarization_pipeline = None

def load_all():
    global stt_model, tokenizer, llm_model
    # global diarization_pipeline
    
    stt_model = load_whisper_model()
    tokenizer, llm_model = load_llama_model()
    
    # print("🔄 Loading Speaker Diarization...")
    # diarization_pipeline = Pipeline.from_pretrained(
    #     "pyannote/speaker-diarization-3.1",
    #     use_auth_token=config.HF_TOKEN
    # )
    # diarization_pipeline.to(torch.device("cuda"))
    # print("✅ Speaker Diarization loaded")