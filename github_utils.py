import os
import subprocess
from datetime import datetime

GITHUB_REPO_URL = "https://github.com/comus3/league_of_legends_dataset.git"
REPO_DIR = "league_of_legends_dataset"

def set_github_token(token: str):
    """Store token securely in the environment for later use."""
    os.environ["GITHUB_PAT"] = token

def ensure_git_repo():
    """Ensure the repo has been cloned locally."""
    if not os.path.exists(REPO_DIR):
        print("Cloning dataset repo...")
        subprocess.run(["git", "clone", GITHUB_REPO_URL])
    else:
        print("Repo already exists.")

def create_branch_and_commit_changes(branch_prefix="ai-autosave"):
    """Create a new branch, add and commit CSV changes."""
    github_pat = os.getenv("GITHUB_PAT")
    if not github_pat:
        raise ValueError("GitHub PAT not set. Use set_github_token(token) first.")

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    branch_name = f"{branch_prefix}-{timestamp}"
    remote_url = f"https://{github_pat}@github.com/comus3/league_of_legends_dataset.git"

    # Move into the repo
    cwd = os.getcwd()
    os.chdir(REPO_DIR)

    subprocess.run(["git", "checkout", "-b", branch_name])
    subprocess.run(["git", "add", "*.csv"])
    subprocess.run(["git", "commit", "-m", f"Dataset auto-update {timestamp}"])
    subprocess.run(["git", "push", remote_url, branch_name])

    os.chdir(cwd)
    print(f"Changes committed and pushed to branch '{branch_name}'")

def reset_local_repo():
    """Reset repo to clean state (useful for testing)."""
    os.chdir(REPO_DIR)
    subprocess.run(["git", "reset", "--hard"])
    subprocess.run(["git", "clean", "-fd"])
    subprocess.run(["git", "checkout", "main"])
    subprocess.run(["git", "pull"])
    os.chdir("..")
