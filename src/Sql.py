# runsql.py

import sqlite3

def databasecreate():

    """
    Función que se encarga de crear en un primer lugar una base de datos para poder crear
    el esquema de las tablas en la APIRest. Esta se encarga simplemente de facilitar la
    creación de la Base de Datos *Padre* sobre la cual poder introducir más información
        :param name: conn
                    Objeto de sql que se encarga de realizar todas las operaciones con la Base de Datos sqlite3.
    """

    print("Creando la base de datos");

    # TABLA DE USUARIOS

    conn = sqlite3.connect('gmailapi.db')
    conn.execute("CREATE TABLE usuarios (nombre char(50), correo char(60) PRIMARY KEY NOT NULL)")
    conn.execute("INSERT INTO usuarios (nombre, correo) VALUES ('default','default@uca.es') ")
    
    conn.commit()
    conn.close()

    print("\n Base de datos creada")    


if __name__ == '__main__':

    databasecreate()