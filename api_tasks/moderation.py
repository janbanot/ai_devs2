import os
from dotenv import load_dotenv
from ai_devs_task import Task
import openai
from typing import Dict, Any, List

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

moderation: Task = Task(ai_devs_api_key, "moderation")
token: str = moderation.auth()
task_content: Dict[str, Any] = moderation.get_content(token)
sentence_list: List[str] = task_content["input"]

moderation_response: openai.Moderation = openai.Moderation.create(input=sentence_list)
moderation_results: List[Dict[str, Any]] = moderation_response["results"]
results_list: List[int] = [1 if result["flagged"] else 0 for result in moderation_results]
answer_payload: Dict[str, List[int]] = {"answer": results_list}

task_result: Dict[str, Any] = moderation.post_answer(token, answer_payload)
print(task_result)
