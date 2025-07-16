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

os.environ['DEEPSEEK_API_KEY'] = ''
MODEL_DEEPSEEK = "deepseek/deepseek-chat"

# Define 2 agents: code agent, teacher agent

code_agent = None
try:
    code_agent = Agent(
        name="code_agent",
        model=LiteLlm(model=MODEL_DEEPSEEK), # Can be a string for Gemini or a LiteLlm object
        description="用于生成代码的智能体",
        instruction="你是一个写代码的智能体"
        "你负责根据需要来写代码，要求代码简单，中学生可以读懂。",
    )
    print(f"Agent '{code_agent.name}' created using model '{MODEL_DEEPSEEK}'.")
except Exception as e:
    print(f"Could not create code agent: {e}")

teacher_agent = None
try:   
    teacher_agent = Agent(
        name="teacher_agent",
        model=LiteLlm(model=MODEL_DEEPSEEK), # Can be a string for Gemini or a LiteLlm object
        description="用于作为老师的智能体",
        instruction="你是老师，你要根据学生的提问做出回答。"
        "你的学生是中学生，所以要用中学生能理解的语言来回答他们的问题。"
        "你要用中文回答问题。并且注意不要直接给出学生答案，而是要启发性的反问学生，让他们自己思考出答案。"
        "注意你不负责给出代码，写代码的工作由其他agent完成",
    )
    print(f"Agent '{teacher_agent.name}' created using model '{MODEL_DEEPSEEK}'.")
except Exception as e:
    print(f"Could not create teacher agent: {e}")

# @title Define the Root Agent with Sub-Agents

root_agent = None
runner_root = None # Initialize runner

if code_agent and teacher_agent:
    # Let's use a capable Gemini model for the root agent to handle orchestration

    code_agent_team = Agent(
        name="code_agent_team", # Give it a new version name
        model=LiteLlm(model=MODEL_DEEPSEEK),
        description="用于中学生编程问题的专家",
        instruction="你是一个编程专家，需要指导中学生进行编程。你要用中文来回答问题 "
                    "你有2个sub-agent帮助你完成相关功能"
                    "1. 'code_agent': 用于编写代码，确保代码简单易懂，适合中学生阅读。 "
                    "2. 'teacher_agent': 用于回答学生问题，并尽可能启发学生思考。 "
                    "你需要根据学生的提问来决定调用什么agent。如果你判断是需要跟学生进一步交流的，就调用teacher_agent来回答学生问题。"
                    "如果你判断是需要生成代码的，就调用code_agent来生成代码。注意code_agent是一个智能体，不是tools"
                    "请注意，除非是明确必须写代码了，否则尽可能调用teacher_agent来回答问题。",
        sub_agents=[code_agent, teacher_agent]
    )
    print(f"✅ Root Agent '{code_agent_team.name}' created using model '{MODEL_DEEPSEEK}' with sub-agents: {[sa.name for sa in code_agent_team.sub_agents]}")
    root_agent = code_agent_team

else:
    print("❌ Cannot create root agent because one or more sub-agents failed to initialize")
    if not code_agent: print(" - Code Agent is missing.")
    if not teacher_agent: print(" - Farewell Agent is missing.")

