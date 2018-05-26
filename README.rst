===============
Docker Template
===============

List of docker template for quick deployment.


Requirements
------------

List of requirements to get the template working:

- Docker engine
- Docker compose


Quick Usage
-----------

Rapid commands to use the template. Notes:

- PROJECT_NAME: Represent your project name
- COMPOSE_YML: This is the docker compose yaml configuration choosen (eg. ./docker/wordpress.yml)

Build & Up (Detached)
^^^^^^^^^^^^^^^^^^^^^

Build docker configuration and start it up to create network, images and run it all in background mode.

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml

    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} build && docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} up -d

Execute Script
^^^^^^^^^^^^^^

Quick way to execute script into **running** container.

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml
    SERVICE_NAME=php

    # execute bash in command mode
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec ${SERVICE_NAME} bash -c "echo A"

    # or simply SSH into the service/container
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec ${SERVICE_NAME} bash

Stop
^^^^

Stopping containers in docker.

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml

    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} stop


Remove
^^^^^^

Remove all containers in the docker.

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml

    # remove container, and network
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} down

    # remove volume (your data)
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} down -v


Directory Structures
--------------------

- data: The data directory for the applications, can be logs, images

- docker: The root directory of the docker configuration

    - php: The build configuration of each containers

    - wordpress.yml: The docker-compose configuration

- src: The main code of your applications

Wordpress WIKI
--------------

Quick wiki for daily tasks around docker. This is temporary space until there is better place to put.

Database not created
++++++++++++++++++++

Just delete all /data/mysql directory, to start from scratch.

Import mysql database
+++++++++++++++++++++

Ensure you have mysql container in the configuration and your sql file in /data/backup.sql directory.
Change the database username, password in wordpress.yml if necessary

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml
    SERVICE_NAME=mysql

    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} exec ${SERVICE_NAME} bash -c "mysql -u wordpress_user -pwordpress_password1 wordpress < /data/backup.sql"

TODO
----

- [ ] Add more commands for Windows
- [ ] Add bash script startup commands

