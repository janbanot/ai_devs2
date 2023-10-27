import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")
url_name = "https://zadania.aidevs.pl/token"

url = f"{url_name}/helloapi"
data = {
    "apikey": ai_devs_api_key
}

response = requests.post(url, json=data)

response_json = json.loads(response.text)
token = response_json['token']

url2 = f"{url_name}/task/{token}"
task_response = requests.get(url2)
task_response_json = json.loads(task_response.text)

cookie = task_response_json['cookie']
payload = {
    "answer": cookie
}

url3 = f"{url_name}/answer/{token}"
final_response = requests.post(url3, json=payload)
