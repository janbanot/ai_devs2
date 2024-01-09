import os
import requests  # type: ignore
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any
from openai import OpenAI

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

optimaldb: Task = Task(ai_devs_api_key, "optimaldb")
token: str = optimaldb.auth()
task_content: Dict[str, Any] = optimaldb.get_content(token)
print(task_content)
db_url: str = task_content["database"]
people_data = requests.get(db_url).json()

optimal_db = {}
prompt = """Compress information that you have about this person.
            Condense the data without losing any specific info.
            Answer in polish."""
for key, value in people_data.items():
    model_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": str(value)}
        ]
    )
    shortened_info = model_response.choices[0].message.content or ""
    optimal_db[key] = shortened_info

# print(optimal_db)
answer_payload: Dict[str, str] = {"answer": str(optimal_db)}
task_result: Dict[str, Any] = optimaldb.post_answer(token, answer_payload)
print(task_result)
