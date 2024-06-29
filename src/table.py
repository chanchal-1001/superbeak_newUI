from tkinter import font
import tkinter as tk
from src.custom_logger import logger

class Table(tk.Frame):
    def __init__(self, parent, file_dict):
        super().__init__(parent)     
        self.parent = parent
        self.file_dict = file_dict
        # Create a Canvas widget
        self.canvas = tk.Canvas(self.parent, width=300, height=60 , bg="#8DA8C5")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, pady=30, padx = 20)

        # Add a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.canvas.yview ,  width=20)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y , pady=30)

        # Configure the Canvas to use the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Add content to the Canvas (for demonstration purposes)
        self.content_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor=tk.CENTER)
        
        self.create_table()        
        
    def create_table(self):
        
        bold_font = font.Font(family="Helvetica", size=10, weight="bold")
        columns = list(self.file_dict[0].keys())
        for c, column in enumerate(columns):
            if column == 'S.No':
                header_label = tk.Label(self.content_frame, text=column, borderwidth=1, relief="solid", width=5, justify='left',  anchor='w', font = bold_font)
            else:
                header_label = tk.Label(self.content_frame, text=column, borderwidth=1, relief="solid", width=10, justify='left', anchor='w', font = bold_font)
            header_label.grid(row=0, column=c , sticky='n', padx=5, pady=0 )
                
        for r in range(len(self.file_dict)):
            for c, column in enumerate(columns):
                cell_data = self.file_dict[r][column]
                data_label = tk.Label(self.content_frame, text=str(cell_data), borderwidth=1, wraplength=100, justify='left', anchor='w')
                data_label.grid(row=r+1, column=c, sticky='w', padx=5, pady=0)

        
                # Update the Canvas scroll region
        self.content_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        # Move the scrollbar to the top
        self.canvas.yview_moveto(0.0)
        # Bind the MouseWheel event to enable scrolling with the mouse wheel
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)        

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                
    def delete_table(self):
        try:            
            if hasattr(self, 'content_frame') :#and self.content_frame.winfo_children():                
                for widget in self.content_frame.winfo_children():            
                    widget.destroy()
            # Destroy the Scrollbar
            self.scrollbar.destroy()           
            if hasattr(self, 'canvas') and self.canvas.winfo_children():                    
                self.canvas.destroy()
        except Exception as e:
            logger.info("Warning! Tried to clear an empty canvas")