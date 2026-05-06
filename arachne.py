import subprocess
import os
import time
from urllib.parse import urlparse
import requests

class Arachne:
    def __init__(self, config):
        self.config = config
    
    def fetch_documentation(self, documentation_config):
        if 'url' not in documentation_config or not isinstance(documentation_config['url'], str):
            return
        
        url  = urlparse(documentation_config['url'])
        if all([url.scheme, url.netloc]):
            response = requests.get(documentation_config['url'])
            if response.status_code == 200:
                print('Documentation downloaded successfully')
            else:
                print('Failed to download documentation', response.status_code)
        else:
            print('Invalid URL format')
        
    def validate_file(self, file_path):
        return os.path.isfile(file_path) if file_path is not None else False
    
    def validate_web_file(self, file_path):
        url = urlparse(file_path)
        
        # Check for valid URL scheme and netloc
        if all([url.scheme, url.netloc]):
            return self.validate_file(file_path)
            
        _, ext = os.path.splitext(file_path)
        valid_extensions  = ['.html', '.css', '.js']  
        
        if ext in valid_extensions:
            return True
    
    def start_daemon(self):
        while True:
            try:
                if 'stop_daemon' in self.config and self.config['stop_daemon'] == True:
                    break
                
                if 'documentation' in self.config and isinstance(self.config['documentation'], dict) and 'url' in self.config['documentation']:
                    self.fetch_documentation(self.config['documentation'])
                    self.run_tests()  
            except Exception as e:
                print("An error occurred: ", str(e)) 
            
            time.sleep(60)
    
    def run_tests(self):
        if 'test_command' not in self.config or not isinstance(self.config['test_command'], str):
            return False
        
        retries = self.config.get('retries', 1)    
        for _ in range(retries):
            process  = subprocess.run(self.config['test_command'], shell=True, capture_output=True)
            if process.returncode == 0:
                print('Tests passed successfully')
                return True
        
        print('Failed to run tests', process.returncode)
        print('Output:', process.stdout, process.stderr)
        return False