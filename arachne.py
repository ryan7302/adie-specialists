import subprocess
import os
import time

class Arachne:
    def __init__(self, config):
        self.config = config

    def validate_file(self, filename):
        valid_extensions = ['.html', '.css', '.js', '.jpg', '.png', '.gif']
        if not os.path.exists(filename):  # Check file existence before extension check
            return False
        _, extension = os.path.splitext(filename)
        return extension in valid_extensions
        
    def run_tests(self):
        test_command = self.config['test_command']
        for i in range(3):
            print(f"Running tests with command:   {test_command}  (attempt  {i+1})")
            result = subprocess.run(test_command, shell=True)
            if result.returncode == 0:
                return True
        return False
    
    def fetch_documentation(self, url):
        command = f"wget -O documentation.html {url}"
        print(f"Fetching documentation with command:   {command}")
        subprocess.run(command, shell=True)
        
    def start_daemon(self):
        while True:
            self.run_tests()
            time.sleep(60)