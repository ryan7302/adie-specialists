from urllib.parse import urlparse
import os
import subprocess

class Arachne:
    def __init__(self, config):
        self.config = config
        self.handle_config_test_command()   # Initiate test command handling
    
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
        for _ in range(3):   # Attempt running the command up to 3 times
            result = subprocess.run(test_command, shell=True)
            
            if result.returncode == 0:
                return True
        
        return False   # Command failed after three attempts
    
    def handle_config_test_command(self):
        self.run_tests()   # Retry the test command up to 3 times if it fails
    
    def run_tests(self):
        return self.run_test_command(self.config['test_command'])
    
    def fetch_documentation(self, url):
        file_name = 'documentation.html'
        command = f"curl {url} > {file_name}"
        subprocess.run(command, shell=True)