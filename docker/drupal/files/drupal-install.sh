#!/usr/bin/env bash

# just reload the env
. ~/.bashrc

# copy bootstrap
cp -r /script/startup/. /var/www/html/

# install dependencies
composer install

# drush magic
drush si --db-url=mysql://drupal:Password1@mysql/drupal --account-mail=robertus.johansyah@sl.nsw.gov.au --account-name=core --account-pass=rob! --site-mail=robertus.johansyah@sl.nsw.gov.au --site-name=D8 --yes
