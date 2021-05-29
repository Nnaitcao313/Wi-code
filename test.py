from flask import Flask, render_template, flash, request, redirect, url_for
from flask_mail import Mail, Message
import os, shutil
from werkzeug.utils import secure_filename
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def fig_barh(ylabels, xvalues, title=''):
    # create a new figure
    fig = plt.figure()

    # plot to it
    yvalues = 0.1 + np.arange(len(ylabels))
    plt.barh(yvalues, xvalues, figure=fig)
    yvalues += 0.4
    plt.yticks(yvalues, ylabels, figure=fig)
    if title:
        plt.title(title, figure=fig)

    # return it
    return fig

a = fig_barh(['a','b','c'], [1, 2, 3], 'Test #1')
b = fig_barh(['x','y','z'], [5, 3, 5], 'Test #2')


@app.route('/')
def main():
    return render_template("test.html")

@app.route('/index')
def show_index():
    full_filename = "/static/testB.png"
    print(full_filename)
    return render_template("test2.html", user_image = full_filename)

@app.route('/form')
def form():
    print(request.form.get('date'))
    return(render_template('test2.html', ndate=request.args.get('date')))

if __name__ == '__main__':
    app.run(debug=True)