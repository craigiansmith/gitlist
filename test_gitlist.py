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

def test_are_there_untracked_changes():
    gl = GitList()
    TARGET_DIR = Path('tests', 'fixtures', 'repos', 'second')
    TARGET_FILE = Path(TARGET_DIR, 'index.html')
    original_filetext = ''
    with open(TARGET_FILE, 'r') as f:
        original_filetext = f.read()
    with open(TARGET_FILE, 'a') as f:
        f.write('new change\n')
    assert gl.uncommitted_change(TARGET_DIR)
    with open(TARGET_FILE, 'w') as f:
        f.write(original_filetext)

def test_there_are_no_unommitted_changes():
    gl = GitList()
    TARGET_DIR = Path('tests', 'fixtures', 'repos', 'first')
    assert not gl.uncommitted_change(TARGET_DIR)

def test_are_there_local_unpushed_changes():
    gl = GitList()
    TARGET_DIR = Path('tests', 'fixtures', 'repos', 'first')
    assert gl.unpushed_changes(TARGET_DIR)

def test_there_are_no_unpushed_changes():
    gl = GitList()
    TARGET_DIR = Path('tests', 'fixtures', 'repos', 'second')
    assert not gl.unpushed_changes(TARGET_DIR)

