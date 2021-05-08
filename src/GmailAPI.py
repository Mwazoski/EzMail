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

    """
    Ruta que interpreta la pagina principal donde se permite realizar tanto un registro de correos electrónicos
    que podremos seleccionar en el momento de mandar un mensaje por correo.
    """

    return render_template('index.html')

@app.route('/login_done', methods=["GET","POST"])
def login_done():

    """
    Ruta que interpreta el apartado de mensajería una vez que los datos de inicio de sesión son correctos.
        
        :param email:
                    Email que se ha proporcionado en el logeo de sesión
        :param password:
                    password que se ha proporcionado en el logeo de sesión
        :param user:
                    Información relativa al usuario que proviene del login
        :param conn:
                    Objeto sql para realizar las conexiones a la base de datos estipulada
        :param c:
                    Cursos de la conexión sql
        :param query:
                    Query que se encarga de realizar la operacion adecuada para la consulta sql
        :param direcciones:
                    Direcciones de correo electronico que estan almacenadas en la base de datos y que serviran 
                    para proporcionar todos los destinatarios disponibles
    """

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

    """
    Ruta que interpreta el apartado de mensajería una vez que el mensaje se ha enviado correctamente, esta parte
    es la que permite que el cliente se conecte con la API para realizar las operaciones de envio de mensajes.
    
        :param asunto:
                    Asunto que se ha proporcionado en el mensaje de correo
        :param destinatario:
                    Destinatario que se ha proporcionado en el mensaje de correo.
        :param mensaje:
                    Objeto mensaje que se encarga de mandar el correo con un asunto, un destinatario y un formato html
        :param parte_html:
                    Cuerpo, en html, del mensaje
        :param context:
                    Conexión que se realiza con la API para que se pueda mandar el correo, a este se le proporciona un logeo
                    de sesión, el asunto, destinatario y cuerpo del mensaje.
    """

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

    """
    Ruta que interpreta el apartado la pagina principal una vez que el registro de un destinatario se ha realizado con éxito.
    
        :param email:
                    Email que se ha proporcionado en el registro de destinatario
        :param name:
                    Nombre que se ha proporcionado en el registro de destinatario
        :param conn:
                    Objeto sql para realizar las conexiones a la base de datos estipulada
        :param c:
                    Cursos de la conexión sql
        :param query:
                    Query que se encarga de realizar la operacion adecuada para la consulta sql
    """
    
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