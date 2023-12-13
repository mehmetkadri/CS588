import requests
import json
import os

popular_repos = []
medium_repos = []
small_repos = []


with open('repo_links.json') as f:
    data = json.load(f)
    popular_repos = data['popular_repos']
    medium_repos = data['medium_repos']
    small_repos = data['small_repos']

for repo in popular_repos:
    print(repo['link'])
#    print(repo['stars'])

def get_forks(project_name):
    forks = []
    page_count = 1
    print(project_name.split('/')[1] + "'s forks:")
    while page_count>0:
        print("Forks numbered " + str((page_count-1)*100) + " to " + str(page_count*100) + " are being fetched.")
        try:
            r = requests.get('https://api.github.com/repos/' + project_name + '/forks?per_page=100&page=' + str(page_count), auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github+json'})
            page_count += 1
            if len(r.json()) == 0:
                page_count = -1
                break
            for fork in r.json():
                forks.append(fork['created_at'])
        except:
            print(project_name.split('/')[1] + " has no more forks to fetch.")
            page_count = -1
            break
    with open('forks_' + project_name.split('/')[1] + '.json', 'w') as f:
        json.dump(forks, f)
    return

def get_stars(project_name):
    stars = []
    page_count = 1
    print(project_name.split('/')[1] + "'s stars:")
    while page_count>0:
        print("Stars numbered " + str((page_count-1)*100) + " to " + str(page_count*100) + " are being fetched.")
        try:
            r = requests.get('https://api.github.com/repos/' + project_name + '/stargazers?per_page=100&page=' + str(page_count), auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github.v3.star+json'})
            page_count += 1
            if len(r.json()) == 0 or page_count > 400:
                page_count = -1
                break
            for star in r.json():
                stars.append(star['starred_at'])
        except:
            print(project_name.split('/')[1] + " has no more stars to fetch.")
            page_count = -1
            break
    with open('stars_' + project_name.split('/')[1] + '.json', 'w') as f:
        json.dump(stars, f)
    return

def get_commits(project_name):
    commits = []
    page_count = 1
    print(project_name.split('/')[1] + "'s commits:")
    while page_count>0:
        print("Commits numbered " + str((page_count-1)*100) + " to " + str(page_count*100) + " are being fetched.")
        try:
            r = requests.get('https://api.github.com/repos/' + project_name + '/commits?per_page=100&page=' + str(page_count), auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github+json'})
            page_count += 1
            if len(r.json()) == 0:
                page_count = -1
                break
            for commit in r.json():
                sha = commit['sha']
                date = commit['commit']['author']['date']
                message = commit['commit']['message']
                commits[sha] = [date, message]
        except:
            print(project_name.split('/')[1] + " has no more commits to fetch.")
            page_count = -1
            break
    with open('commits_' + project_name.split('/')[1] + '.json', 'w') as f:
        json.dump(commits, f)
    return

def get_issues(project_name):
    issues = []
    page_count = 1
    print(project_name.split('/')[1] + "'s issues:")
    while page_count>0:
        print("Issues numbered " + str((page_count-1)*100) + " to " + str(page_count*100) + " are being fetched.")
        try:
            r = requests.get('https://api.github.com/repos/' + project_name + '/issues?per_page=100&page=' + str(page_count), auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github+json'})
            page_count += 1
            if len(r.json()) == 0:
                page_count = -1
                break
            for issue in r.json():
                sha = issue['id']
                date = issue['created_at']
                issues[sha] = date
        except:
            print(project_name.split('/')[1] + " has no more issues to fetch.")
            page_count = -1
            break
    with open('issues_' + project_name.split('/')[1] + '.json', 'w') as f:
        json.dump(issues, f)
    return

def get_branches(project_name):
    branches = []
    page_count = 1
    print(project_name.split('/')[1] + "'s branches:")
    while page_count>0:
        print("Branches numbered " + str((page_count-1)*100) + " to " + str(page_count*100) + " are being fetched.")
        try:
            r = requests.get('https://api.github.com/repos/' + project_name + '/branches?per_page=100&page=' + str(page_count), auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github+json'})
            page_count += 1
            if len(r.json()) == 0:
                page_count = -1
                break
            for branch in r.json():
                name = branch['name']
                commit_url = branch['commit']['url']
                is_protected = branch['protected']
                r = requests.get(commit_url, auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github+json'})
                commit = r.json()
                date = commit['commit']['author']['date']
                message = commit['commit']['message']
                branches[name] = [date, message, is_protected]
        except:
            print(project_name.split('/')[1] + " has no more branches to fetch.")
            page_count = -1
            break
    with open('branches_' + project_name.split('/')[1] + '.json', 'w') as f:
        json.dump(branches, f)
    return

def get_readme_content(project_name, sha):
    with open('readme_changes_' + project_name.split('/')[1] + '.json', 'r') as f:
        readme_changes = json.load(f)
    for sha, date in readme_changes.items():
        print("Fetching readme content for commit " + sha + "...")
        try:
            r = requests.get('https://raw.githubusercontent.com/' + project_name + '/' + sha + '/README.md')
            # save to file
            with open('readme_content_' + project_name.split('/')[1] + date + '.json', 'w') as f:
                json.dump(r.json(), f)
        except:
            print("No readme content found for commit " + sha + ".")
    return

def get_commit_readme_changes(project_name):
    readme_changes = {}
    page_count = 1
    print(project_name.split('/')[1] + "'s commits:")
    while page_count>0:
        print("Commits numbered " + str((page_count-1)*100) + " to " + str(page_count*100) + " are being fetched.")
        try:
            r = requests.get('https://api.github.com/repos/' + project_name + '/commits?path=README.md&per_page=100&page=' + str(page_count), auth=('Bearer', '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'), headers={'Accept': 'application/vnd.github+json'})
            page_count += 1
            if len(r.json()) == 0:
                page_count = -1
                break
            for commit in r.json():
                sha = commit['sha']
                date = commit['commit']['author']['date']
                readme_changes[sha] = date
        except:
            print(project_name.split('/')[1] + " has no more commits to fetch.")
            page_count = -1
            break
    with open('readme_changes_' + project_name.split('/')[1] + '.json', 'w') as f:
        json.dump(readme_changes, f)
    return



# create directory for popular repos if it doesn't exist
if not os.path.exists('popular_repos'):
    os.makedirs('popular_repos')
os.chdir('popular_repos')

for repo in popular_repos:
    get_forks(repo['link'])
    get_stars(repo['link'])
    get_commits(repo['link'])
    get_issues(repo['link'])
    get_branches(repo['link'])
    get_commit_readme_changes(repo['link'])
    get_readme_content(repo['link'])

os.chdir('..')


# create directory for medium repos if it doesn't exist
if not os.path.exists('medium_repos'):
    os.makedirs('medium_repos')
os.chdir('medium_repos')

for repo in medium_repos:
    get_forks(repo['link'])
    get_stars(repo['link'])
    get_commits(repo['link'])
    get_issues(repo['link'])
    get_branches(repo['link'])
    get_commit_readme_changes(repo['link'])
    get_readme_content(repo['link'])

os.chdir('..')


# create directory for small repos if it doesn't exist
if not os.path.exists('small_repos'):
    os.makedirs('small_repos')
os.chdir('small_repos')

for repo in small_repos:
    get_branches(repo['link'])
    get_commit_readme_changes(repo['link'])
    get_issues(repo['link'])
    get_forks(repo['link'])
    get_commits(repo['link'])
    get_stars(repo['link'])
#    get_readme_content(repo['link'])

os.chdir('..')