'''src/traffic_monitor/fetcher.py

GitHubFetcher: handles communication with GitHub API to retrieve traffic stats.
Uses PyGithub under the hood.
'''
import logging
from github import Github, GithubException
from typing import List, Dict, Optional

class GitHubFetcher:
    """
    Fetch traffic metrics (views & clones) for all repos in a user or organization.
    """
    def __init__(self, token: str, org: Optional[str] = None):
        self.token = token
        self.org = org
        self.client = Github(self.token)
        self.logger = logging.getLogger(__name__)

    def _get_account(self):
        try:
            if self.org:
                self.logger.debug(f"Fetching organization: {self.org}")
                return self.client.get_organization(self.org)
            else:
                self.logger.debug("Fetching authenticated user account")
                return self.client.get_user()
        except GithubException as e:
            self.logger.error(f"Error fetching account '{self.org or 'user'}': {e}")
            raise

    def fetch_all(self) -> List[Dict[str, int]]:
        """
        Fetch traffic stats for every repository under the account.
        Returns a list of dicts with keys: name, views_count, views_uniques, clones_count, clones_uniques
        """
        account = self._get_account()
        stats = []
        for repo in account.get_repos():
            data = self._fetch_repo(repo.full_name)
            if data:
                stats.append(data)
        self.logger.info(f"Fetched traffic for {len(stats)} repos")
        return stats

    def _fetch_repo(self, full_name: str) -> Optional[Dict[str, int]]:
        """
        Fetch traffic stats for a single repository by full name (e.g. 'user/repo').
        """
        try:
            repo = self.client.get_repo(full_name)
            views = repo.get_views_traffic()
            clones = repo.get_clones_traffic()
            return {
                'name': repo.full_name,
                'views_count': views.count,
                'views_uniques': views.uniques,
                'clones_count': clones.count,
                'clones_uniques': clones.uniques,
            }
        except GithubException as e:
            self.logger.warning(f"Unable to fetch traffic for {full_name}: {e}")
            return None
