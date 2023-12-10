import os
import openai
import json
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, List, Any

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

tools: Task = Task(ai_devs_api_key, "tools")
token: str = tools.auth()
task_content: Dict[str, Any] = tools.get_content(token)
print(task_content["question"])


def function_calling(query: str) -> Dict[str, Any]:
    function_descriptions: List[Dict[str, Any]] = [
                {
                    "name": "categorisation",
                    "description": "Categorise the input to one of two categories",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "ToDo (eg. 'Przypomnij mi, że mam kupić mleko') or Calendar (eg. 'Jutro mam spotkanie z Marianem')",  # noqa: E501
                                "enum": ["ToDo", "Calendar"]
                            },
                            "desc": {
                                "type": "string",
                                "description": "Task content eg. 'Przypomnij mi, że mam kupić mleko' -> 'Kup mleko' or 'Jutro mam spotkanie z Marianem' -> 'Spotkanie z Marianem'",  # noqa: E501
                            },
                            "date": {
                                "type": "string",
                                "description": "Date for the task eg. 'Jutro mam spotkanie z Marianem' -> 'datetime.tommorrow'",  # noqa: E501
                            }
                        },
                        "required": ["category", "desc"]
                    },
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


fcall_dict = function_calling(task_content["question"])
json_dict = json.loads(fcall_dict["arguments"])

answer_dict = new_dict = {
  "tool": json_dict["category"],
  "desc": json_dict["desc"],
}
# TODO: add date parsing to datetime
if "date" in json_dict:
    new_dict["date"] = json_dict["date"]

answer_payload: Dict[str, Any] = {"answer": answer_dict}
task_result: Dict[str, Any] = tools.post_answer(token, answer_payload)
print(task_result)
