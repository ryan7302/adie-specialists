from urllib.parse import urlparse
import os
import subprocess

class Arachne:
    def __init__(self, config):
        self.config = config
        
    def validate_web_file(self, file_path):
        url = urlparse(file_path)
        
        if all([url.scheme in ['http', 'https'], url.netloc]):
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
            
    def run_tests(self):
        return self.run_test_command(self.config['test_command'])