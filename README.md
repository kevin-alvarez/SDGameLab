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
