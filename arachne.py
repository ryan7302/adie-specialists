import subprocess
import os

def validate_config(self):
    if 'daemon_interval' not in self.config or (isinstance(self.config['daemon_interval'], int) and self.config['daemon_interval'] > 0):
        return False
    
    if ('test_command' not in self.config or not isinstance(self.config['test_command'], str)) or \
       ('retries' not in self.config or not isinstance(self.config['retries'], int) or self.config['retries'] < 1):
        return False
    
    if 'retries' in self.config and (not isinstance(self.config['test_command'], str) or len(self.config['test_command'].strip()) == 0):
        return False
        
    if 'test_command' in self.config and (not isinstance(self.config['retries'], int) or not 1 <= self.config['retries'] <= 10):
        return False
    
    return True

def run_tests(self):
    for _ in range(self.config['retries']):
        process = subprocess.run(self.config['test_command'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if process.returncode == 0:
            return True
    return False

def validate_file(self, filename):
    valid_extensions = ['.html', '.css', '.js']
    _, ext = os.path.splitext(filename)
    if ext in valid_extensions:
        return True
    else:
        return False

def fetch_documentation(self, url):
    command = 'curl -o documentation.html {}'.format(url)
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process.returncode == 0