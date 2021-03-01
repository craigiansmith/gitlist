from src.gitlist.gitlist import GitList, Display
from pathlib import Path
import os
import subprocess


def test_git_installed():
    # When run, gitlist should fail if git isn't installed
    gl = GitList()
    assert gl.ready()


def test_find_git_repos():
    gl = GitList()
    BASE_DIR = Path("tests", "fixtures", "repos")
    assert gl.find(BASE_DIR)


def test_are_there_untracked_changes():
    gl = GitList()
    TARGET_DIR = Path("tests", "fixtures", "repos", "second")
    TARGET_FILE = Path(TARGET_DIR, "index.html")
    original_filetext = ""
    with open(TARGET_FILE, "r") as f:
        original_filetext = f.read()
    with open(TARGET_FILE, "a") as f:
        f.write("new change\n")
    assert gl.uncommitted_change(TARGET_DIR)
    with open(TARGET_FILE, "w") as f:
        f.write(original_filetext)


def test_there_are_no_unommitted_changes():
    gl = GitList()
    TARGET_DIR = Path("tests", "fixtures", "repos", "first")
    assert not gl.uncommitted_change(TARGET_DIR)


def test_are_there_local_unpushed_changes():
    gl = GitList()
    TARGET_DIR = Path("tests", "fixtures", "repos", "first")
    if remote_not_configured(TARGET_DIR):
        configure_remote_tracking_repo(TARGET_DIR)
    assert gl.unpushed_changes(TARGET_DIR)


def remote_not_configured(directory):
    cwd = os.getcwd()
    os.chdir(directory)
    result = (
        "ahead"
        in subprocess.run(
            ["git", "branch", "-vv"], capture_output=True, text=True
        ).stdout
    )
    os.chdir(cwd)
    return not result


def configure_remote_tracking_repo(directory):
    cwd = os.getcwd()
    os.chdir(directory)
    subprocess.run(
        [
            "git",
            "remote",
            "add",
            "upstream",
            "git@github.com:craigiansmith/gitlist_test_repo_4.git",
        ]
    )
    subprocess.run(["git", "fetch", "upstream"])
    subprocess.run(["git", "checkout", "master"])
    subprocess.run(["git", "branch", "-u", "upstream/master"])
    os.chdir(cwd)


def test_there_are_no_unpushed_changes():
    gl = GitList()
    TARGET_DIR = Path("tests", "fixtures", "repos", "second")
    assert not gl.unpushed_changes(TARGET_DIR)


def test_initialise_display():
    display = Display("console")


def test_start_a_message():
    display = Display("console")
    s = "This is the start of the message"
    display.msg(s, 1)
    assert s in display.flush()


def test_add_to_a_msg():
    display = Display("console")
    s = "Start message"
    s2 = "-- continue message"
    s3 = "-- continue further"
    display.msg(s, 1)
    display.msg(s2, 2)
    display.msg(s3, 3)
    output = display.flush()
    assert s in output
    assert s2 in output
    assert s3 in output
