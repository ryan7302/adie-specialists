import subprocess
from pathlib import Path
import json
import re
import requests

class Arachne:
    def __init__(self, config_path="arachne_config.json", tasks_path="arachne_tasks.txt"):
        self.config_path = config_path
        self.tasks_path = tasks_path
        self.config = self.load_config()
        self.repo = self.config["repo"]
        self.workspace = Path("./arachne_workspace") / self.repo.replace("/", "_")
        self.git = None
    
    def validate_file(self, file_path):
        path = Path(file_path)
        return path.is_file()
        
    #... existing methods here ...

    def run_tests(self):
        test_command  = self.config['test_command']
        max_retries = self.config['max_test_retries']
        
        for _ in range(max_retries):
            result = subprocess.run(test_command, shell=True, capture_output=True)
            
            if result.returncode == 0:
                return True
                
        return False
    
    def validate_web_file(self, file_path):
        # Check if it's a URL
        try:
            request = requests.get(file_path)
            if request.status_code == 200 and '.html' in file_path or '.css' in file_path or '.js' in file_path:
                return True
            else:
                return False
        except:  # If it's not a URL, check if local file with .html, .css, or .js extension
            path = Path(file_path)
            if path.is_file() and ('.html' in file_path or '.css' in file_path or '.js' in file_path):
                return True
            else:
                return False