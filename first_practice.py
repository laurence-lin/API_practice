from flask import Flask, request, render_template, session
import os
import shutils

# instance of Flask would be WSGI application
# central registry for view functions
app = Flask('main')  # pass name of package, if only one module, __name__ is correct and fine, else define by ourself


@app.route('/') # route: define what URL would trigger our function
def main_page():
    return 'Welcome to web defect detection system!'  # function return the message we want to display on the browser

@app.route('/hello')
def second_page():
    return "Hello World!"

#Read files from disk and display
@app.route('/web_test_data')
def show_webtest_data():    # read files from disk and display 
    test_list = os.listdir('D:/web_testing_data')
    return "All web testing data files: {}".format(test_list)
