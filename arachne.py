import subprocess
import os
import time
from urllib.parse import urlparse

class Arachne:
    def __init__(self, config):
        self.config = config

    # ... other methods are omitted for brevity ...
        
    def start_daemon(self):
        while True:
            if 'documentation' in self.config and isinstance(self.config['documentation'], dict) and 'url' in self.config['documentation']:
                self.fetch_documentation(self.config['documentation'])
            time.sleep(60)