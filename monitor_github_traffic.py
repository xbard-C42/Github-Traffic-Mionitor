'''
monitor_github_traffic.py

A simple Python script to fetch and display traffic statistics (views, unique views, clones, unique clones)
for all repositories in a given GitHub account (user or organization), without having to navigate to the GitHub Traffic page.

Prerequisites:
  - Python 3.7+
  - PyGithub (`pip install PyGithub`)
  - A GitHub personal access token (PAT) with `repo` or `public_repo` scope, set in environment variable `GITHUB_TOKEN`.

Usage:
  1. Export your token:
       export GITHUB_TOKEN="your_personal_access_token"
  2. (Optional) To target an organization instead of your user account, edit the script’s `TARGET_ORG`.
  3. Run:
       python monitor_github_traffic.py

This can be scheduled via cron or any scheduler of your choice.
'''  
import os
import sys
from github import Github, GithubException

def fetch_traffic_stats(token, target_org=None):
    g = Github(token)
    try:
        if target_org:
            account = g.get_organization(target_org)
        else:
            account = g.get_user()
    except GithubException as e:
        print(f"Error fetching account: {e}")
        sys.exit(1)

    repos = account.get_repos()
    stats = []
    for repo in repos:
        try:
            views = repo.get_views_traffic()
            clones = repo.get_clones_traffic()
            stats.append({
                'name': repo.full_name,
                'views_count': views['count'],
                'views_uniques': views['uniques'],
                'clones_count': clones['count'],
                'clones_uniques': clones['uniques'],
            })
        except GithubException as e:
            print(f"Error fetching traffic for {repo.full_name}: {e}")
    return stats

if __name__ == '__main__':
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN not set")
        sys.exit(1)

    # To monitor an organization instead, set TARGET_ORG e.g. 'my-org'
    TARGET_ORG = None  # or 'my-org'
    data = fetch_traffic_stats(token, TARGET_ORG)
    print(f"Fetched traffic for {len(data)} repos:\n")
    for d in data:
        print(f"{d['name']}: Views={d['views_count']} ({d['views_uniques']} unique)  Clones={d['clones_count']} ({d['clones_uniques']} unique)")
