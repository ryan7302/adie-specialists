import os
import json
from llama import Llama
from git_manager import GitManager
import sys   
import subprocess

class Arachne:
    def __init__(self):
        self.tasks = []
        self.config = {}
        self.llama = Llama(model='deepseek-coder:6.7b-instruct-q4_K_M')  
        self.git_manager = GitManager()
        
    def load_tasks(self, file_name='arachne_tasks.txt'):
        with open(file_name) as f:
            self.tasks = [line.rstrip('\n') for line in f]
            
    def load_config(self, file_name='arachne_config.json'):
        with open(file_name) as f:
            self.config = json.load(f)
    
    def handle_test_commands(self):
        if 'tests' in self.config:
            for test in self.config['tests']:
                try:
                    subprocess.run(test, shell=True, check=True)
                except subprocess.CalledProcessError as error:
                    print(f"Test command {test} failed with error: {error}")
    
    def run(self):
        for task in self.tasks:
            files_to_edit = self.llama.ask(task)   
            new_content = self.llama.generate_code(task, files_to_edit)   
            
            for file in files_to_edit:
                if file.endswith('.html') or file.endswith('.css') or file.endswith('.js'):
                    self.git_manager.edit_file(file, new_content)  
            
            test_command = 'test command'   
            os.system(test_command) 
        
            branch_name = f"arachne/task-{task}"
            
            self.git_manager.create_branch(branch_name)   
            self.git_manager.commit('Update files')   
            
            self.git_manager.push()   
        
        pull_request = 'open PR command'    
        os.system(pull_request) 
        
        # Added this line to handle test commands
        self.handle_test_commands()   
    
    def daemon(self):
        if len(sys.argv) != 2 or sys.argv[1] != 'daemon':
            print("Usage: python arachne.py daemon")
            return
        
        try:
            while True:
                self.run()
        except Exception as e:
            print("An error occurred: ", str(e))
            
if __name__ == "__main__":
    arachne = Arachne()
    arachne.load_tasks()
    arachne.load_config()
    
    print("\n\U0001F573" * 2 + "\nArachne is running!\n" + "\U0001F573" * 2)
    
    if 'daemon' in sys.argv:
        arachne.daemon()
    else:
        arachne.run()