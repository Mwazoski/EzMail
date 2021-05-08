.. EasyGmail documentation master file, created by
   sphinx-quickstart on Wed May  5 19:05:37 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Documentación de EasyGmail
==========================

Esta APIRest se encarga de realizar un inicio de sesión para poder facilitar el envio de mensajes a través de una API, la API de Gmail necesita que 
tengamos un asunto del mensaje, un destinatario, un cuerpo del mensaje, y obviamente, un emisor.

Una vez hemos realizado el login del usuario (con una cuenta verificada por gmail) introduciremos el asunto, destinatario y mensaje que queramos y enviaremos
el mensaje

Es una API sencilla que nos permitirá incorporarla en otras webs donde necesitemos manejar correos electrónicos. En este proyecto solo se ve reflejado el envio de mensajes,
pero de igual manera, se podrían reproducir los mensajes que se nos envíe. De esta forma lograríamos dentro de nuestra web una pequeña administración de nuestros emails.

.. toctree::
   :maxdepth: 2
   :caption: Indice

   documentos/instalacion
   documentos/autores
   documentos/ejecucion
   documentos/uso
   documentos/codigo
