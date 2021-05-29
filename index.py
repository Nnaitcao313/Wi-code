from flask import Flask, render_template, flash, request, redirect, url_for
from flask_mail import Mail, Message
import os, shutil
from werkzeug.utils import secure_filename

from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates
import numpy as np

import excel

app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'wicode.soporte@gmail.com'
app.config["MAIL_PASSWORD"] = 'wicode3626'
app.config["MAIL_DEFAULT_SENDER"] = "wicode.soporte@gmail.com"
app.config["MAIL_MAX_EMAILS"] = None

mail = Mail(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
folder = 'uploads'

values = excel.get_values()

def get_day(t_date):
    temp = ""
    n = 11
    for i in range(len(t_date) - n):
        temp = temp + t_date[i]
    return(temp)

def get_year(t_date):
    temp = ""
    n = 11
    for i in range(len(t_date) - n):
        temp = temp + t_date[i]
    year = ""
    for i in range(4,0,-1):
        year += temp[-i]
    return(year)

def get_month(t_date):
    year = get_year(t_date)
    month = ""
    ind = t_date.index(" ")
    month = t_date[0:ind]
    return(month + " " + year)

def get_avg(datos, target, type, fechas):
    fechas.clear()
    new_data = []
    leg = target
    remai = len(datos) % leg

    for (i, item) in enumerate(datos, start=0):
        if i % leg == (leg-1):
            var = 0
            for x in range(0,leg):
                if (i-x) % leg != 0:
                    var += float(datos[(i-x)][type])
                elif (i-x) % leg == 0:
                    var += float(datos[(i-x)][type])
                    var = float(var) / leg
                    round(var,2)
                    new_data.append(var)
                    fechas.append(datos[(i-x)][0])
        elif i == (len(datos)-remai):
            var = 0
            for x in range(0,remai):
                if (i+x) == (len(datos)-remai):
                    var += float(datos[(i+x)][type])
                    fechas.append(datos[i][0])
                elif (i+x) != len(datos)-1:
                    var += float(datos[(i+x)][type])
                elif (i+x) == len(datos)-1:
                    var += float(datos[(i+x)][type])
                    var = float(var)/remai
                    round(var,2)
                    new_data.append(var)
    return(new_data)


def get_avi(datos, type, fechas):
    fechas.clear()
    new_data = []
    for (i, item) in enumerate(datos, start=0):
        if i % 2 == 1:
            var = (float(item[type]) + float(datos[i-1][type])) / 2
            round(var,2)
            new_data.append(var)
            fechas.append(datos[i-1][0])
        elif i == (len(datos)-1):
            new_data.append(float(item[type]))
            fechas.append(item[0])
    return(new_data)


def fig_plot(xvalues, yvalues, title, ylabel, extension):
    with plt.style.context('ggplot'):
        fig = plt.figure()

        plt.plot_date(xvalues, yvalues, 'b-')
        plt.title(title, figure=fig)
        plt.xlabel(ylabel)
        plt.ylabel("Fechas")

        fig.autofmt_xdate()

        fig.savefig(f"static/{extension}.png", transparent=True)
        return(f"static/{title}.png")

def change_dformat(date):
    sample_date = datetime.strptime(date, "%Y-%m-%d")
    tdate = sample_date.strftime("%B %d, %Y at %I:%M%p")
    return(tdate)

def get_target(date, index):
    ndate = datetime.strptime(date, "%B %d, %Y at %I:%M%p")
    target = ndate.strftime(index)
    return(target)


#Cambiar los get_XXX por get_target
#Usar el change_dformat para pasar el request al formato necesario
#Actualizar las comparaciones para usar las nuevas funciones y la nueva forma de encontrar el tiempo puesto


@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/datos', methods=['POST','GET'])
def datos():
    date_format = "%B %d, %Y at %I:%M%p"
    lista_datos = []
    fechas = [1]
    datos_hum = []
    datos_cel = []
    datos_far = []
    form_date = change_dformat(request.form.get('date'))

    global humedad
    global farenheit
    global celcius
    
    if request.form.get('time') == "Año":
        for item in values:
            if get_target(item[0], "%Y") == get_target(form_date, "%Y"):
                trary_list = [item[0],item[2],item[3],item[4]]
                lista_datos.append(trary_list)

        lista_datos.sort(key=lambda date: datetime.strptime(date[0], date_format))

        datos_hum = get_avg(lista_datos,720,1,fechas)
        datos_cel = get_avg(lista_datos,720,2,fechas)
        datos_far = get_avg(lista_datos,720,3,fechas)

        fechas = matplotlib.dates.datestr2num(fechas)

        humedad = fig_plot(fechas, datos_hum, "Gráfico Porcentage Humedad: Año", "% Humedad", "hum_anual")
        celcius = fig_plot(fechas, datos_cel, "Gráfico Grados Celcius: Año", "Grados Celcius", "cel_anual")
        farenheit = fig_plot(fechas, datos_far, "Gráfico Grados Farenheit: Año", "Grados Farenheit", "far_anual")


    elif request.form.get('time') == "Mes":
        for item in values:
            if get_target(item[0], "%Y-%B") == get_target(form_date, "%Y-%B"):
                trary_list = [item[0],item[2],item[3],item[4]]
                lista_datos.append(trary_list)

        lista_datos.sort(key=lambda date: datetime.strptime(date[0], date_format))

        datos_hum = get_avg(lista_datos,60,1,fechas)
        datos_cel = get_avg(lista_datos,60,2,fechas)
        datos_far = get_avg(lista_datos,60,3,fechas)

        fechas = matplotlib.dates.datestr2num(fechas)

        humedad = fig_plot(fechas, datos_hum, "Gráfico Porcentage Humedad: Mes", "% Humedad", "hum_men")
        celcius = fig_plot(fechas, datos_cel, "Gráfico Grados Celcius: Mes", "Grados Celcius", "cel_men")
        farenheit = fig_plot(fechas, datos_far, "Gráfico Grados Farenheit: Mes", "Grados Farenheit", "far_men")
        
        
    elif request.form.get('time') == "Día":
        for item in values:
            if get_target(item[0],"%B %d, %Y") == get_target(form_date, "%B %d, %Y"):
                trary_list = [item[0],item[2],item[3],item[4]]
                lista_datos.append(trary_list)

        lista_datos.sort(key=lambda date: datetime.strptime(date[0], date_format))

        datos_hum = get_avi(lista_datos,1,fechas)
        datos_cel = get_avi(lista_datos,2,fechas)
        datos_far = get_avi(lista_datos,3,fechas)

        fechas = matplotlib.dates.datestr2num(fechas)

        humedad = fig_plot(fechas, datos_hum, "Gráfico Porcentage Humedad: Día", "% Humedad", "hum_dia")
        celcius = fig_plot(fechas, datos_cel, "Gráfico Grados Celcius: Día", "Grados Celcius", "cel_dia")
        farenheit = fig_plot(fechas, datos_far, "Gráfico Grados Farenheit: Día", "Grados Farenheit", "far_dia")

    return render_template("display.html", 
    hum = humedad, cel = celcius, far = farenheit)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/Equipo')
def about():
    return render_template("about.html")

@app.route('/Contactanos')
def contact():
    return render_template("contact.html")

@app.route('/Blog')
def blog():
    return render_template("blog.html")

@app.route('/Proyectos')
def projects():
    return render_template("projects.html")

@app.route('/Mision')
def mision():
    return render_template("mision.html")

@app.route('/Tienda')
def tienda():
    return render_template("tienda.html")

@app.route('/Productos')
def products():
    last_3 = len(values) -3
    
    date = get_target(values[last_3-1][0],"%B %d, %Y")
    hum = float(values[last_3][2])

    dat1 = f"{date}: {hum}"

    last_3+=1

    date = get_target(values[last_3-1][0],"%B %d, %Y")
    hum = float(values[last_3][2])

    dat2 = f"{date}: {hum}"

    last_3+=1

    date = get_target(values[last_3-1][0],"%B %d, %Y")
    hum = float(values[last_3][2])

    dat3 = f"{date}: {hum}"


    return render_template("products.html", dato1=dat1, dato2=dat2,dato3=dat3)

@app.route('/Carrito')
def carrito():
    return render_template("carrito.html")

@app.route('/Cuenta')
def cuenta():
    return render_template("cuenta.html")

@app.route('/Info')
def req():
    return render_template("request.html")

@app.route('/Display')
def display():
    return render_template("display.html")

@app.route('/Witrap-Ms')
def an_ms():
    return render_template("an_ms.html")

@app.route('/Witrap-Cr')
def an_cr():
    return render_template("an_cr.html")

@app.route('/Witrap-Zc')
def an_zc():
    return render_template("an_zc.html")

@app.route('/Witrap-XX')
def an_xx():
    return render_template("an_xx.html")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/form', methods=['POST','GET'])
def form():
        nombre = request.form.get('nombre')
        comentario = request.form.get('comentario')
        email = request.form.get('email')
        telefono = request.form.get('telefono')

        msg = Message("Soporte: Nueva Solicitud", recipients=['Wicodeinc@gmail.com'])
        msg.html = '<body><p>Nombre: %s</p><p>Email: %s</p><p>Telefono: %s</p><p>Comentario: %s</p></body>' %(nombre, email, telefono, comentario)
    
        if request.method == 'POST':
            file = request.files['archivo']
            if request.files['archivo'].filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                    fic = open("uploads/" + file.filename, "r", encoding='utf8', errors='ignore')


                    with app.open_resource("uploads/" + file.filename) as test:
                        msg.attach(file.filename, 'image/jpg', test.read())

                        mail.send(msg)

                    #msg.attach({{url_for('uploads', filename=filename)}}, "image/png", fic.read())

        mail.send(msg)

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        return redirect('Contactanos')



if __name__ == '__main__':
    app.run(debug=True)