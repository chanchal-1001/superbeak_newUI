from custom_logger import logger
import os
import math
import fitz
import docx
from src.table import Table
from tkinter import filedialog
import src.ui_controller as ctrl

def select_directory(self):
        if self.table:
            self.table.delete_table()
            self.table.destroy()
        ctrl.hideButton(self.upload_Button)
        ctrl.hideButton(self.refresh_button)        
        self.directory_path = filedialog.askdirectory(title="Select files")        
        display_files(self)
        ctrl.hide_and_clear_chat(self)
                
def display_files(self):        
    self.file_S_no = 0
    self.filesDetails = []
    if self.directory_path:  
        logger.info(self.directory_path)
        self.selected_dir.config(text=f"Selected directory: {self.directory_path}")        
        self.files = os.listdir(self.directory_path)            
        filesList = ''
        allowed_file_type = ['txt','pdf','docx']     
        logger.info(self.files)
        for index, value in enumerate(self.files):                     
            f_path = os.path.join(self.directory_path, value)
            if os.path.isfile(f_path) :#and value.split('.')[1] in allowed_file_type:
                #filesList += f'\n {index+1}: {value}'                    
                f_path = os.path.join(self.directory_path, value)
                get_file_properties(self, f_path)

        table = Table(self.window, self.filesDetails)
        self.table = table
        table.pack(padx=10, pady=10)                           
        #self.selected_files.config( text=newline.join([f'{index+1}: {value}' for index, value in enumerate(self.files)]))  
        #self.selected_files.config( text= filesList )  
        logger.info(self.filesDetails)
        ctrl.showButton(self.upload_Button)
        self.upload_Button.config(command=lambda :upload_files(self))            
        ctrl.showButton(self.refresh_button)
        self.refresh_button.config(command= lambda :ctrl.delete_and_display(self))            
    #self.upload_Button.pack()                              

def upload_files(self):    
        corpus = ''
        count = 0
        self.error_msg_text = ""
        allowed_file_type = ['txt','pdf','docx']          
        ctrl.hideButton( self.refresh_button)       
        ctrl.hideButton( self.start_chat_Button)        
        
        for f in self.filesDetails:           
            file_name = f['File Name'] 
            file_content = ""            
            f_path = os.path.join(self.directory_path, file_name)
            f_path = f_path.replace("\\", "/")
            if not file_name.split('.')[1] in allowed_file_type:
                handle_file_exceptions(self, f_path, f["File Size"], file_content, "Supported file types are 'txt','pdf','docx' but trying to read ")
            elif file_name.startswith('~'): 
                    handle_file_exceptions(self, f_path, f["File Size"], file_content, "Ignoring the file starting with ~")
            else:                                    
                logger.info(f"Reading file : {f_path}")
                prefix = ' Content under ' + file_name + ' file : '
                if os.path.isfile(f_path)  and os.path.exists(f_path):                    
                    if f_path.endswith('.txt'):                                
                        file_content = read_txt(self, f_path)
                        corpus += prefix + file_content
                        count  = count + 1 
                    elif f_path.endswith('.docx'):   
                        file_content = read_docx(self, f_path)
                        corpus += prefix + file_content
                        count +=1
                    elif f_path.endswith('.pdf'):   
                        file_content = read_pdf(self, f_path)
                        corpus += prefix + file_content
                        count +=1           
        
        self.corpus = corpus + " Total number of files are " + str(count) +"."          
        ctrl.hideButton( self.upload_Button) 
        ctrl.showButton( self.refresh_button)                    
        ctrl.showButton( self.start_chat_Button)

def read_docx(self,f_path):
    file_content = ""
    error_msg = ""        
    try:
        file_size = os.path.getsize(f_path)              
        # Create a Document object from the .docx file
        doc =  docx.Document(f_path)
        # Iterate through paragraphs and append text to the content string            
        for paragraph in doc.paragraphs:                               
            if paragraph.text:                     
                file_content += paragraph.text + "\n"                 
    except Exception as e:                         
        error_msg = f'Problem occured {e} while reading the file'
        lbl_msg = self.errorMsg["text"]
        new_errmsg = lbl_msg + f'\n{error_msg} : {f_path}'
        self.errorMsg.config(text = new_errmsg, fg="red")           
    handle_file_exceptions(self, f_path, file_size, file_content, error_msg)        
    return file_content
    
    
def read_txt(self, f_path):        
    file_content = ""
    error_msg = ""        
    try:
        file_size = os.path.getsize(f_path)             
        with open(f_path, "r") as file:
            for line in file:
                file_content += line                                 
    except Exception as e:        
        error_msg = f'Problem occured {e} while reading the file'
        lbl_msg = self.errorMsg["text"]
        new_errmsg = lbl_msg + f'\n{error_msg} : {file}'
        self.errorMsg.config(text = new_errmsg, fg="red")            
    handle_file_exceptions(self, f_path,file_size, file_content,error_msg)    
    return file_content
    
    
def read_pdf(self, f_path):
    file_content = ''
    error_msg = ""        
    try:
        file_size = os.path.getsize(f_path) 
        # Open the PDF file
        with fitz.open(f_path) as pdf_document:
        # Iterate through pages and extract text

            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                file_content += page.get_text()
            # # Close the PDF file
            # pdf_document.close()
    except Exception as e:            
        logger.info("Error reading PDF file")
        error_msg = f'Problem occured {e} while reading the file'
        lbl_msg = self.errorMsg["text"]
        new_errmsg = lbl_msg + f'\n{error_msg} : {f_path}'
        self.errorMsg.config(text = new_errmsg, fg="red")
    handle_file_exceptions(self, f_path,file_size, file_content,error_msg)        
    return file_content

def handle_file_exceptions(self, file, file_size, file_content, error_msg):
    file = file.split('/')
    file = file[len(file)-1]
    logger.info(f"handle file exceptions for : {file}")
    lbl_msg = self.errorMsg["text"]        
    if len(error_msg) > 0 :
            self.error_msg_text = f'{error_msg} : {file}'
    else:            
        if int(file_size) > 0 and file_content == "":             
            self.error_msg_text = lbl_msg + f'\n*Problem Occured while reading the file : {file}'        
            logger.error(self.error_msg_text)    
        elif int(file_size) == 0: 
            self.error_msg_text = lbl_msg + f'\nWarning!!! File is empty : {file}'
            logger.error(self.error_msg_text)  
        

    self.errorMsg.config(text = self.error_msg_text, fg="red")
            
def get_file_properties(self,file_path):
    # Get the file size in bytes
    file_size = os.path.getsize(file_path)
    file_size = math.ceil( file_size/ 1024)
    self.file_S_no += 1
    file_dict = {'S.No': self.file_S_no, 'File Name':os.path.basename(file_path),'File Size':file_size}
    self.filesDetails.append(file_dict)
    # Get other file properties
    file_properties = {
        "file_size": file_size,            
        "isDirectory": os.path.isdir(file_path),
        "isFile": os.path.isfile(file_path),
        "lastModifiedTime": os.path.getmtime(file_path),
        "creationTime": os.path.getctime(file_path),
    }                     
    return file_properties