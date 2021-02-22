from gitlist import GitList
from pathlib import Path

def test_git_installed():
    # When run, gitlist should fail if git isn't installed
    gl = GitList()
    assert gl.ready()

def test_find_git_repos():
    gl = GitList()
    BASE_DIR = Path('tests', 'fixtures', 'repos')
    assert gl.find(BASE_DIR)

