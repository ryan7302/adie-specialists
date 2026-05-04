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
        
        url = urlparse(documentation_config['url'])
        if all([url.scheme, url.netloc]):
            response = requests.get(documentation_config['url'])
            if response.status_code == 200:
                print('Documentation downloaded successfully')
            else:
                print('Failed to download documentation', response.status_code)
        else:
            print('Invalid URL format')
        
    def start_daemon(self):
        while True:
            if 'documentation' in self.config and isinstance(self.config['documentation'], dict) and 'url' in self.config['documentation']:
                self.fetch_documentation(self.config['documentation'])
            time.sleep(60)