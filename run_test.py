import os
import subprocess
import numpy as np
import pandas as pd

import json
import argparse


'''

1. Receive web test arguments and create a setting.json file to store on disk
2. Create a new folder for new test

'''

project_path = 'D:/webtest_site_storage'

argparser = argparse.ArgumentParser()
argparser.add_argument('-u', '--url', action='store')
argparser.add_argument('-b', '--browser', action='store')
argparser = vars(argparser.parse_args())
url = argparser['url']
browser = argparser['browser']


def background_run_test():
    print('Start testing in backgound...')
    new_folder = os.path.join(project_path, 'project_folder1')
    os.mkdir(new_folder) # create new project folder
    # new test folder
    new_test_folder = os.path.join(new_folder, 'test_folder')
    os.mkdir(new_test_folder)
    
    # Save web test arguments as json file
    # 1. first create a dictionary
    # 2. Save the dictionary as json file
    settings = {'url':url, 'browser':browser, 'state':'running'}    
    # save dictionary as JSON file
    with open('{}/settings.json'.format(project_path), 'w+') as f:
        json.dump(settings, f)
    
background_run_test()