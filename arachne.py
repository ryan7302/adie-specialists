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
        return bool(parsed_url.scheme and parsed_url.netloc)
        
    # Method to check if a file has valid web extension 
    def validate_web_file(self, file_name):
        _, file_ext = os.path.splitext(file_name)
        return bool((file_ext == '.html') or (file_ext == '.css') or (file_ext == '.js'))
        
    def fetch_documentation(self, url_dict):
        if 'url' in url_dict:
            if self.validate_url(url_dict['url']):
                _, file_ext = os.path.splitext(urlparse(url_dict['url']).path)
                
                if not file_ext or file_ext == '.':  
                    url_hash = hashlib.md5(url_dict['url'].encode('utf-8')).hexdigest() 
                    file_name = f"{url_hash}.html"  
                else:
                    _, file_name = os.path.split(urlparse(url_dict['url']).path) 
                
                # Check if the fetched file already exists before attempting to save it
                if os.path.exists(file_name):
                    print("The fetched file already exists.")
                    return
                
                command = f"curl {url_dict['url']} > {file_name}"
                subprocess.run(command, shell=True)
                
                if self.validate_web_file(file_name):
                    print("The fetched file is a valid web file.")
                else:
                    os.remove(file_name)          # Remove the file if it's not a valid web file
                    print("The fetched file is not a valid web file and has been removed.")
    
    def run_tests(self):
        result = subprocess.run(self.config['test_command'], shell=True)
        return True if result.returncode == 0 else False