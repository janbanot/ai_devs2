import os
from dotenv import load_dotenv
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")

helloapi = Task(ai_devs_api_key, "helloapi")

token = helloapi.auth()
task_content = helloapi.get_content(token)

cookie = task_content['cookie']
task_payload = {"answer": cookie}

result = helloapi.post_answer(token, task_payload)
print(result)
