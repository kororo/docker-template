---------------
Docker Commands
---------------

Build & Up (Detached)
^^^^^^^^^^^^^^^^^^^^^

Build docker configuration and start it up to create network, images and run it all in background mode.

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} build && docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} up

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


Following Logs
^^^^^^^^^^^^^^

Watching logs in containers

MacOS/UNIX
++++++++++

.. code:: bash

    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml

    # watching all containers logs
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} logs -f

    SERVICE_NAME=mysql
    # watching mysql container
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} logs -f ${SERVICE_NAME}

    # it is better to run not in detached, because it is running and starting watching all the logs
    docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} build && docker-compose -p ${PROJECT_NAME} -f ${COMPOSE_YML} up

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

