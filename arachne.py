import subprocess

class Arachne:
    def __init__(self, config):
        self.config = config

    def validate_file(self, filename):
        valid_extensions = ['.html', '.css', '.js']
        _, extension = os.path.splitext(filename)
        return extension in valid_extensions
        
    def run_tests(self):
        test_command  = self.config['test_command']
        for i in range(3):
            print(f"Running tests with command:  {test_command} (attempt {i+1})")
            result = subprocess.run(test_command, shell=True)
            if result.returncode == 0:
                return True
        return False