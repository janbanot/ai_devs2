# TODO: rewrite using LangChain and use AI to find names in the sentences

import os
import openai
import re
from dotenv import load_dotenv
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

inprompt = Task(ai_devs_api_key, "inprompt")
token = inprompt.auth()
task_content = inprompt.get_content(token)

knowledge_dict = {}
input = task_content["input"]
for entry in input:
    words = entry.split()
    name = words[0]
    knowledge_dict[name] = entry

question = task_content["question"]
name_pattern = r"\b[A-Z][a-z]*\b"
subject = re.findall(name_pattern, question)[0]
subject_info = knowledge_dict[subject]

prompt = f"""
Answer the question shortly using only the information given below:
{subject_info}
"""

model_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question}
        ]
)
task_answer = model_response["choices"][0]["message"]["content"]

answer_payload = {"answer": task_answer}
task_result = inprompt.post_answer(token, answer_payload)
print(task_result)
