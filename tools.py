from config import *
import urllib.request
import json
import requests
from requests.auth import HTTPBasicAuth


suffix = "?access_token=c024106aa6c245aa520b26d8c5d0f27e508ce1ae" # temp auth token

def get_url(source,type,user):
    if source == GITHUB:
        if type == REPOS:
            return GITHUB_API_HOME + user + '/repos' + suffix     
        elif type == FOLLOWER:
            return GITHUB_API_HOME + user + suffix      
        elif type == STARS_GIVEN:
            return GITHUB_API_HOME + user + '/starred' + suffix
        else:
            raise Exception("type is not defined")     
    elif source == BITBUCKET:
        if type == REPOS:
            return BITBUCKET_HOME + user
        else:
            raise Exception("type is not defined")
    else:
        raise Exception("source is not defined")


class GitHubProfileGenerator(object):
    def __init__(self):
        self.repos = []
        self.init_repo = False
        self.language = []
        self.topics = []
        self.commits = 0
        self.star_given_count = 0           
        
    def get_repos(self, user="", link =""):
        """ Get all repos array """
        try:
            if link == "":
                url = get_url(GITHUB,REPOS,user)
            else:
                url = link
            myResponse = requests.get(url)
            if (myResponse.ok):
                self.repos.extend(json.loads(myResponse.content))
                link = myResponse.headers.get('link')
                if link is None:
                    return
                else:
                    next_url = self._find_next(link)
                    if next_url is not None:
                        self.get_repos(link=next_url)
                    else:
                        return
            else:
                myResponse.raise_for_status()
        except Exception as e:
            print (e)
  
    def count_profile(self,user):
        """ get tuple for repo_count,open_issue_count,size_count,star_receive_count"""
        try:
            repo_count = 0
            open_issue_count = 0
            size_count = 0
            #star received
            watcher_count = 0
            if not self.init_repo:
                self.get_repos(user)
                self.init_repo = True
            if len(self.repos) != 0:
                for repo in self.repos:
                    if repo['fork'] is True:
                        # skip it, only counting folk == False
                        continue
                    
                    repo_count +=1
                    open_issue_count += repo['open_issues_count']
                    size_count += repo['size']
                    watcher_count += repo['stargazers_count']
                    self.language.append(repo['language'])
                    # Skip if did not find topic
                    try:
                        self.topics.append(repo['topics'] if repo['topic'] is not None else [] )
                    except:
                        pass        
                self.language = [(l,self.language.count(l)) for l in set(self.language)]
                if self.topics != []:
                    self.topics = [(t,self.topics.count(t)) for t in set(self.topics)]
            return (repo_count,open_issue_count,size_count,watcher_count)
        except Exception as e:
            print (e)
        
  
    def count_follower(self,user):
        """ Get total watcher/follower count """
        try:
            repo_url = get_url(GITHUB,FOLLOWER,user)
        
            myResponse = requests.get(repo_url)
            if (myResponse.ok):
                profile = json.loads(myResponse.content)
                return profile['followers']
            else:
                myResponse.raise_for_status()
        except Exception as e:
            print (e)

    
    """
    users/:usename/starred
    """
    def count_star_given(self,user='',link=''):
        try:
            star_given_count = 0
            if link == '':
                url = get_url(GITHUB,STARS_GIVEN,user)
            else:
                url = link
            myResponse = requests.get(url)
            if (myResponse.ok):
                profile = json.loads(myResponse.content)
                self.star_given_count += len(profile)
                link = myResponse.headers.get('link')
                if link is None:
                    return
                else:
                    next_url = self._find_next(link)
                    if next_url is not None:
                        self.count_star_given(link=next_url)
                    else:
                        return
            else:
                myResponse.raise_for_status()             
        except Exception as e:
            print (e)


    def count_commits(self,user):
        try:
            if not self.init_repo:
                self.get_repos(user)
                self.init_repo = True
            for repo in self.repos:
                if repo['fork'] is True:
                    # skip it, only counting folk == True
                    continue
                self._count_repo_commits(repo['url'] + '/commits')
            return self.commits
        except Exception as e:
            print (e)

    def _count_repo_commits(self, url ):
        myResponse = requests.get(url)
        if (myResponse.ok):
            resouces = json.loads(myResponse.content)
            n = len(resouces)
            if n == 0:
                return
            self.commits += n
            link = myResponse.headers.get('link')
            if link is None:
                return
            else:
                next_url = self._find_next(myResponse.headers['link'])
                if next_url is None:
                    return
                else: 
                    self._count_repo_commits(next_url)
        else:
            myResponse.raise_for_status() 

    def _find_next(self,link):
        """find next url link from response header link"""
        for l in link.split(','):
            a, b = l.split(';')
            if b.strip() == 'rel="next"':
                return a.strip()[1:-1]
                
class BitBucketProfileGenerator(object):
    def __init__(self):
        self.repos = []
        self.language = []
        self.topics = []
        self.repo_count = 0
        self.open_issue_count = 0
        self.size_count = 0
        self.watcher_count = 0
        self.follower_count = 0
        self.star_given_count = 0
            
    def count_repo_count(self,user):
        url = get_url(BITBUCKET,REPOS,user)
        myResponse = requests.get(url)
        if (myResponse.ok):
            profile = json.loads(myResponse.content)
            return profile['size']
        else:
            myResponse.raise_for_status()
            
    def count_openissue_count(self,user):
        # doing query
        return self.open_issue_count
        
    def count_size(self,user):
        # doing query
        return self.size_count
        
    def count_star_received(self,user):
        # doing query
        return self.watcher_count
        
    def count_follower(self,user):
        # doing query
        return self.follower_count
        
    def count_star_given(self,user):
        # doing query
        return self.star_given_count

if __name__ == '__main__':
    pass

    
    
    
    
    