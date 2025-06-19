from github import Github
import json
# Authentication is defined via github.Auth
from github import Auth
import requests
import datetime


import configparser
config = configparser.RawConfigParser()
config.read('git.config')
access_token = config.get('AUTH', 'github-access-token')

class user:
    def __init__(self, access_token):
        self.access_token = access_token
        self.repos = {}

    def access_github(self):
        # using an access token
        auth = Auth.Token(self.access_token)

        # First create a Github instance:
        # Public Web Github
        self.g = Github(auth=auth)
        self.user = self.g.get_user()
        updata_data = input("update data[Y/N]")
        if updata_data == "Y":
            self.serialize_data()
        self.update_log()
        # To close connections after use
        self.g.close()


    def serialize_data(self):
        data = []
        for repo in self.user.get_repos():
            data.append(str(repo.full_name))
        with open('data.json', 'w') as f:
            json.dump(data, f, sort_keys=True)

            

    def update_log(self):
        self.current_repo = ""
        with open('data.json', 'r') as f:
            data = json.load(f)
        for repo_name in data:
            if repo_name == "BoaN235/gitloggertest":
                l = log()
                current_repo = self.g.get_repo(str(repo_name))
                r = repository(current_repo)
                r.add_log(l)

class repository:
    def __init__(self, repo):
        self.repo = repo
        self.name = repo.full_name
        self.contents = self.repo.get_contents("")

    def add_log(self, log):
        Has_Log_File = False
        log = "\n\n### " + str(log.title) + " -- "  + str(log.date) + "\n\n" + str(log.value)
        for content in self.contents:
            org_content = content.decoded_content.decode()
            if content.path == "LOG.MD":
                msg = str(org_content) + log
                self.repo.update_file(content.path, "updated LOG.MD file", msg , content.sha) 
                Has_Log_File = True
        if Has_Log_File == False:
            msg = "# Log\n\n## created with [GitLog](https://github.com/BoaN235/GitLog)" + log
            self.repo.create_file("LOG.MD", "added LOG.MD file", msg)
        print("Completed Log")
        return
        

class log:
    def __init__(self):
        self.date = datetime.datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")
        self.title = input("input title:\n")
        self.value = input("input log:\n")


u = user(access_token)

u.access_github()
