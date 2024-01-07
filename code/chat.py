# my chatbot
from langchain.vectorstores import Chroma
import os

from langchain.text_splitter import CharacterTextSplitter

from langchain.document_loaders import PyPDFLoader
from dotenv import load_dotenv



# OpenAIEmbeddings() was deprecated in LangChain 0.1.0 and will be removed in 0.2.0. That's why I use langchain_openai instaed
import langchain_openai
import logging

api_key = os.getenv("OPENAI_API_KEY")
k = 4
from utilities.customprompt import PROMPT

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from langchain.chains.chat_vector_db.prompts import CONDENSE_QUESTION_PROMPT

from langchain.chains.llm import LLMChain


load_dotenv()
# Initialize logging with the specified configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(config.LOGS_FILE),
        logging.StreamHandler(),
    ],
)
LOGGER = logging.getLogger(__name__)


llm=langchain_openai.OpenAI(openai_api_key = api_key, model_name="text-davinci-003", temperature=0,max_tokens=300)



# Load documents from the specified directory using a DirectoryLoader object
loader = PyPDFLoader("docs/Naval Ravikant - The Almanack.pdf")
documents = loader.load()


embeddings = langchain_openai.OpenAIEmbeddings(openai_api_key=api_key)

# split the text to chuncks of of size 1000
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)

# split the text to chuncks of size 1000
vector_store = Chroma.from_documents(texts, embeddings)


# Create a vector store from the chunks using an OpenAIEmbeddings object and a Chroma object
embeddings = langchain_openai.OpenAIEmbeddings(openai_api_key=api_key)
docsearch = Chroma.from_documents(documents, embeddings)

# Define answer generation function
def get_semantic_answer_lang_chain(query, chat_history):
    
    # Log a message indicating that the function has started
    LOGGER.info(f"Start answering based on prompt: {query}.")
    
    # Create a prompt template using a template from the config module and input variables
    
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

