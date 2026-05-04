def run_tests(self):
    test_command = self.config['test_command']
    print("Running tests with command: ", test_command)
    
    try:
        result = subprocess.run(test_command, shell=True, stderr=subprocess.PIPE, check=False)
        
        if result.returncode == 0:
            print("Tests passed.")
            return True
        else:
            print("Tests failed.")
            print(result.stderr.decode())
            return False
    except Exception as e:
        print("Error running tests: ", str(e))
        return False