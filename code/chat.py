# Libraries
from langchain.vectorstores import Chroma
import os

from langchain.text_splitter import CharacterTextSplitter

from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv


# OpenAIEmbeddings() was deprecated in LangChain 0.1.0 and will be removed in 0.2.0. That's why I use langchain_openai instaed
import langchain_openai
import logging


from utilities.customprompt import PROMPT

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT

from langchain.chains.llm import LLMChain

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

api_key = os.getenv("OPENAI_API_KEY")
k = 4
load_dotenv()


# Initialize logging with the specified configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/log.log"),
        logging.StreamHandler(),
    ],
)
LOGGER = logging.getLogger(__name__)


# Define the llm model
llm=ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.7)


# Load documents from the specified directory
loader = PyPDFLoader("docs/Naval Ravikant - The Almanack.pdf")
documents = loader.load()

# transform words into numbers
embeddings = langchain_openai.OpenAIEmbeddings(openai_api_key=api_key)

# split the text to chuncks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

# Upload into the vector store
vector_store = Chroma.from_documents(texts, embeddings)

# Define answer generation function
def get_semantic_answer_lang_chain(query, chat_history):
    
    # Log a message indicating that the function has started
    LOGGER.info(f"Start answering based on prompt: {query}.")
    
    # Load a QA chain using an OpenAI object, a chain type, and a prompt template.
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT, verbose=False)

    doc_chain = load_qa_with_sources_chain(llm, chain_type="stuff", verbose=False, prompt=PROMPT)

    chain = ConversationalRetrievalChain(
        retriever=vector_store.as_retriever(),
        question_generator=question_generator,
        combine_docs_chain=doc_chain,
        return_source_documents=True,
    )

    # Log a message indicating the number of chunks to be considered when answering the user's query.
    LOGGER.info(f"The top {k} chunks are considered to answer the user's query.")
    
    
    result = chain.invoke({"question": query, "chat_history": chat_history})

    # Extracting unique sources
    unique_sources = set(map(lambda x: x.metadata["source"], result['source_documents']))

    # Enumerating and formatting the sources
    sources = [f"{idx}. {source}" for idx, source in enumerate(unique_sources, start=1)]

    source_chunks="\n".join(f"Chunck_number_{i}:{doc.page_content}" for i, doc in enumerate(result['source_documents']))
    
    # Log a message indicating the answer that was generated
    LOGGER.info(f"The returned answer is: {result['answer']}")

    # Log a message indicating that the function has finished and return the answer.
    LOGGER.info(f"Answering module over.")

    return query, result['answer'], sources, source_chunks

