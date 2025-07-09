# ai4eduagent

This repository contains a minimal interactive Python tutor designed for middle school students.

## Requirements
- Python 3.10+
- `google-adk` and `litellm` packages
- An API key for your chosen model provider (OpenAI, DeepSeek, or Google Gemini)

Install dependencies:
```bash
pip install google-adk litellm
```

## Usage
Set the appropriate API key and model, then run the tutor:
```bash
export OPENAI_API_KEY=your-key-here  # or DEEPSEEK_API_KEY / GOOGLE_API_KEY
export MODEL_NAME=gpt-3.5-turbo      # or deepseek-chat / gemini-pro
python python_tutor.py
```

The tutor interacts in Chinese, guiding students step by step to learn Python. Type `exit` or `quit` to leave the conversation.
