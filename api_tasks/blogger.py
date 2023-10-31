# TODO: try rewritting/create another one using Langchain

import os
from dotenv import load_dotenv
from ai_devs_task import Task
import openai

load_dotenv()
ai_devs_api_key = os.getenv("AI_DEVS_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")

blogger = Task(ai_devs_api_key, "blogger")
token = blogger.auth()
task_content = blogger.get_content(token)

prompt = """
You are a pizza master that writes a blog about pizza in polish.
Write a short paragraph about the given topic.
"""

result = []
blog_topics = task_content["blog"]
for topic in blog_topics:
    blog_article = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": topic}
        ]
    )
    result.append(blog_article.choices[0].message["content"])

answer_payload = {"answer": result}
task_result = blogger.post_answer(token, answer_payload)
print(task_result)
