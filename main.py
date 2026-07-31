import os
from datetime import datetime
from git import Repo, InvalidGitRepositoryError
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_config(task):

    if task.host.platform == "linux":
        command = "cat /etc/hostname"
    else:
        command = "show running-config"

    # Fetch configuration via Netmiko
    result = task.run(task=netmiko_send_command, command_string=command)
    config_data = result[0].result

    # Save to backups/hostname.txt
    file_path = os.path.join(BACKUP_DIR, f"{task.host.name}.txt")
    with open(file_path, "w") as f:
        f.write(config_data)

    return f"Saved configuration for {task.host.name}"


def git_commit_backups():

    try:
        repo = Repo(".")
    except InvalidGitRepositoryError:
        print(" Error: Git repository not initialized. Run 'git init' first.")
        return

    # Stage backup directory
    repo.git.add(BACKUP_DIR)

    # Check for staged changes against HEAD
    if repo.head.is_valid() and repo.is_dirty(index=True, working_tree=False):
        print("\n Configuration Drift Detected!")

        # Fetch and print line-by-line diff
        diff_output = repo.git.diff("--cached")
        print("\n--- Differences Found ---")
        print(diff_output)
        print("-" * 30)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_message = f"Auto-backup: Network config backup at {timestamp}"

        repo.index.commit(commit_message)
        print(f"\n Git Commit Created: '{commit_message}'")
    else:
        print("\n No configuration changes detected. Git status clean.")


def main():
    # 1. Initialize Nornir
    nr = InitNornir(config_file="config.yaml")

    print("Running device backups...\n")
    results = nr.run(task=backup_config)

    # 2. Print result summary
    print_result(results)

    # 3. Auto-commit to Git
    print("\n Checking Git repository for changes...")
    git_commit_backups()


if __name__ == "__main__":
    main()