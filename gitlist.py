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
        for directory, subdirs, files in os.walk(start_directory):
            if ".git" in subdirs:
                print("{d}/ is a git repo".format(d=directory))

        return True

if __name__ == "__main__":
    import sys
    directory = sys.argv[1]
    gl = GitList()
    gl.ready()
    gl.find(directory)
