#!/usr/bin/env python3
"""
Arachne - Web Development Specialist Agent
"""

import sys, json, time, subprocess, re
from pathlib import Path
import ollama
from git_manager import GitManager

MODEL = "deepseek-coder:6.7b-instruct-q4_K_M"

class Arachne:
    def __init__(self, config_path="arachne_config.json", tasks_path="arachne_tasks.txt"):
        self.config_path = config_path
        self.tasks_path = tasks_path
        self.config = self.load_config()
        self.repo = self.config["repo"]
        self.workspace = Path("./arachne_workspace") / self.repo.replace("/", "_")
        self.git = None

    def load_config(self):
        with open(self.config_path) as f:
            return json.load(f)

    def validate_config(self):
        if 'test_command' not in self.config or not isinstance(self.config['test_command'], str):
            return False
        if 'retries' not in self.config or not isinstance(self.config['retries'], int) or self.config['retries'] < 1:
            return False
        if 'url' not in self.config or not (isinstance(self.config['url'], str) and self.config['url'].startswith('http')):
            return False
        return True

    def load_tasks(self):
        if not Path(self.tasks_path).exists():
            return []
        with open(self.tasks_path) as f:
            return [line.strip() for line in f if line.strip()]

    def remove_task(self, task):
        tasks = self.load_tasks()
        if task in tasks:
            tasks.remove(task)
            with open(self.tasks_path, "w") as f:
                for t in tasks:
                    f.write(t + "\n")

    def clone_or_pull_repo(self):
        if not (self.workspace / ".git").exists():
            print(f"Cloning {self.repo}...")
            clone_url = f"https://github.com/{self.repo}"
            subprocess.run(["git", "clone", clone_url, str(self.workspace)], check=False)
        self.git = GitManager(self.workspace)
        self.git.run_git(["fetch", "origin"])
        self.git.run_git(["checkout", "main"])
        self.git.run_git(["pull", "origin", "main"])

    def suggest_files(self, task):
        tree_result = subprocess.run(
            ["find", ".", "-type", "f", "-not", "-path", "./.git/*"],
            cwd=self.workspace, capture_output=True, text=True
        )
        tree = tree_result.stdout[:4000]
        prompt = (
            f"Project file tree:\n{tree}\n\n"
            f"Task: {task}\n\n"
            "Return ONLY a Python list of relative file paths to edit (e.g., ['index.html', 'style.css']). No other text."
        )
        response = ollama.chat(model=MODEL, messages=[{"role":"user","content":prompt}])
        raw = response['message']['content']
        try:
            import ast
            files = ast.literal_eval(raw.split("```")[0].strip())
            if isinstance(files, list):
                return [f for f in files if isinstance(f, str)]
        except:
            pass
        matches = re.findall(r'[\w\-/]+\.\w+', raw)
        return matches[:5]

    def generate_code(self, file_path, current_code, task, error_feedback=None):
        prompt = (
            f"File: {file_path}\n\n"
            f"Current content:\n```\n{current_code}\n```\n\n"
            f"Task: {task}\n"
        )
        if error_feedback:
            prompt += f"\nPrevious attempt error:\n{error_feedback}\nPlease fix."
        messages = [
            {"role":"system","content":"You are a web developer. Output only the complete new file content, no explanations."},
            {"role":"user","content": prompt}
        ]
        response = ollama.chat(model=MODEL, messages=messages)
        code = response['message']['content']
        if "```" in code:
            code = re.sub(r'```\w*\n?', '', code).replace('```', '')
        return code.strip()

    def process_task(self, task):
        match = re.match(r'@file:\s*(\S+)', task)
        if not match:
            print("No @file: directive, skipping.")
            return False
        file_to_edit = match.group(1)
        clean_task = task[len(match.group(0)):].strip()

        files_to_edit = self.suggest_files(clean_task)
        if file_to_edit not in files_to_edit:
            files_to_edit.append(file_to_edit)

        for f in files_to_edit:
            path = self.workspace / f
            current = path.read_text() if path.exists() else ""
            new_code = self.generate_code(f, current, clean_task)
            if new_code:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(new_code)
                print(f"Updated {f}")

        self.git.run_git(["add", "."])
        self.git.run_git(["commit", "-m", f"arachne: {clean_task[:80]}"])
        branch = f"arachne/task-{re.sub(r'[^a-z0-9]','-', clean_task.lower())[:20]}-{abs(hash(clean_task)) % 10000:04d}"
        self.git.run_git(["checkout", "-B", branch])
        self.git.push_to_github("origin", branch)

        subprocess.run([
            "gh", "pr", "create",
            "--repo", self.repo,
            "--title", clean_task[:80],
            "--body", "Automated by Arachne",
            "--head", branch
        ])
        return True

    def run(self):
        tasks = self.load_tasks()
        if not tasks:
            print("No tasks.")
            return
        self.clone_or_pull_repo()
        task = tasks[0]
        print(f"Processing: {task}")
        self.process_task(task)
        self.remove_task(task)

    def daemon(self):
        print("🕸️ Arachne – Web Specialist (daemon mode)")
        while True:
            tasks = self.load_tasks()
            if tasks:
                self.clone_or_pull_repo()
                for task in tasks[:1]:
                    print(f"Processing: {task}")
                    self.process_task(task)
                    self.remove_task(task)
            time.sleep(60)

if __name__ == "__main__":
    agent = Arachne()
    if "daemon" in sys.argv:
        agent.daemon()
    else:
        agent.run()
