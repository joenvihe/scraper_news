import sys
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.retrievers import SVMRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import CallbackManager

retriever_type = "SIMILARITY SEARCH"
# Use RecursiveCharacterTextSplitter as the default and only text splitter
splitter_type = "RecursiveCharacterTextSplitter"

def create_retriever(_embeddings, splits, retriever_type):
    if retriever_type == "SIMILARITY SEARCH":
        try:
            vectorstore = FAISS.from_texts(splits, _embeddings)
        except (IndexError, ValueError) as e:
            print(f"Error creating vectorstore: {e}")
            return
        retriever = vectorstore.as_retriever(k=5)
    elif retriever_type == "SUPPORT VECTOR MACHINES":
        retriever = SVMRetriever.from_texts(splits, _embeddings)

    return retriever

def split_texts(text, chunk_size, overlap, split_method):

    # Split texts
    # IN: text, chunk size, overlap, split_method
    # OUT: list of str splits

    split_method = "RecursiveTextSplitter"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap)

    splits = text_splitter.split_text(text)
    if not splits:
        print("Failed to split document")

    return splits

if __name__ == '__main__':
    if len(sys.argv) == 3:
        os.environ["OPENAI_API_KEY"] = os.environ["TOKEN_OPENAI_CHATGPT"]
        user_question_file = sys.argv[1]
        content_file = sys.argv[2]
        # Load and process the uploaded PDF or TXT files.
        with open(user_question_file, "r") as archivo:
            user_question = archivo.read()

        # Load and process the uploaded PDF or TXT files.
        with open(content_file, "r") as archivo:
            loaded_text = archivo.read()
             
        # Split the document into chunks
        splits = split_texts(loaded_text, chunk_size=1000,
                            overlap=0, split_method=splitter_type)


        embeddings = OpenAIEmbeddings()
        retriever = create_retriever(embeddings, splits, retriever_type)
        # Initialize the RetrievalQA chain with streaming output
        callback_handler = StreamingStdOutCallbackHandler()
        callback_manager = CallbackManager([callback_handler])

        chat_openai = ChatOpenAI(
            streaming=True, callback_manager=callback_manager, verbose=True, temperature=0)
        qa = RetrievalQA.from_chain_type(llm=chat_openai, retriever=retriever, chain_type="stuff", verbose=True)
        
        answer = qa.run(user_question)
        print("Answer:", answer)


