from src.custom_logger import logger
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import src.ui_controller as ctrl
import subprocess

prompt_template = """
You are an expert in reading data from diffrent files and their content. Your job is to answer to questions only from context given to you. 
You do this by reading text below and making user understand better on the question asked.

------------
{context}
------------

Generate answer that will apear to user who asked question.
Make sure not to lose any important information.
If you don't know the answer, say you don't know or ask user to rephrase their question for better understanding. Don't cook any wrong information.
Question: {question}
"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=['context','question'])

def generate_chatbot_response(self,user_message):
        # Sample chatbot response logic (replace with your own logic)       
        if user_message:
            
            response = self.answer_generation_chain.run(user_message)
            #self.vector_index.search(user_message) 
            # response = ['Hi! how are you', "Tell me more.", "That's interesting!"]
            # response = random.choice(response)
        return response
        
def get_corpus_chunks(self,corpus):
    try:
        
        docs = []
        logger.info("get_corpus_chunks calleds for text len : ",len(corpus.split(" ")))
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(self.corpus)                  
        docs = [Document(page_content = t) for t in texts]
        logger.info("docs lenth : %d", len(docs))    
        return docs
    except Exception as e:
        logger.info(f"An error occurred during chunking: {e}")
        
        
def getVectorIndexForLoader(self):
    try:
        corpus = self.corpus
        #self.vector_index = VectorstoreIndexCreator().from_documents(self.get_corpus_chunks(corpus)) 
        embeddings = OpenAIEmbeddings()

        self.vector_index = FAISS.from_documents(get_corpus_chunks(self, corpus), embeddings)
        llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo")
        
        self.answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen, 
                                            chain_type="stuff", 
                                            retriever=self.vector_index.as_retriever(),
                                            chain_type_kwargs = {"prompt": PROMPT})
        self.showChatWindow()
    except Exception as e:
        logger.info(f"An error occurred: {e}")            
        if e.message:               
            self.errorMsg.config( text=e.message , fg="red")
        else:
            self.errorMsg.config( text="Application is facing difficulty in connecting with Open.Ai."\
                                    " \n Consider checking your plan and billing details OR Try again later." , fg="red")               
        
            
        ctrl.hideButton(self, self.start_chat_Button)

    
def setEnvironmentVariable(name, value):
        command = f'setx {name} "{value}"'
        #Calling the subprocess to run the command for adding the environment variable
        subprocess.run(command, shell=True)
        return True