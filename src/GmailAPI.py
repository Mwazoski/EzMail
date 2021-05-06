# Librerias 
import smtplib , ssl
import getpass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Librerias para el framework Flask
from flask import Flask, render_template, request

# Librerias para el manejo de la base de datos sqlite3 y sus errores.
from sqlite3 import IntegrityError
import sqlite3


app = Flask(__name__)       # Iniciamos la aplicacion de Flask

usuario = ["a" , "a"]

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/login_done', methods=["GET","POST"])
def login_done():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        usuario[0] = email         # Variable global Usuario
        usuario[1] = password

    conn = sqlite3.connect('gmailapi.db')
    c = conn.cursor()
    query = "SELECT correo FROM usuarios WHERE 1=1;"
    c.execute(query)
    direcciones = c.fetchall()
    c.close()

    return render_template('email.html', direcciones = direcciones)

@app.route('/message_send', methods=["GET","POST"])
def message_send():
    if request.method == 'POST':
        
        asunto = request.form['asunto']
        destinatario = request.form['destinatario']
        texto = request.form['mensaje']

        mensaje = MIMEMultipart("alternative")
        mensaje["Subject"] = asunto
        mensaje["From"] = usuario[1]
        mensaje["To"] = destinatario 
        
        html = f"""
        <html>
        <body>
            <p>{texto}</p>
        </body>
        </html>
        """

        parte_html = MIMEText(html, "html")
        mensaje.attach(parte_html)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com" , 465 , context=context) as servidor:
            servidor.login(usuario[0], usuario[1])
            servidor.sendmail(usuario[1], destinatario, mensaje.as_string())                               # Enviamos mail con toda la información
            print("Mensaje Enviado!!")

    return render_template('index.html')

@app.route('/register_done', methods=["GET","POST"])
def register_done():
    
    try:
        if request.method == 'POST':
            
            email = request.form['email']
            name = email.split('@', 1)
            
            print(name[0])
            conn = sqlite3.connect('gmailapi.db')
            c = conn.cursor()
            query = "INSERT INTO usuarios (nombre,correo) VALUES ('{}' , '{}');".format(name[0], email)
            c.execute(query)
            conn.commit()
            c.close()
    
    except sqlite3.Error as m_error:
        print(m_error)
        return render_template('index.html' , error = 513)          # El error 513 especifica que en la base de datos se ha producido un error  


    finally:
            if (conn):
                conn.close()
    
    return render_template('index.html')


# Arranca la aplicación

if __name__ == "__main__":
    app.run(debug=True)