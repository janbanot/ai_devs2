import os
import openai
from dotenv import load_dotenv
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

embedding = Task(ai_devs_api_key, "embedding")
token = embedding.auth()

text_string = "Hawaiian pizza"
model_id = "text-embedding-ada-002"

embedding_list = openai.Embedding.create(
    input=text_string,
    model=model_id)["data"][0]["embedding"]

answer_payload = {"answer": embedding_list}
task_result = embedding.post_answer(token, answer_payload)
print(task_result)
