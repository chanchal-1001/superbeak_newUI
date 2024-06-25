import os
from pathlib import Path
from custom_logger import logger

list_of_files = [
    "src/__init__.py",    
    "images/"
    ".env",
    "setup.py",
    "research/app.ipynb",   
    "requirement.txt" 
]

for file_path in list_of_files:
    file_path = Path(file_path)
    
    file_dir, file_name = os.path.split(file_path)

    if file_dir!= "":
        os.makedirs(file_dir, exist_ok=True)
    logger.info(f"{file_path}")
    
    if (not os.path.exists(file_path) or os.path.getsize(file_path) == 0) :
        with open(file_path,'w') as f:
            pass
    else:
        logger.warning(f"{file_name} is already exists")
    