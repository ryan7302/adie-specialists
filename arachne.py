def run_tests(self):
    test_cmd = self.config['test_command']
    result = subprocess.run(test_cmd, shell=True)
    return result.returncode == 0