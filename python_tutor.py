import os
import asyncio
from google.generativeai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.sessions.in_memory_session_service import (
    InMemorySessionService,
)
from google.adk.auth.credential_service.in_memory_credential_service import (
    InMemoryCredentialService,
)
from google.adk.runners import Runner
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm

SYSTEM_PROMPT = (
    "你是一个友好的 Python 编程辅导老师，面对的学生是中学生初学者。"
    "你的目标是引导学生自己完成任务。首先通过启发式提问和给出小提示，"
    "逐步帮助学生思考；如果学生多次尝试仍有困难，再提供更详细的提示，"
    "最后给出完整示例并附上清晰易懂的解释。请始终使用中文回答，语言要简洁、鼓励。"
)


async def main() -> None:
    model_name = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
    if model_name.startswith("gemini"):
        llm_model = Gemini(model=model_name)
    else:
        llm_model = LiteLlm(model=model_name)
    root_agent = LlmAgent(
        name="python_tutor",
        instruction=SYSTEM_PROMPT,
        model=llm_model,
    )
    artifact_service = InMemoryArtifactService()
    session_service = InMemorySessionService()
    credential_service = InMemoryCredentialService()

    user_id = "student"
    session = await session_service.create_session(
        app_name="python_tutor", user_id=user_id
    )
    runner = Runner(
        app_name="python_tutor",
        agent=root_agent,
        artifact_service=artifact_service,
        session_service=session_service,
        credential_service=credential_service,
    )

    print("欢迎使用 Python 自学助手，输入 exit 或 quit 退出。")
    while True:
        try:
            user_input = input("你: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                print("再见！")
                break
            content = types.Content(role="user", parts=[types.Part(text=user_input)])
            async for event in runner.run_async(
                user_id=user_id, session_id=session.id, new_message=content
            ):
                if event.content and event.content.parts:
                    text = "".join(part.text or "" for part in event.content.parts)
                    if text:
                        print(f"{event.author}: {text}")
        except KeyboardInterrupt:
            print("\n再见！")
            break


if __name__ == "__main__":
    asyncio.run(main())
