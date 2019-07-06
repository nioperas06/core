import requests
import time
import os

r = requests.post('https://circleci.com/api/v1/project/masoniteframework/validation/tree/circle-ci?circle-token={}'.format(os.getenv('CIRCLE_TOKEN')))
print('Building: ', r.json()['build_num'])

status = requests.get('https://circleci.com/api/v1.1/project/github/masoniteframework/validation/{}?circle-token={}'.format(r.json()['build_num'], os.getenv('CIRCLE_TOKEN')))
print('Build Status: ', status.json()['lifecycle'])
while status.json()['lifecycle'] != 'finished':
    print('Build Status: ', status.json()['lifecycle'])
    time.sleep(3)
    status = requests.get('https://circleci.com/api/v1.1/project/github/masoniteframework/validation/{}?circle-token={}'.format(r.json()['build_num'], os.getenv('CIRCLE_TOKEN')))

print('Finished. Failed? ', status.json()['failed'])
if status.json()['failed']:
    exit(1)
