import subprocess

class Arachne:
    # ...
    def run_tests(self):
        test_command = self.config['test_command']
        print(f"Running tests with command: {test_command}")
        result = subprocess.run(test_command, shell=True)
        return result.returncode == 0