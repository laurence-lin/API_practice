from flask import Flask, request, render_template, session, redirect, url_for
import os
import shutils
import pandas as pd
import json
import subprocess
from threading import Thread
import glob

# instance of Flask would be WSGI application
# central registry for view functions
app = Flask('main')  # pass name of package, if only one module, __name__ is correct and fine, else define by ourself


app.secret_key = b'flafhe9898jgajsr9jg9j8qt8jpgq98j4' # set secret key for session

project_path = 'D:/webtest_site_storage'


@app.route('/') # route: define what URL would trigger our function
def main_page():
    return 'Welcome to web defect detection system!'  # function return the message we want to display on the browser


# Start the function of web testing system
@app.route('/main_page', methods=['GET','POST'])
def main_webpage():
    if request.method == 'POST':
        return redirect(url_for('start_test'))
    
    return render_template('main_page.html')


# send POST message to Flask server
@app.route('/web_test', methods=['GET', 'POST'])
def start_test():
    if request.method == 'POST':
        session['url'] = request.form['url']
        session['browser'] = request.form['browser']
        return redirect(url_for('background_run_test'))
    
    return render_template('enter_argument.html')

# background script: create folder and receive argument
@app.route('/running_test')
def background_run_test():
    url = session['url']
    browser = session['browser']
    os.system("python D:/API/first_flask/run_test.py --url {} --browser {}".format(url, browser)) # execute python script
    return 'Running test!  Current argument: URL = {}  browser = {}'.format(session['url'], session['browser'])


#get state of current test from folder
@app.route('/get_stat')
def get_state():
    # read state from file in server
    with open(os.path.join(project_path, 'settings.json'), 'r+') as f:
        data = json.load(f)
        state = data['state']
        return 'test state: {}'.format(state)
    
# Calculate total files in folder
@app.route('/get_total_images')
def get_sum_imgs():
    total_imgs = glob.glob('D:/webtest_site_storage/test_folder1/images/*.png')
    total_imgs = len(total_imgs)

    return 'Total images: {}'.format(total_imgs)

# Get testing result.json file
@app.route('/get_test_result')
def get_test_result():
    path = 'D:/webtest_site_storage/test_result.json'
    with open(path, 'r+') as f:
        data = json.load(f)
        
    return data

@app.route('/get_image_file/image_id=<image_id>')
def get_single_image(image_id):
    # To display specific image: get image directory from test_result.json file
    print('Image id: ', image_id)
    path = 'D:/webtest_site_storage/test_result.json'
    with open(path, 'r+') as f:
        data = json.load(f)
        for i in range(len(data)):
            if data[i]['imageID'] == int(image_id):
               return data[i]['image_dir']
        
        return 'Image ID not found!'
    
# Setup debug mode by default: code updates automatically without restart needed
if __name__ == '__main__':
   app.debug=True 
   app.run()













