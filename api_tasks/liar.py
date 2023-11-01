import os
import openai
from dotenv import load_dotenv
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

liar = Task(ai_devs_api_key, "liar")

token = liar.auth()
task_content = liar.get_content(token)

question = {"question": "What is the capital of Poland?"}
answer_json = liar.post_question(token, question)
answer = answer_json["answer"]

prompt = """
Answer simply YES or NO
Is it a correct answer to the following question:
"What is the capital of Poland?"
"""

check_answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": answer}
        ]
    )
answer_content = check_answer["choices"][0]["message"]["content"]

result_payload = {"answer": answer_content}
result = liar.post_answer(token, result_payload)
print(result)
