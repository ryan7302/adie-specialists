import subprocess

class Arachne:
    def __init__(self, config):
        self.config = config
    
    def run_tests(self):
        command = self.config['test_command']
        result = subprocess.run(command, shell=True)
        return True if result.returncode == 0 else False