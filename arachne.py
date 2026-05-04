def run_tests(self):
    test_command = self.config['test_command']
    result = subprocess.run(test_command, shell=True)
    return result.returncode == 0

if __name__ == "__main__":
    agent = Arachne()
    if "daemon" in sys.argv:
        agent.daemon()
    elif "tests" in sys.argv:
        print(agent.run_tests())
    else:
        agent.run()