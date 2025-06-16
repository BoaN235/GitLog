from github import Github

# Authentication is defined via github.Auth
from github import Auth

import configparser
config = configparser.RawConfigParser()
config.read('git.config')
access_token = config.get('AUTH', 'github-access-token')

class user:
    def __init__(self, access_token):
        self.access_token = access_token
        self.repos = []
        

    def get_repos(self):
        # using an access token
        auth = Auth.Token(self.access_token)

        # First create a Github instance:

        # Public Web Github
        g = Github(auth=auth)
        self.repos = []
        # Then play with your Github objects:
        for repo in g.get_user().get_repos():
            r = repository(repo)
            self.repos.append(r)

        # To close connections after use
        g.close()

class repository:
    def __init__(self, repo):
        self.repo = repo
        self.name = repo.full_name

u = user(access_token)
u.get_repos()

for repo in u.repos:
    print(repo.name)