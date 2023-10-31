# TODO: try rewritting/create another one using Langchain

import os
from dotenv import load_dotenv
from ai_devs_task import Task
import openai

load_dotenv()
ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

moderation = Task(ai_devs_api_key, "moderation")
token = moderation.auth()
task_content = moderation.get_content(token)
sentence_list = task_content["input"]

moderation_response = openai.Moderation.create(input=sentence_list)
moderation_results = moderation_response["results"]
results_list = [1 if result["flagged"] else 0 for result in moderation_results]
answer_payload = {"answer": results_list}

task_result = moderation.post_answer(token, answer_payload)
print(task_result)
