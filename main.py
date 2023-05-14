import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from llama_index import StorageContext, load_index_from_storage
from llama_index.node_parser import SimpleNodeParser
from llama_index import LLMPredictor, GPTVectorStoreIndex, PromptHelper, ServiceContext
import os
import sys
app = FastAPI()

os.environ["OPENAI_API_KEY"] = "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"


class Questions(BaseModel):
    text: str

@ app.get('/')
def index():
    return {'message': 'Welcome to our Brand New Chatbot'}

@app.get('/answer/{question}')
def predict_review(question:str):
    storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    print(response)
    return {
        'answer': response
    }

@app.post('/answer')
def predict_review(data:Questions):
    received = data.dict()
    question = received['text']
    storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    print(response)
    return {
        'answer': response
    }

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)