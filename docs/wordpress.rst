---------
Wordpress
---------

Quick Start
-----------

.. code:: bash

    # edit docker.config
    PROJECT_NAME=wordpress
    COMPOSE_YML=./docker/wordpress.yml

    # run
    ./docker.sh start -f

    # open in http://localhost:10001

FAQ
---

Database not created
^^^^^^^^^^^^^^^^^^^^

Just delete all /data/mysql directory, to start from scratch.

Import/export mysql database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure you have mysql container in the configuration and your sql file in /data/backup.sql directory.
Change the database username, password in wordpress.yml if necessary. Ensure the database host is "mysql"

MacOS/UNIX
^^^^^^^^^^

.. code:: bash

    ./docker.sh exec mysql bash -c "mysql -u root -pwordpress_password1 wordpress < /data/backup.sql"
