class Arachne:
    def __init__(self, config_path="arachne_config.json", tasks_path="arachne_tasks.txt"):
        self.config_path = config_path
        self.tasks_path = tasks_path
        self.config = self.load_config()
        self.repo = self.config["repo"]
        self.workspace = Path("./arachne_workspace") / self.repo.replace("/", "_")
        self.git = None

    #... existing methods here ...

    def run_tests(self):
        test_command = self.config['test_command']
        result = subprocess.run(test_command, shell=True, capture_output=True)
        return result.returncode == 0