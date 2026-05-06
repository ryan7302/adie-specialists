from urllib.parse import urlparse
import os

def validate_web_file(self, file_path):
    url = urlparse(file_path)
    
    # Check for valid URL scheme and netloc
    if all([url.scheme in ['http', 'https'], url.netloc]):
        _, ext = os.path.splitext(file_path)
        valid_extensions = ['.html', '.css', '.js']  
        
        if ext in valid_extensions:
            return True