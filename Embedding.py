import getpass
import os
import time



import ReadPDF
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from typing import List
from langchain_aws import ChatBedrock
from langchain.tools import tool
from langchain_core.documents import Document
from langchain_core.runnables import chain
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model
from langchain_aws import BedrockEmbeddings, ChatBedrock, AmazonKnowledgeBasesRetriever


google_model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")
#aws_model = ChatBedrock(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
aws_model = ChatBedrock(model="anthropic.claude-3-sonnet-20240229-v1:0")

# if not os.environ.get("OPENAI_API_KEY"):
#     print("OpenAI API key not set")
#     os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

if not os.environ.get("GOOGLE_API_KEY"):
    print("Google API key not set")
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


model_gemma = "google/embeddinggemma-300m"

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
#embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

vector_store = InMemoryVectorStore(embeddings)

def setupVectorStore():
    docs = ReadPDF.ReadPDF('pdfjs/input.pdf')
    splits = ReadPDF.TextSplitter(docs)
    ids = vector_store.add_documents(documents=splits)
    print("-------------------Vector Database-------------------")

@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information to help answer a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    print("Retrieve_context123",retrieved_docs)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs
#retrieve_context("What is size of the matrix display")

tools = [retrieve_context]

prompt = (
    "You have access to a tool that retrieves context from a research paper "
    "Use the tool to help answer user queries."
)

def search(querystring) :
    agent = create_agent(google_model, tools, system_prompt=prompt)

    query = (
        f"{querystring}\n\n "
    )
    print("Query String", query)
    final_result = ""
    #agent.run({"messages": [{"role": "user", "content": query}]})

    for event in agent.stream(
        {"messages": [{"role": "user", "content": query}]},
        stream_mode="values",
    ):
        final_result = event["messages"][-1].content

    return final_result[0]["text"] #pip install -U `langchain-openai

    # for event in agent.stream(
    #     {"messages": [{"role": "user", "content": query}]},
    #     stream_mode="values",
    #     event["messages"][-1].pretty_print()


# setupVectorStore()
# results = search("What is the power consumption of the LED matrix display?")
# print(f"Result123:{results}")