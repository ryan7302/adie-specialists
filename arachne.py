import subprocess
import os
import time
import re

class Arachne():
    def __init__(self, config):
        self.config = config
        
    def validate_config(self):
        if 'daemon_interval' not in self.config or (isinstance(self.config['daemon_interval'], int) and self.config['daemon_interval'] > 0):
            raise ValueError("Invalid configuration: ‘daemon_interval’ must be an integer greater than 0")
    
        if 'test_command' not in self.config or not isinstance(self.config['test_command'], str) or \
             'retries' not in self.config or not isinstance(self.config['retries'], int) or self.config['retries'] < 1:
            return False
        
        if 'url' not in self.config or not (isinstance(self.config['url'], str) and (self.config['url'].startswith('http://') or self.config['url'].startswith('https://'))):
            return False
            
        return True
    
    def run_tests(self):
        result = subprocess.run(self.config['test_command'], shell=True)
        if result.returncode == 0:
            return True
        else:
            return False
    
    def validate_file(self, filename):
        return os.path.isfile(filename)
    
    def validate_url(self):
        url = self.config['url']
        if isinstance(url, str) and (url.startswith('http://') or url.startswith('https://')):
            return True
        else:
            return False