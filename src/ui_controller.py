import os
import tkinter as tk
from src.custom_logger import logger
import src.resource_handler as res
import src.file_handler as fh
        
def hideButton(button):
    button.pack_forget()

def showButton(button):        
    button.pack()

def close_chatwindow(self):
    self.window.destroy()        
                    
def delete_and_display(self):
    self.files = os.listdir(self.directory_path)   
    if len(self.files) != self.file_S_no:
        logger.info("Deleting table content and loading again")
        self.errorMsg.config(text = "")
        hideButton(self.upload_Button)
        hideButton(self.refresh_button)   
        hideButton(self.start_chat_Button)   
        self.table.delete_table()
        self.table.destroy()    
        fh.display_files(self)
        showButton(self.upload_Button)
        showButton(self.refresh_button)
        hide_and_clear_chat(self)

        
        
def hide_and_clear_chat(self):
    if hasattr(self, 'chat_box'):            
        # Hide the text widget        
        self.chat_box.pack_forget()
        self.input_box.pack_forget()
        # Clear the content of the text widget
        self.input_box.delete('1.0', tk.END)            
        self.chat_box.delete('1.0', tk.END)
        hideButton(self.send_button)

def process_query(self):
    user_message = self.input_box.get("1.0", tk.END).strip()
    logger.info("User query:", user_message)
    if user_message:
        # Enable the widget for modifications
        self.chat_box.config(state=tk.NORMAL)
        self.chat_box.insert(tk.END, f"You: {user_message}\n", "user")
        self.input_box.delete("1.0", tk.END)  # Clear the entry widget
        # Simulate a chatbot response (replace this with your actual chatbot logic)
        self.chat_box.yview(tk.END)
        self.chat_box.config(state=tk.DISABLED)
        
    return user_message
        
def on_enter_press(self, event):           
    user_message = process_query(self)      
    writeResponse(self, user_message)

def on_send_button_click(self):        
    user_message = process_query(self)      
    writeResponse(self, user_message)

def writeResponse(self, user_message):
    self.chat_box.config(state=tk.NORMAL)
    chatbot_response = res.generate_chatbot_response(self, user_message)            
    self.chat_box.insert(tk.END, f"Chatbot: {chatbot_response}\n", "chatbot")
    self.chat_box.yview(tk.END)  # Auto-scroll to the latest message
    self.chat_box.config(state=tk.DISABLED)

def hideReset(self):
    self.enter_new_key_lbl.pack_forget()
    self.enter_new_key.pack_forget()
    self.reset.place_forget()

def reset_key(self):
    # self.enter_new_key_lbl.place(x=900, y=20)
    # self.enter_new_key.place(x=900, y=45)
    #self.reset.place(x=900, y=70)
    self.enter_new_key_lbl.pack()
    self.enter_new_key.pack()
    self.reset.place(x=1000, y=140)