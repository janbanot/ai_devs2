from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.http.models import PointStruct
from qdrant_client.http.exceptions import UnexpectedResponse


client = QdrantClient("localhost", port=6333)
collection_name = "test_collection2"
try:
    response = client.get_collection(collection_name=collection_name)
    print(response)
except UnexpectedResponse as e:
    if "404 (Not Found)" in str(e):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=4, distance=Distance.DOT),
            on_disk_payload=True
        )

        operation_info = client.upsert(
            collection_name=collection_name,
            wait=True,
            points=[
                PointStruct(id=1, vector=[0.05, 0.61, 0.76, 0.74], payload={"city": "Berlin"}),
                PointStruct(id=2, vector=[0.19, 0.81, 0.75, 0.11], payload={"city": "London"}),
                PointStruct(id=3, vector=[0.36, 0.55, 0.47, 0.94], payload={"city": "Moscow"}),
                PointStruct(id=4, vector=[0.18, 0.01, 0.85, 0.80], payload={"city": "New York"}),
                PointStruct(id=5, vector=[0.24, 0.18, 0.22, 0.44], payload={"city": "Beijing"}),
                PointStruct(id=6, vector=[0.35, 0.08, 0.11, 0.44], payload={"city": "Mumbai"}),
            ]
        )
    else:
        print(e)
