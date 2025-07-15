# @title Import necessary libraries
import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm # For multi-model support
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types # For creating message Content/Parts

# import warnings
# # Ignore all warnings
# warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)


os.environ['DEEPSEEK_API_KEY'] = 'sk-94e460547fd24456abdb50bd1160d9e3'
MODEL_DEEPSEEK = "deepseek/deepseek-chat"

# @title Define the Code Tutor Agent
# Use one of the model constants defined earlier

root_agent = Agent(
    name="code_tutor",
    model=LiteLlm(model=MODEL_DEEPSEEK), # Can be a string for Gemini or a LiteLlm object
    description="用于回答中学生编程相关问题的智能体",
    instruction=" 你是一个中学生编程问题的专家。学生可能会问你各种编程类型的问题"
    "。请用中文回答他们的问题，确保回答准确且易于理解。"
    "如果你不确定答案，请诚实地告诉他们，并建议他们查阅相关资料。"
    "请确保你的代码示例清晰易懂，并提供必要的注释，要求代码是中学生容易理解的。"
    "请确保不要直接提供完整的代码，而是引导学生一步步理解和编写代码。",
)
