import os
from dotenv import load_dotenv

load_dotenv()

# --- Auth ---
HF_TOKEN = os.getenv("HF_TOKEN")

# --- Models ---
LLAMA_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
WHISPER_MODEL_SIZE = "small"  # base / small / medium

# --- Generation Params ---
MAX_NEW_TOKENS_GRAMMAR = 2500
MAX_NEW_TOKENS_ANALYSIS = 1200
TRANSLATION_INTERVAL_SEC = 1.5

# --- Prompts & Roles ---
ROLES = {
    "📊 Analyst": "You are a professional analyst. Extract core essence and key points. Use Markdown.",
    "⚔️ Critic": "You are a critical opponent. Find weak arguments, logical flaws and inconsistencies.",
    "📱 SMM Manager": "You are an SMM manager. Create an engaging Telegram post based on this content.",
    "📋 Secretary": "You are a secretary. Create a meeting protocol: who said what, what tasks were assigned.",
    "🧠 Psychologist": "You are a psychologist. Analyze the emotional tone, stress points and speaker's mental state.",
    "🎯 Coach": "You are a life coach. Extract actionable insights and next steps from this content.",
}