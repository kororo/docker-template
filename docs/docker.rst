------
Docker
------

This is knowledge based for Docker related.

KB
--

Docker logs for process PID != 1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you have docker and spawn multiple processes. You will start notice there is no logs outputed into docker logs.
This due to Docker arch only listen to the process PID == 1. How to fix this is to redirect the stdout to PID 1.

.. code:: bash

    # create bash script to run this command when docker is running
    # in docker-compose.yml you can do:
    # command: "/script/start.sh"

    #!/usr/bin/env bash
    tail -n 0 -q -F /your/app/dir/logs/*.log >> /proc/1/fd/1 &


Make process running forever in Docker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sometime, when you create your own bootstrap script for your container. You need something to run forever to keep the
Docker container to not exited.

.. code:: bash

    # create bash script to run this command when docker is running
    # in docker-compose.yml you can do:
    # command: "/script/start.sh"

    #!/usr/bin/env bash

    echo "Running app ..."
    trap : TERM INT; sleep infinity & wait


Docker Commands
---------------

List of nice docker-compose commands.

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

