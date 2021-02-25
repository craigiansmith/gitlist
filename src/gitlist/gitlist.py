#!/usr/bin/env python3

# Gitlist will walk the directory tree from the current directory, looking for
# git repos. It will report back repos with untracked files, uncommitted 
# changes.

import subprocess
import os

class NotReadyError(Exception):
    pass

class GitList:
    def ready(self):
        # Assert preconditions: git installed
        result = subprocess.run(['which', 'git'], capture_output=True, text=True)
        if 'git' in result.stdout:
            return True
        else:
            raise NotReadyError("Git is not installed")

    def find(self, start_directory):
        found = False
        for directory, subdirs, files in os.walk(start_directory):
            if '.git' in subdirs or '.git' in files:
                found = True
                print("{d}/ is a git repo".format(d=directory))
                if self.uncommitted_change(directory):
                    print(' -- with uncommitted changes')
                if self.unpushed_changes(directory):
                    print(' -- with unpushed local changes')

        return found

    def uncommitted_change(self, directory):
        cwd = os.getcwd()
        os.chdir(directory)
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        os.chdir(cwd)
        if 'modified' in result.stdout or 'untracked' in result.stdout:
            return True
        else:
            return False

    def unpushed_changes(self, directory):
        cwd = os.getcwd()
        os.chdir(directory)
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        os.chdir(cwd)
        if 'ahead' in result.stdout:
            return True
        else:
            return False

if __name__ == "__main__":
    import sys
    try:
        directory = sys.argv[1]
    except IndexError:
        directory = '.'
    gl = GitList()
    gl.ready()
    gl.find(directory)
