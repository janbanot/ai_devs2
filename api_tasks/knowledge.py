import os
import openai
import requests  # type: ignore
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, List, Any

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

knowledge: Task = Task(ai_devs_api_key, "knowledge")
token: str = knowledge.auth()
task_content: Dict[str, Any] = knowledge.get_content(token)
question: str = task_content["question"]


def get_exchange_rate(currency: str) -> float:
    url: str = f"http://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json"
    response: Dict[str, Any] = requests.get(url).json()
    return response["rates"][0]["mid"]


def get_population(country: str) -> int:
    url: str = f"https://restcountries.com/v3.1/name/{country}"
    response: List[Dict] = requests.get(url).json()
    return response[0]["population"]


def function_calling(query: str) -> Dict[str, Any]:
    function_descriptions: List[Dict[str, Any]] = [
                {
                    "name": "get_exchange_rate",
                    "description": "If question is about exchange rate",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "currency": {
                                "type": "string",
                                "description": "currency name",
                            }
                        },
                        "required": ["currency"]
                    },
                },
                {
                    "name": "get_population",
                    "description": "If question is about country's population",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "country": {
                                "type": "string",
                                "description": "country name",
                            }
                        }
                    },
                    "required": ["country"]
                }
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[{"role": "user", "content": query}],
        functions=function_descriptions
    )
    response_message = response["choices"][0]["message"]

    if "function_call" in response_message:
        return response_message["function_call"]
    else:
        return response_message


fcall = function_calling(question)

if "content" in fcall:
    answer = fcall["content"]
elif fcall["name"] == "get_exchange_rate":
    currency = fcall["arguments"]["currency"]
    answer = get_exchange_rate(currency)
elif fcall["name"] == "get_population":
    country = fcall["arguments"]["country"]
    answer = get_population(country)

answer_payload: Dict[str, str] = {"answer": answer}
task_result: Dict[str, Any] = knowledge.post_answer(token, answer_payload)
print(task_result)
