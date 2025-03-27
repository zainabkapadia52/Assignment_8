from fastapi import FastAPI
from elasticsearch import Elasticsearch
from uuid import uuid4
import uvicorn
import os

app = FastAPI()

ES_SERVER = os.environ.get("ES_HOST", "http://localhost:9200")
client = Elasticsearch(ES_SERVER)
INDEX = "docs_collection"

def initialize_index():
    if not client.indices.exists(index=INDEX):
        client.indices.create(index=INDEX, body={
            "mappings": {
                "properties": {
                    "doc_id": {"type": "keyword"},
                    "content": {"type": "text"}
                }
            }
        })

initialize_index()

@app.get("/search/{term}")
async def search_document(term: str):
    result = client.search(index=INDEX, body={
        "query": {"match": {"content": term}}
    })
    return {"results": result["hits"]["hits"]}

@app.get("/add/{content}")
async def add_document(content: str):
    new_id = str(uuid4())
    document = {"doc_id": new_id, "content": content}
    response = client.index(index=INDEX, id=new_id, document=document)
    return {"status": response["result"], "id": new_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9200)