import sys
import os
import json
from subprocess import Popen, PIPE


def is_git_directory(root):
    if os.path.isfile(root):
        return False

    return ".git" in os.listdir(root)


def git_status():
    return Popen(["git", "status"], stdout=PIPE).communicate()[0].decode("utf-8")


def collect_git_statuses(root):
    result = {
        "git": {},
        "notgit": []
    }

    if is_git_directory(root):
        print("Root is a git directory")
        return

    folders = os.listdir(root)

    for folder in folders:
        path = os.path.join(root, folder)
        if is_git_directory(path):
            os.chdir(path)
            result["git"][path] = git_status()
        else:
            result["notgit"].append(path)

    return result

root = os.getcwd()

if len(sys.argv) > 1:
    root = sys.argv[1]

all_folders = collect_git_statuses(root)

repos = all_folders["git"]
not_repos = all_folders["notgit"]

repos = [r for r in repos if "nothing to commit" not in repos[r]]
print("Git repos with git status: {}".format(len(repos)))
for repo in repos:
    print(repo)

print("Not git repos: {}".format(len(not_repos)))
for folder in not_repos:
    print(folder)
