import os
import getpass
from typing import TypedDict, Annotated, List
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
import google.generativeai as genai
from operator import itemgetter
from dotenv import load_dotenv
load_dotenv()

# --- Step 1: Document Loading and Processing ---
def load_and_split_documents(pdf_paths: List[str], web_urls: List[str]):
    """Loads and splits documents from PDFs and websites."""
    docs = []
    # Load PDFs
    for path in pdf_paths:
        loader = PyPDFLoader(path)
        docs.extend(loader.load())
    
    # Load websites
    for url in web_urls:
        loader = WebBaseLoader(url)
        docs.extend(loader.load())

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    all_splits = text_splitter.split_documents(docs)
    return all_splits


def create_retriever(documents: List[Document]):
    """Creates a FAISS vector store and a retriever using Gemini embeddings."""
    vectorstore = FAISS.from_documents(documents, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    retriever = vectorstore.as_retriever()
    return retriever


def get_prompt_template():
    """Returns the chat prompt template."""
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful personal assistant. Use the following context to answer the user's question. "
                "If you don't know the answer, just say that you don't know, don't try to make up an answer."
                "\n\nContext:\n{context}\n\n"
                "Also, ensure your answer is friendly and conversational.",
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )


class GraphState(TypedDict):
    """Represents the state of our graph."""
    messages: Annotated[List[BaseMessage], add_messages]
    context: str

def rag_node(state: GraphState):
    """
    Retrieves documents and generates a response using Gemini.
    """
    print("---EXECUTING RAG NODE---")
    messages = state["messages"]
    last_message = messages[-1]
    
    # The last message is the user's question.
    question = last_message.content

    
    retrieved_docs = retriever.invoke(question)
    context_str = "\n\n".join(doc.page_content for doc in retrieved_docs)
    

    llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0)
    prompt = get_prompt_template()
    
    # Corrected chain using itemgetter to pass the correct variables
    rag_chain = (
        {"context": itemgetter("context"), "messages": itemgetter("messages")}
        | prompt
        | llm
    )
    
    response = rag_chain.invoke({"context": context_str, "messages": messages})

    # Return the updated state
    return {"messages": [response], "context": context_str}

def build_graph():
    """Builds and compiles the LangGraph workflow."""
    workflow = StateGraph(GraphState)
    workflow.add_node("rag", rag_node)
    workflow.add_edge("rag", END)
    workflow.set_entry_point("rag")
    app = workflow.compile()
    return app

# --- Main Execution Block ---
if __name__ == "__main__":

    pdf_files = [r"K:\farmsathichatbot\pesticides recomendation data.pdf"]  
    web_urls = ["https://www.wikipedia.org/wiki/Artificial_intelligence"] 

    print("Loading and processing documents...")
    try:
        documents = load_and_split_documents(pdf_files, web_urls)
        print(f"Loaded {len(documents)} document chunks.")

        print("Creating vector store and retriever...")
        retriever = create_retriever(documents)
        print("Retriever created successfully.")

        print("Building and compiling the LangGraph...")
        rag_app = build_graph()
        print("LangGraph compiled.")

        print("\n--- Personal Assistant is ready! Type 'exit' to quit. ---")
        while True:
            user_question = input("You: ")
            if user_question.lower() == "exit":
                break
            
            # Create the initial message for the graph
            inputs = {"messages": [HumanMessage(content=user_question)]}
            
            # Invoke the graph to get a response
            response = rag_app.invoke(inputs)
            
            # Print the AI's response from the final state
            print("Assistant:", response["messages"][-1].content)

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have a valid Google API key and that the document paths are correct.")
