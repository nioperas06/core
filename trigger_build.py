import requests
import time
import os
import argparse
parser = argparse.ArgumentParser()

#-db DATABSE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-r", "--repo", help="Repository name")
parser.add_argument("-b", "--branch", help="Branch name")
parser.add_argument("-t", "--token", help="Circle CI Token")

args = parser.parse_args()

repo = args.repo
branch = args.branch or 'master'
token = args.token or os.getenv('CIRCLE_TOKEN')
r = requests.post('https://circleci.com/api/v1/project/{}/tree/{}?circle-token={}'.format(repo, branch, token))

if 'build_num' not in r.json():
    print('ERROR: Could not find repository {} or with the branch {}'.format(repo, branch))

print('Building: ', r.json()['build_num'])

status = requests.get('https://circleci.com/api/v1.1/project/github/{}/{}?circle-token={}'.format(repo, r.json()['build_num'], token))
print('Build Status: ', status.json()['lifecycle'])
while status.json()['lifecycle'] != 'finished':
    time.sleep(3)
    print('Build Status: ', status.json()['lifecycle'])
    status = requests.get('https://circleci.com/api/v1.1/project/github/{}/{}?circle-token={}'.format(repo, r.json()['build_num'], token))

print('Finished. Failed? ', status.json()['failed'])
if status.json()['failed']:
    exit(1)
