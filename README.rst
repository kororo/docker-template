===============
Docker Template
===============

List of docker template for quick deployment.


Why?
----

Reason there is existance of this project is based on my own experience. I been working for at least 10+ projects with docker.
My main reason of using docker is to eliminate of "tedious" command line execution to start up my environment. Yes, it is true
most of the heavy lifted by Docker + docker-compose but it is still lots of commands to remember and typing, especially if you
have bit custom than usual.

Requirements
------------

List of requirements to get the template working:

- Docker engine
- Docker compose


Installation
------------

MacOS
^^^^^

- Install `Docker for Mac <https://store.docker.com/editions/community/docker-ce-desktop-mac>`_


UNIX
^^^^

.. code:: bash

    ### Docker Installation ###
    # install docker-ce with edge engine
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update && sudo apt-get install -y docker-ce

    # install docker-compose
    sudo curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # prepare the users
    sudo usermod -aG docker ubuntu

    # restart to take effect
    sudo service docker restart

    # relog the SSH
    exit

    # verify docker
    docker ps
    ### End Docker Installation ###


Quick Usage
-----------

Rapid commands to use the template. Notes:

- PROJECT_NAME: Represent your project name
- COMPOSE_YML: This is the docker compose yaml configuration choosen (eg. ./docker/wordpress.yml)

What is docker.sh?
------------------

It is shortcut to execute docker commands, at the moment only available for UNIX environment. If you are not interested
to use **docker.sh**, please check more in `docs/docker <https://github.com/kororo/docker-template/tree/master/docs/docker.rst>`_

.. code:: bash

    # ensure you have execute permission
    chmod +x docker.sh

    # if you feel this script is worth to use globally, "docker-template start"
    cp ./docker.sh /usr/local/bin/docker-template

    # change the configuration inside docker.config
    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml


Build & Up (Detached)
^^^^^^^^^^^^^^^^^^^^^

Build docker configuration and start it up to create network, images and run it all in background mode.

MacOS/UNIX
++++++++++

.. code:: bash

    # run in foreground
    ./docker.sh start

    # run in background
    ./docker.sh start -d

Execute Script
^^^^^^^^^^^^^^

Quick way to execute script into **running** container.

MacOS/UNIX
++++++++++

.. code:: bash

    # echo in container
    ./docker.sh exec echo "hello"

    # SSH-ing into container
    ./docker.sh ssh

    # run bash
    ./docker.sh exec bash -c "echo 'hello'"


Stop
^^^^

Stopping containers in docker.

MacOS/UNIX
++++++++++

.. code:: bash

    ./docker.sh stop

Following Logs
^^^^^^^^^^^^^^

Watching logs in containers

MacOS/UNIX
++++++++++

.. code:: bash

    # watch all logs
    ./docker.sh logs

    # tail the logs
    ./docker.sh logs -f

    # get specific container log
    ./docker.sh logs mysql

Remove
^^^^^^

Remove all containers in the docker.

MacOS/UNIX
++++++++++

.. code:: bash

    # remove all container and network
    ./docker.sh remove

    # remove all including volume
    ./docker.sh remove -v

Directory Structures
--------------------

- data: The data directory for the applications, can be logs, images

- docker: The root directory of the docker configuration

    - php: The build configuration of each containers

    - wordpress.yml: The docker-compose configuration

- src: The main code of your applications

- docker.sh: shortcut docker commands

Spaces
------

Spaces is the way to organised what application you could bootstrap quickly

- Wordpress: `docs/wordpress <https://github.com/kororo/docker-template/tree/master/docs/wordpress.rst>`_
- PHP7: `docs/php <https://github.com/kororo/docker-template/tree/master/docs/php.rst>`_

FAQ
---

**Q: Why you use specific version of Docker image?**

A: The reason of this project is to show the basic guideline on how to use the Docker.
It is recommended for you to go fork the repo and change to your specific needs.


**Q: Where is Windows version?**

A: I use Windows just pure gaming experience in the past 2 years. I will put this into the least things to do in the project.
If someone keen enough to do PR for me to do powershell, that would be awesome.

TODO
----

- [ ] Add more commands for Windows
- [X] Add bash script startup commands
- [ ] Add more environment variables for port
- [ ] Do deployment with kubernetes
- [ ] Add more docker recipe for python, solr, psql, neo4j, mongo, nodejs

