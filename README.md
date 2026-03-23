# 🎙️ Llama Analyst Station

![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg) ![LLM](https://img.shields.io/badge/Model-Llama--3.2--3B-orange.svg) ![Whisper](https://img.shields.io/badge/ASR-Whisper--Small-green.svg) ![Gradio](https://img.shields.io/badge/UI-Gradio-lightgrey.svg) ![License](https://img.shields.io/badge/license-MIT-blue.svg)

*Read this in other languages: [English](#english) | [Русский](#русский)*

---

<a id="english"></a>
## 🇬🇧 English

**Llama Analyst Station** is a professional, local-first AI workspace designed to transform raw audio and video recordings into highly structured, role-based analytical reports. By orchestrating SOTA models (OpenAI Whisper for ASR and Meta Llama 3.2 for NLP), it automates transcription, grammar correction, and deep semantic analysis.

This project demonstrates modular LLM engineering, efficient memory management (4-bit quantization), and advanced prompt architecture.

### ✨ Key Features
* **Multi-modal Input:** Process both audio (MP3, WAV) and video (MP4) seamlessly.
* **LLM-Powered Analysis:** Extract insights using 6 predefined prompt-engineered personas (e.g., *Data Analyst, SMM Manager, Psychologist, Critic*).
* **Speaker Diarization (Optional):** Built-in support for `pyannote.audio` to identify individual speakers in multi-speaker recordings (requires manual uncommenting for local setups).
* **Hardware Optimized:** Implements `BitsAndBytes` 4-bit quantization (NF4) to run heavy LLMs (3B+ parameters) on consumer GPUs (e.g., 16GB VRAM or T4).
* **Asynchronous Translation:** Real-time generation and translation stream using multi-threading to prevent UI freezing.
* **Google translation:** Translation of all types of analytics ENG/RU.
* **Rich Export Options:** Generate production-ready `.pdf`, `.docx`, `.txt`, and `.md` files.

<p align="center">
  <img src="Present.gif" width="800" alt="Llama Analyst Station Demo">
</p>

### 🏗️ Project Architecture

The repository is structured to support both local modular deployment and cloud-based execution (Kaggle).

```text
llama-analyst-station/
│
├── 📓 kaggle_notebook.ipynb     # Cloud execution (All-in-one for limited hardware)
│
├── 📁 local/                    # Modular production-ready codebase
│   ├── config.py                # System prompts (ROLES), constants, model params
│   ├── models.py                # Whisper & LLaMA initialization (4-bit quant)
│   ├── transcribe.py            # Audio/Video processing pipelines
│   ├── analysis.py              # LLM inference, text generation & async translation
│   ├── export.py                # PDF, DOCX, TXT formatting and generation
│   ├── ui.py                    # Gradio web interface
│   └── app.py                   # Main entry point
│
├── requirements_kaggle.txt      # Cloud dependencies
├── requirements_local.txt       # Local deployment dependencies (CUDA/Torch)
├── .env.example                 # Environment variables template (HF_TOKEN)
├── .gitignore
└── README.md
```

### 🚀 Getting Started

#### Option A: Cloud Deployment (Recommended for users without high-end GPUs)
If you don't have a local GPU with at least 8-12GB VRAM, use the provided Kaggle environment:
1. Open `kaggle_notebook.ipynb` in Kaggle.
2. Ensure the accelerator is set to **GPU T4 x2** or similar.
3. Add your Hugging Face Token to Kaggle Secrets as `HF_TOKEN`.
4. Run all cells.

#### Option B: Local Deployment
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/llama-analyst-station.git](https://github.com/yourusername/llama-analyst-station.git)
   cd llama-analyst-station
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements_local.txt
   ```
3. Create a `.env` file based on `.env.example` and insert your Hugging Face token.
4. Run the application:
   ```bash
   python local/app.py
   ```

### 🛣️ Roadmap
- [ ] **RAG Integration:** Allow users to chat with their entire history of transcribed meetings.
- [ ] **Chunking Pipeline:** Implement sliding window context for processing 2+ hour recordings without hitting token limits.

---

<a id="русский"></a>
## 🇷🇺 Русский

**Llama Analyst Station** — это профессиональное рабочее место на базе ИИ, созданное для преобразования сырых аудио- и видеозаписей в структурированные аналитические отчеты. Проект объединяет передовые модели (OpenAI Whisper для распознавания речи и Meta Llama 3.2 для анализа текста) в единый пайплайн.

Проект демонстрирует навыки модульной разработки AI-приложений, оптимизации использования видеопамяти (4-битное квантование) и проектирования системных промптов (Prompt Engineering).

### ✨ Главные возможности
* **Мультимодальность:** Поддержка загрузки аудио (MP3, WAV) и видео (MP4).
* **LLM-Аналитика:** Извлечение смыслов с помощью 6 заранее спроектированных ролей (например, *Аналитик, SMM-менеджер, Психолог, Критик*).
* **Диаризация спикеров (Опционально):** Встроенная поддержка `pyannote.audio` для разделения текста по говорящим (требуется раскомментировать код для локального использования).
* **Аппаратная оптимизация:** Использование `BitsAndBytes` (NF4 квантование) для запуска тяжелых моделей (3B+ параметров) на потребительских видеокартах 16GB VRAM.
* **Асинхронный перевод:** Стриминг текста и перевода в реальном времени с использованием многопоточности для плавности интерфейса.
* **Google перевод:** Перевод всех видов аналитики ENG/RU.
* **Экспорт отчетов:** Сохранение готовых результатов в форматах `.pdf`, `.docx`, `.txt` и `.md`.

### 🏗️ Архитектура проекта

Репозиторий спроектирован для поддержки как модульного локального запуска, так и быстрого развертывания в облаке (Kaggle).

```text
llama-analyst-station/
│
├── 📓 kaggle_notebook.ipynb     # Для запуска в Kaggle — всё в одном
│
├── 📁 local/                    # Архитектура для локального запуска
│   ├── config.py                # Константы, системные промпты (ROLES)
│   ├── models.py                # Загрузка Whisper + LLaMA (4-bit)
│   ├── transcribe.py            # Функции расшифровки аудио
│   ├── analysis.py              # Генерация LLM-ответов и асинхронный перевод
│   ├── export.py                # Сохранение в PDF, DOCX, TXT
│   ├── ui.py                    # Веб-интерфейс на Gradio
│   └── app.py                   # Главная точка входа
│
├── requirements_kaggle.txt      # Зависимости для облака
├── requirements_local.txt       # Зависимости для локального запуска
├── .env.example                 # Пример переменных окружения
├── .gitignore
└── README.md
```

### 🚀 Установка и запуск

#### Вариант А: Запуск в облаке (Рекомендуется при отсутствии GPU)
Если ваша текущая система не позволяет развернуть LLM локально, используйте Kaggle:
1. Откройте `kaggle_notebook.ipynb` в среде Kaggle.
2. Включите акселератор **GPU T4**.
3. Добавьте ваш токен Hugging Face в Kaggle Secrets под именем `HF_TOKEN`.
4. Запустите все ячейки (Run All).

#### Вариант Б: Локальный запуск (Требуется GPU от 8GB+ VRAM)
1. Склонируйте репозиторий:
   ```bash
   git clone [https://github.com/yourusername/llama-analyst-station.git](https://github.com/yourusername/llama-analyst-station.git)
   cd llama-analyst-station
   ```
2. Создайте виртуальное окружение и установите зависимости:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Для Windows
   pip install -r requirements_local.txt
   ```
3. Создайте файл `.env`, опираясь на `.env.example`, и добавьте ваш `HF_TOKEN`.
4. Запустите приложение:
   ```bash
   python local/app.py
   ```

### 🛣️ Планы развития
- [ ] **RAG-система:** Возможность задавать вопросы к архиву всех прошлых записей.
- [ ] **Chunking алгоритмы:** Обработка длинных записей (от 2 часов) без переполнения контекстного окна модели.
- [ ] 
