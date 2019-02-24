# SDGameLab
Laboratorio de Sistema Distribuidos - Juego distribuido


## Docker image
Para poder ejecutar el ejemplo de una app en Python 3 con Redis es necesario instalar Docker para crear y montar la imagen.

* [Link para instalación de Docker en Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)

Luego es necesario instalar docker-compose, el cual puede ser instalado usando pip mediante el comando:

```bash
$ pip install docker-compose
```

Para crear y montar la imagen se usa el comando docker-compose

```bash
$ docker-compose up
```
*En primera instancia se construye la imagen y se monta, si la imagen ya fué construida con anterioridad solo se monta la existente, en caso de querer reconstruir la imagen se debe agregar la flag --build*

Con el comando `$ docker ps` se pueden observar los contenedores en ejecución, los cuales en este caso serán la app y redis.

* En caso de existir imagenes nulas (< none >) se pueden eliminar con el comando `$ docker image prune` mientras se tiene ejecución los contenedores con las imágenes que se desean mantener (elimina imágenes que no están es un uso).

## RQ Service

Servicio de colas haciendo uso de RQ junto con python para encolar y procesar trabajos.

* Se hace uso de la imagen de jaredv rq-docker (jaredv/rq-docker:0.0.2)

Se tienen imagenes para 4 contenedores:
* rq-server: Contenedor de redis para almacenar las colas en la BD
* rq-worker: Contenedor de worker para obtener y procesar los trabajos desde las colas
* rq-dashboard: Contenedor de una app de dashboard para monitorear los trabajos de los workers
* rq-service_app: Contenedor de la aplicación en flask, en la cual se realizan las llamadas al servicio

Para construir las imagenes y montarlas se hace uso del comando `$ docker-compose up` luego de esto, ya con los contenedores funcionando se podrá acceder al dashboard en la dirección http://localhost:9181 y para las llamadas a los servicios la dirección http://localhost:5000

*No existe feature en dashboard para monitorear trabajos terminados, esto solo se puede observar en la consola, donde si el trabajo fue terminado con éxito llegará un mensaje del contenedor del worker que lo realizó informando "queue: job OK (job_id)"*

*Actualmente solo existe un servicio el cual crea un job para la suma de 5+5, lo cual retorna un 10*
