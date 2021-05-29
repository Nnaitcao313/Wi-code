from flask import Flask, render_template, flash, request, redirect, url_for
from flask_mail import Mail, Message
import os, shutil
from werkzeug.utils import secure_filename

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import random


randomlist = []

for i in range(0,20):
    n = random.randint(1,30)
    randomlist.append(n)

listax = [4]


date = "2021-05-06"

def change_dformat(date):
    sample_date = datetime.strptime(date, "%Y-%m-%d")
    tdate = sample_date.strftime("%B %d, %Y at %I:%M%p")
    return(tdate)

nd = change_dformat(date)

print(nd + "hola wenas")


def sumcum(datos, lista):
    lista.append(datos[1])
    lista.append(datos[2])
    return(datos)

sumcum(randomlist, listax)

print(listax)
