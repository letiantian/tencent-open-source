# coding: utf-8
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

BASE_URL = 'https://api.github.com'

def get_repos_for_one(name):
    """ get repos by username or org name """
    r = requests.get(BASE_URL + '/users/'+name+'/repos')
    return json.loads( r.text )

def filter_repos_by_stars(repos, min_stars=10):
    """ filter """
    return [repo for repo in repos if repo.get('stargazers_count')>min_stars]

def show_repos_as_list(repos):
    """ print repos as list """
    # remove forked projects
    repos = [repo for repo in repos if not repo.get('fork')]
    if len(repos) == 0:
        print 'no non-forked repos'
        return
    # sort by stars
    repos = sorted(repos, key=lambda repo: repo.get('stargazers_count'), reverse=True)
    for repo in repos:
        name = repo.get('name')
        url = repo.get('html_url')
        desc = repo.get('description', 'No description.')
        if desc is None:
            desc = ''
        desc = desc.strip().replace('\n', '').replace('\r', '')
        print '* [{}]({}) {}'.format(name, url, desc).decode('utf-8')

def show_repos_as_table(repos):
    """ print repos as table """
    # remove forked projects
    repos = [repo for repo in repos if not repo.get('fork')]
    if len(repos) == 0:
        print 'no non-forked repos'
        return
    # sort by stars
    repos = sorted(repos, key=lambda repo: repo.get('stargazers_count'), reverse=True)
    print '|Name|Star|Language|Description|'
    print '|----|----|--------|-----------|'
    for repo in repos:
        name = repo.get('name')
        url = repo.get('html_url')
        language = repo.get('language')
        desc = repo.get('description')
        star = repo.get('stargazers_count')
        if language is None:
            language = ''
        if desc is None:
            desc = ''
        desc = desc.strip().replace('\n', '').replace('\r', '')
        print '| [{}]({}) | {} | {} | {} |'.format(name, url, star, language, desc).decode('utf-8')


if __name__ == '__main__':
    print ('# Tencent Open Source Works\n'
            '腾讯开源作品整理. (仅收录Github上的项目).\n'
            '\n'
            'From: \n'
            '\n')

    names = ('Tencent', 'tencent-wechat', 'weui', 'weixin', 'QMUI', 'TencentOpen', 'AlloyTeam', 'frozenui', 'tencent-php')
    min_star = 10
    repos = []
    for name in names:
        print '* [{}]({})'.format( name, 'https://github.com/'+name )
        repos += get_repos_for_one(name)

    print ('\n'
            'Repos:\n'
            '\n')
    repos = filter_repos_by_stars(repos, min_star)
    print 
    show_repos_as_table(repos)
    print
    print
    print '## License'
    print 'MIT'
