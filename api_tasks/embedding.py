import os
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

embedding: Task = Task(ai_devs_api_key, "embedding")
token: str = embedding.auth()

text_string: str = "Hawaiian pizza"
model_id: str = "text-embedding-ada-002"

embedding_list: List[float] = client.embeddings.create(
    input=text_string,
    model=model_id).data[0].embedding

answer_payload: Dict[str, List[float]] = {"answer": embedding_list}
task_result: Dict[str, Any] = embedding.post_answer(token, answer_payload)
print(task_result)
