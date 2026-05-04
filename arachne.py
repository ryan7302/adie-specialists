def run_tests(self):
    test_cmd = self.config.get('test_command', '')
    if not test_cmd:
        print("No testing command found in config.")
        return False
    
    result = subprocess.run(test_cmd, shell=True, capture_output=True)
    if result.returncode == 0:
        return True
    else:
        print('Testing failed:', result.stderr.decode())
        return False

if __name__ == "__main__":
    agent = Arachne()
    if "daemon" in sys.argv:
        agent.daemon()
    elif "test" in sys.argv:  # Add new command to run tests
        print("Running tests...")
        success = agent.run_tests()
        print(f'Tests {"succeeded" if success else "failed"}')
    else:
        agent.run()