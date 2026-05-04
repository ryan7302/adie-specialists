import subprocess
import os
import time
from urllib.parse import urlparse

class Arachne:
    def __init__(self, config):
        self.config = config

    def validate_file(self, filename):
        valid_extensions = ['.html', '.css', '.js', '.jpg', '.png', '.gif']
        if not os.path.exists(filename):    
            return False
        
        _, extension = os.path.splitext(filename)
        return extension in valid_extensions or self.is_image_file(filename)
    
    def is_image_file(self, filename):
        image_extensions = ['.jpg', '.png', '.gif']
         _, extension = os.path.splitext(filename)
        return extension in image_extensions
        
    def run_tests(self):
        test_command = self.config['test_command']
        for i in range(3):
            print(f"Running tests with command:   {test_command}  (attempt  {i+1})")
            result = subprocess.run(test_command, shell=True)
            if result.returncode == 0:
                return True
        return False
    
    def fetch_documentation(self, doc_config):
        if 'url' in doc_config and self.is_valid_url(doc_config['url']):
            command = f"wget -O documentation.html {doc_config['url']}"
            print(f"Fetching documentation with command:   {command}")
            subprocess.run(command, shell=True)
    
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
        
    def start_daemon(self):
        while True:
            self.run_tests()
            time.sleep(60)