#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request
import time

app = Flask(__name__)
from tools import *


def get_github_profile_user(username):
    ghpg = GitHubProfileGenerator()
    repo_count,open_issue_count,size_count,watcher_count = ghpg.count_profile(username)
    follower_count = ghpg.count_follower(username)
    ghpg.count_star_given(username)
    dict = {}
    dict['username']= username
    dict['repo_count'] = repo_count
    dict['open_issue_count'] = open_issue_count
    dict['size_count'] = size_count
    dict['follower_count'] = follower_count
    dict['star_received_count'] = watcher_count
    dict['star_given_count'] = ghpg.star_given_count
    dict['language'] = ghpg.language
    dict['topic'] = ghpg.topics
    dict["queried_on"] = time.asctime(time.localtime(time.time()) )
    return dict
    
def get_bitbucket_profile_user(username):
    bbpg = BitBucketProfileGenerator()
    repo_count = bbpg.count_repo_count(username)
    open_issue_count = bbpg.count_openissue_count(username)
    size_count = bbpg.count_size(username)
    watcher_count = bbpg.count_star_received(username)
    follower_count = bbpg.count_follower(username)
    star_given_count = bbpg.count_star_given(username)
    dict = {}
    dict['username']= username
    dict['repo_count'] = repo_count
    dict['open_issue_count'] = open_issue_count
    dict['size_count'] = size_count
    dict['follower_count'] = follower_count
    dict['star_received_count'] = watcher_count
    dict['star_given_count'] = star_given_count
    dict['language'] = bbpg.language
    dict['topic'] = bbpg.topics
    dict["queried_on"] = time.time()
    return dict

@app.route('/api/v1.0/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/api/v1.0/users/<string:username>', methods=['GET'])
def get_task(username):
    args = request.args
    args = dict(args)
    
    merged_dict = {}
    github_user_profile = get_github_profile_user(username)
    bitbucket_user_profile = get_bitbucket_profile_user(username)
    for key in github_user_profile:
        if key == "queried_on" or "username":
            merged_dict[key] = github_user_profile[key]
        else:
            merged_dict[key] = github_user_profile[key] + bitbucket_user_profile[key]

    s1 = 0
    s2 = 0
    if 's1' in args:
        print ("step here")
        s1 = args['s1']
    if 's2' in args:
        s2 = args['s2']
        
    if s1 == 'github' and s2 == 'bitbucket':
        pass # we will pass merged dict
    elif s1 == 0 and s2 == 0:
        pass # still pass merged dict
    elif s1 == 'github' and s2 == 0:
        merged_dict = github_user_profile
    elif s1 == 0 and s2 == 'butbucket':
        merged_dict = bitbucket_user_profile
    else:
        pass # still pass merged dict
       
    if len(merged_dict) == 0:
        abort(404)
    return jsonify({'users': merged_dict})
    
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)