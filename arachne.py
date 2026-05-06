#!/usr/bin/env python3
"""
Arachne – Web Development Specialist Agent
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
                    f.write(f"{t}\n")

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
            "Return ONLY a Python list of relative file paths to edit  (e.g., ['index.html', 'style.css']). No other text."
        )
        response = ollama.chat(model=MODEL, messages=[{"role":"user","content":prompt}])
        raw = response['message']['content']
        try:
            import ast
            files = ast.literal_eval(raw.split("