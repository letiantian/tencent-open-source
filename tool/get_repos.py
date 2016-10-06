# coding: utf-8
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

BASE_URL = 'https://api.github.com'

# get username or org name from command line
if len(sys.argv) < 2:
    print 'error, you should give the name!'
    sys.exit(0)

# get repos from github api
r = requests.get(BASE_URL + '/users/'+sys.argv[1]+'/repos')
repos = json.loads( r.text )

if len(repos) == 0:
    print 'no repos'
    sys.exit(0)

# remove forked projects
repos = [repo for repo in repos if not repo['fork']]

if len(repos) == 0:
    print 'no non-forked repos'
    sys.exit(0)

# sort by stars
repos = sorted(repos, key=lambda repo: repo['watchers'], reverse=True)

# print
for repo in repos:
    name = repo.get('name')
    url = repo.get('html_url')
    desc = repo.get('description', 'No description.')
    if desc is None:
        desc = ''
    print '* [{}]({}) {}'.format(name, url, desc).decode('utf-8')
