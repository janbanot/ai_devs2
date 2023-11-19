import os
import openai
import requests  # type: ignore
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain.embeddings import OpenAIEmbeddings
from ai_devs_task import Task

load_dotenv()
ai_devs_api_key: str = os.getenv("AI_DEVS_API_KEY", "")
openai.api_key = os.getenv("OPENAI_API_KEY", "")

search = Task(ai_devs_api_key, "search")
token: str = search.auth()
task_content = search.get_content(token)

qdrant = QdrantClient("localhost", port=6333)
embeddings = OpenAIEmbeddings()
COLLECTION_NAME = "search_task"
SOURCE_URL = "https://unknow.news/archiwum.json"

data = requests.get(SOURCE_URL).json()
input_json = data[:300]

collections = qdrant.get_collections()
collection_names = [element.name for element in collections.collections]
if not (COLLECTION_NAME in collection_names):
    qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            on_disk_payload=True
        )

collection_info = qdrant.get_collection(collection_name=COLLECTION_NAME)

if collection_info.points_count == 0:
    for element in input_json:
        metadata = {
            "source": COLLECTION_NAME,
            "content": element["url"],
            "id": uuid.uuid4().hex,
        }
        element.update(metadata)
        point = element["info"]
        point_id = element["id"]
        point_vector = embeddings.embed_query(point)
        point_struct = {"id": point_id, "payload": metadata, "vector": point_vector}
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=[point_struct]
        )

query_embedding = embeddings.embed_query(task_content["question"])
search_result = qdrant.search(
    collection_name=COLLECTION_NAME,
    query_vector=query_embedding,
    limit=1,
    query_filter={
        "must": [
            {
                "key": "source",
                "match": {
                    "value": COLLECTION_NAME
                }
            }
        ]
    }
)
result_url = search_result[0].payload["content"]  # type: ignore
answer_payload = {"answer": result_url}
result = search.post_answer(token, answer_payload)
print(result)
