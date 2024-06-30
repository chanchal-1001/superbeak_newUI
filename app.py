import tkinter as tk
#from tkinter import ttk
import openai
import sys
import os
import subprocess
from langchain.indexes import VectorstoreIndexCreator #uses OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from tkinter import messagebox
from src.custom_logger import logger
from src.table import Table
import src.file_handler as fh
from tkinter import scrolledtext
import src.ui_controller as ctrl
import src.resource_handler as resource
#from dotenv import load_dotenv

class Superbeak:
    def __init__(self):
        logger.info("LOADING THE APPLICATION...")
        self.window = tk.Tk()        
        self.window.title("Super Beak")                 
        self.window.iconbitmap(resource_path("images/superbeak.ico"))
        # width = self.window.winfo_screenwidth() 
        # height= self.window.winfo_screenheight()
        # #self.window.geometry("700x600-0+0")   
        # self.window.geometry("%dx%d" % (width-160, height-110))
        self.window.state('zoomed')
        self.window.configure(bg='lightblue')      
        self.image7 = tk.PhotoImage(file = resource_path("images/send.png"))
        self.set_the_key_img = tk.PhotoImage(file = resource_path("images/set_the_key.png"))
        self.filesDetails = []
        self.file_S_no = 0
        self.table = []       
        self.errorMsg = tk.Label(text = "", wraplength=500, justify='left', bg="lightblue")           
        self.error_msg_text = ""
        #To reset key when needed
        image1 = tk.PhotoImage(file = resource_path("images/reset_key.png"))  
        self.resetKey_button = tk.Button(self.window , image= image1,command=lambda:ctrl.reset_key(self) , bg="lightblue", border="0")

        self.enter_new_key_lbl = tk.Label(self.window, text="Enter Your OpenAI Secret Key:", bg="lightblue", font=20)
        
        self.enter_new_key = tk.Entry(self.window, width=65)
        self.reset = tk.Button(self.window, image= self.set_the_key_img, command=self.setKeyVal , bg="lightblue", border="0")
        
        #to read the files uploaded
        image3 = tk.PhotoImage(file = resource_path("images/start_processing.png"))
        self.upload_Button = tk.Button(image= image3, bg="lightblue", border="0")
        ctrl.hideButton(self.upload_Button)

        #to reload the file directory
        image4 = tk.PhotoImage(file = resource_path("images/reload.png"))
        self.refresh_button = tk.Button( self.window, image= image4, bg="lightblue", border="0")
        ctrl.hideButton(self.refresh_button)

        #Opens file dialog box
        image2 = tk.PhotoImage(file = resource_path("images/select_dir.png"))
        self.seletct_button = tk.Button(self.window, image= image2,command=lambda:fh.select_directory(self), bg="lightblue", border="0")       

        # Create a label to display the selected file paths
        self.selected_dir = tk.Label( text="No directory selected!", bg="lightblue", font=23)                                                      

        #Button to start the chatbot window after processsing
        image5 = tk.PhotoImage(file = resource_path("images/click_start.png"))
        self.start_chat_Button = tk.Button( self.window, image= image5, bg="lightblue", border="0" )
        self.start_chat_Button.config(command=lambda :resource.getVectorIndexForLoader(self))
        
        self.resetKey_button.pack()
        self.seletct_button.pack() 
        self.selected_dir.pack()
        self.errorMsg.pack()

        self.window.mainloop()               

    def showChatWindow(self):
        # Start the Tkinter event loop
        ctrl.hideButton(self.start_chat_Button)
        ctrl.showButton(self.refresh_button)
        # Create a scrolled text widget for displaying messages with a vertical scrollbar
        self.chat_box = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=100, height=30)
       
        # Configure tags for different message styles (user and chatbot)
        self.chat_box.tag_configure("You", foreground="blue")
        self.chat_box.tag_configure("Superbeak", foreground="green")
        self.chat_box.pack()

        self.input_box = tk.Text(self.window, width=100, height=1)
        
        self.input_box.bind("<Return>", lambda event:ctrl.on_enter_press(self, event))
        self.input_box.pack(pady=10)
        
        # Create a button to send messages        
        self.send_button = tk.Button(self.window, text="Send",image= self.image7, command=lambda:ctrl.on_send_button_click(self) , bg='lightblue', border="0") #command=self.on_send_button_click        
        self.send_button.pack(pady=10)
               
        # Configure row and column weights to make the text box resizable
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)

    

    def setKeyVal(self):
        print("setting called")
        key = self.enter_new_key.get()
        key = key.strip()        
        if key and key.startswith("sk-"):                     
            resource.setEnvironmentVariable('OPENAI_API_KEY', key) 
            openai.api_key = os.getenv("OPENAI_API_KEY")                       
            messagebox.showinfo("Key Alert", "OpenAI Key is Set successfully. You can continue using the Superbeak")  
            ctrl.hideReset(self)              
        else:
             messagebox.showinfo("Key Alert", "Please Enter a Valid OpenAI Secret Key")
    

        
def resource_path(relative_path):
        logger.info(f"resource called for {relative_path}")
        """ Get absolute path to resource, works for dev and for PyInstaller """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        logger.info(base_path)
        imagepath =  os.path.join(base_path, relative_path)
        logger.info(f"Printing joined path :{imagepath} ")
        
        if os.path.exists( imagepath):
            logger.info("File exists")
        else:
            logger.info("files doesn't exist")
       
        return os.path.join(base_path, relative_path)    
    
class KeySet:
    def __init__(self):
        # 
        self.resetKeyWindow = tk.Tk()
        self.resetKeyWindow.title("Super Beak")
        self.resetKeyWindow.configure(bg='lightblue') 
        #icon_path = os.path.join(os.path.dirname(__file__), 'superbeak.png')
        self.resetKeyWindow.iconbitmap(resource_path("images/superbeak.ico"))

        self.set_the_key_img = tk.PhotoImage(file = resource_path("images/set_the_key.png"))
          # Define the window size
        window_width = 430
        window_height = 150

        # Get the screen dimension
        screen_width = self.resetKeyWindow.winfo_screenwidth()
        screen_height = self.resetKeyWindow.winfo_screenheight()

        # Calculate the center position
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        #self.window.geometry("430x200-0+0") 
        self.resetKeyWindow.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resetKeyWindow.label = tk.Label(self.resetKeyWindow, text="Enter Your OpenAI Secret Key:", bg="lightblue", font=20)
        self.resetKeyWindow.label.pack(pady=10)
        self.resetKeyWindow.entry = tk.Entry(self.resetKeyWindow, width=65)
        self.resetKeyWindow.entry.pack()
        
        self.resetKeyWindow.set_the_key = tk.Button( self.resetKeyWindow, image=self.set_the_key_img, bg = "lightblue",border="0")        
        self.resetKeyWindow.set_the_key.config(command=self.setKey) 
        self.resetKeyWindow.set_the_key.pack(pady=10)  
        self.resetKeyWindow.mainloop()
    

    def setKey(self):
        key = self.resetKeyWindow.entry.get()
        key = key.strip()
        if key and key.startswith("sk-"):                        
            isEnvSet = resource.setEnvironmentVariable('OPENAI_API_KEY', key)   
            openai.api_key = os.getenv("OPENAI_API_KEY")           
            messagebox.showinfo("Key Alert", "OpenAI Key is set successfully. Make sure to update the key when expired or no credit available." \
                                    "\nIf you are still facing issues using the chatbot, please contact SuperBeak Technical Support for further assistant")            
            
            self.resetKeyWindow.destroy()            
            if isEnvSet:
                    Superbeak()
        else:
            messagebox.showinfo("Key Alert", "Please Enter a Valid OpenAI Secret Key")
            self.resetKeyWindow.destroy()        
            KeySet() 

    


if __name__ == "__main__":    
    logger.info("STARTING THE APPLICATION...")    
    #del os.environ["OPENAI_API_KEY"]
    #pyinstaller --onefile --name=superbeak_1_0 -i superbeak.ico --add-data "src;src" --add-data "images/*.*;images" app.py --hidden-import=tiktoken_ext.openai_public --hidden-import=tiktoken_ext --noconsole 
    if "OPENAI_API_KEY" in os.environ :
        #del os.environ["OPENAI_API_KEY"]           
        openai.api_key = os.getenv("OPENAI_API_KEY")
        Superbeak()          
    else:
        logger.warning("key not available")
        KeySet()
        logger.info("OPENAI_API_KEY key is created and set")    
        
    
