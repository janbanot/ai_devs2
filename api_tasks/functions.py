import os
from dotenv import load_dotenv
from ai_devs_task import Task
from typing import Dict, Any

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")

functions: Task = Task(ai_devs_api_key, "functions")
token: str = functions.auth()
task_content: Dict[str, Any] = functions.get_content(token)
answer_payload: Dict[str, Any] = {
    "answer": {
            "name": "addUser",
            "description": "add a new user",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "provide name of the user"
                    },
                    "surname": {
                        "type": "string",
                        "description": "provide surname of the user"
                    },
                    "year": {
                        "type": "integer",
                        "description": "provide year of birth of the user"
                    }
                }
            }
        }
}

task_result: Dict[str, Any] = functions.post_answer(token, answer_payload)
print(task_result)
