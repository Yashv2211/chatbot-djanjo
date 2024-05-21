#from langchain.client import LangchainClient
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
import pinecone
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from langchain.schema import Document, BaseRetriever
from typing import List, Any
from pydantic import BaseModel, Field
from .models import PromptResponse, InternalServerException, NetworkException
from rest_framework.exceptions import APIException
from dotenv import load_dotenv
load_dotenv()
index_name = os.environ.get('PINECONE_INDEX')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class SimpleRetriever(BaseRetriever):
    vector_store: Any 
    k: int = Field(default=5, description="The number of documents to retrieve")

    def _get_relevant_documents(self, query: str) -> List[Document]:
        return self.vector_store.similarity_search(query=query, k=self.k)

    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        return await self.vector_store.similarity_search(query=query, k=self.k)
    

prompt_template="""
Answer like a chatbot. Be polite and respectful.You should greet when someone greets you and also say Bye when the person says bye.
You have information about internet users, poverty and unemployment in Brazil from 1960 to 2023 anf can help people by aswering questions related to internet users, poverty and unemployment in Brazil.
If the question is not relevant to the context ask the user to ask a relevant question.
Do not answer any irrelevant questions.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use the following pieces of information to answer the user's question.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""


class PromptResponder:
    #Initialize the PromptResponder with an index name.
    def __init__(self, index_name):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small",openai_api_key=OPENAI_API_KEY)
        self.PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        self.index_name = index_name
        self.init_network()

    def init_network(self):
         #Initialize all network-related components, handles exceptions related to network issues
        try:
            self.docsearch = self.init_docseacrh()
            self.simple_retriever = SimpleRetriever(vector_store=self.docsearch, k=10)
            self.llm = self.init_llm()
            self.qa = self.init_qa()
        except NetworkException as ne:
            print(f"Responder init failed due to network calls: {ne}")
            raise ne
        except Exception as e:
            print(f"Responder init failed: {e}")
            raise InternalServerException("Failed to initialize promptResponder") from e
        
    def init_docseacrh(self):
        #Initialize document search from an existing Pinecone index, handles network related exceptions.
        try:
            return PineconeVectorStore.from_existing_index(index_name=self.index_name, embedding=self.embeddings)
        except Exception as e:
            print(f"docsearch init failed due to network: {e}")
            raise NetworkException() from e


    def init_llm(self):
        #Initialize the language model, handles network related exceptions.
        try:
            return ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name='gpt-4', temperature=0.8)
        except Exception as e:
            print(f"llm init failed due to network: {e}")
            raise NetworkException() from e

    def respond(self, data):
        #Process the given input data and respond, handles all exceptions during the response generation.
        try:
            response = self.qa(data)
            return response
        except Exception as e:
            print(f"Error occurred while responding: {e}")
            raise InternalServerException("Error occurred while responding") from e

    def init_qa(self):
        #Initialize the question-answering system, handles network related exceptions
        try:
            return RetrievalQA.from_chain_type(llm=self.llm, chain_type="stuff", retriever=self.simple_retriever, chain_type_kwargs={"prompt": self.PROMPT})
        except Exception as e:
            print(f"qa init failed due to network: {e}")
            raise NetworkException() from e


responder = None

def retry_network_init():
    #Attempt to re-initialize network components if the first initialization fails.
    global responder
    if responder:
        responder.init_network()

def process_input(data):
    #Process the input through the responder, handle and report any exceptions that occur
    global responder
        
    try:
        if responder is None:
            responder = PromptResponder(index_name=index_name)
        if responder.llm is None or responder.qa is None:
            retry_network_init()
        response = responder.respond(data)
        result = response.get('result', 'No result found')
        return PromptResponse(result)
    except NetworkException as ne:
        error_message = f"Network error occurred: {ne}"
        raise ne from None
    except InternalServerException as ise:
        error_message = f"Internal server error occurred: {ise}"
        raise ise from None
    except Exception as e:
        error_message = f"Unknown error occurred: {e}"
        raise Exception(error_message) from e
