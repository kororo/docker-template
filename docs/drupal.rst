---------
Wordpress
---------

Quick Start
-----------

.. code:: bash

    # edit docker.config
    PROJECT_NAME=drupal
    COMPOSE_YML=./docker/drupal.yml

    # run
    ./docker.sh start -d

    # this is only first time
    ./docker.sh exec php /script/drupal-install.sh

    # drush command?
    ./docker.sh exec php drush st

    # open in http://localhost:10001

FAQ
---

Database error
^^^^^^^^^^^^^^

Q: If you receive this error message "[error]  Failed to create database: ERROR 1045 (28000): Access denied for user 'drupal'@'172.24.0.3' (using password: YES)"
A: Just delete all /data/mysql directory, to start from scratch.

Import/export mysql database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure you have mysql container in the configuration and your sql file in /data/backup.sql directory.
Change the database username, password in drupal.yml if necessary. Ensure the database host is "mysql"

MacOS/UNIX
^^^^^^^^^^

.. code:: bash

    ./docker.sh exec mysql bash -c "mysql -u drupal -pPassword1 drupal < /data/backup.sql"
    ./docker.sh exec mysql bash -c "mysqldump -u drupal -pPassword1 drupal > /data/backup.sql"

Execute drush command
^^^^^^^^^^^^^^^^^^^^^

MacOS/UNIX
^^^^^^^^^^

.. code:: bash

    ./docker.sh exec php drush st
