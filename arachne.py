import os
import json
from llama import Llama
from git_manager import GitManager
import sys  # added import statement for sys module

class Arachne:
    def __init__(self):
        self.tasks = []
        self.config = {}
        self.llama = Llama(model='deepseek-coder:6.7b-instruct-q4_K_M')  # initialize llama with the correct model
        self.git_manager = GitManager()
        
    def load_tasks(self, file_name='arachne_tasks.txt'):
        with open(file_name) as f:
            self.tasks = [line.rstrip('\n') for line in f]
            
    def load_config(self, file_name='arachne_config.json'):
        with open(file_name) as f:
            self.config = json.load(f)
            
    def run(self):
        for task in self.tasks:
            files_to_edit = self.llama.ask(task)  # ask LLM which files to edit
            new_content = self.llama.generate_code(task, files_to_edit)  # generate new content using the LLM
            
            for file in files_to_edit:
                if file.endswith('.html') or file.endswith('.css') or file.endswith('.js'):
                    self.git_manager.edit_file(file, new_content)  # edit the file with new content
            
            test_command = 'test command'  # get the test command (replace with actual implementation)
            os.system(test_command)  # run the test command
        
            branch_name = f"arachne/task-{task}"
            
            self.git_manager.create_branch(branch_name)  # create a new branch
            self.git_manager.commit('Update files')  # commit changes to this branch
            
            self.git_manager.push()  # push the changes
        
        pull_request = 'open PR command'  # get the command to open a pull request (replace with actual implementation)
        os.system(pull_request)  # run the command to open a pull request
    
    def daemon(self):
        while True:
            self.run()
            
if __name__ == "__main__":
    arachne = Arachne()
    arachne.load_tasks()
    arachne.load_config()
    
    print("\n\U0001F573" * 2 + "\nArachne is running!\n" + "\U0001F573" * 2)
    
    if 'daemon' in sys.argv:
        arachne.daemon()