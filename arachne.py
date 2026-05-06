from urllib.parse import urlparse
import os
import subprocess
import hashlib
import time

class Arachne:
    def __init__(self, config):
        self.config = config
    
    def validate_url(self, url):
        parsed_url = urlparse(url)
        return all([parsed_url.scheme in ['http', 'https'], parsed_url.netloc])
    
    def validate_web_file(self, file_path):
        if self.validate_url(file_path):
            _, ext = os.path.splitext(file_path)
            valid_extensions = ['.html', '.css', '.js']  
            
            if ext in valid_extensions:
                return True
        return False
    
    def is_valid_web_file(self, file_path):
        return self.validate_web_file(file_path)
    
    def run_test_command(self, test_command):
        for _ in range(3):  
            result = subprocess.run(test_command, shell=True)
            
            if result.returncode == 0:
                return True
        
        return False 
    
    def handle_config_test_command(self):
        for _ in range(3):  
            result = self.run_tests() 
            if result == True:
                break
                
        if result != True:
            print("Test command failed after 3 attempts.")
    
    def run_daemon(self):
        while True:
            self.handle_config_test_command()
            time.sleep(5)  # Wait for 5 seconds before next call
    
    def run_tests(self):
        return self.run_test_command(self.config['test_command'])
    
    def fetch_documentation(self, url_dict):
        if 'url' in url_dict:
            if self.validate_url(url_dict['url']):
                _, file_ext = os.path.splitext(urlparse(url_dict['url']).path)
                
                if not file_ext or file_ext == '.':  # Checking if there is no extension or the file has no extension
                    url_hash = hashlib.md5(url_dict['url'].encode('utf-8')).hexdigest() 
                    file_name = f"{url_hash}.html"  
                else:
                    _, file_name = os.path.split(urlparse(url_dict['url']).path) 
                
                command = f"curl {url_dict['url']} > {file_name}"
                subprocess.run(command, shell=True)