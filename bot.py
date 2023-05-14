from llama_index import SimpleDirectoryReader, GPTListIndex, readers, GPTVectorStoreIndex, LLMPredictor, PromptHelper
from llama_index import StorageContext, load_index_from_storage
from llama_index.node_parser import SimpleNodeParser
from llama_index import LLMPredictor, GPTVectorStoreIndex, PromptHelper, ServiceContext
import os
import sys
from dotenv import load_dotenv

load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def construct_index(directory_path):
    documents = SimpleDirectoryReader(directory_path).load_data()
    parser = SimpleNodeParser()
    nodes = parser.get_nodes_from_documents(documents)
    # define LLM
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.4, model_name="text-davinci-003"))

    # define prompt helper
    # set maximum input size
    max_input_size = 4096
    # set number of output tokens
    num_output = 256
    # set maximum chunk overlap
    max_chunk_overlap = 20
    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index = GPTVectorStoreIndex.from_documents(
        documents, service_context=service_context
    )

    index.storage_context.persist(persist_dir="<persist_dir>")
    query_engine = index.as_query_engine()

    while True: 
        query = input("What do you want to ask? ")
        response = query_engine.query(query)
        print(response)

def ask():
    storage_context = StorageContext.from_defaults(persist_dir="<persist_dir>")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    query = input("What do you want to ask? ")
    response = query_engine.query(query)
    print(response)

if __name__ == "__main__":
    # construct_index(sys.argv[1])
    ask()