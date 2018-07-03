FROM php:7.1.17-apache

# upgrade packages
RUN apt-get update && \
    apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev libmcrypt-dev libcurl4-openssl-dev libxml2-dev \
    vim wget git mysql-client

# install PHP extensions
# curl dom fileinfo iconv json mbstring pdo xml
RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ && \
    docker-php-ext-install gd && \
    docker-php-ext-install bcmath exif mcrypt mysqli pdo_mysql soap zip 2>&1 > /dev/null

# setup Apache
RUN a2enmod rewrite
COPY ./files/php.ini /usr/local/etc/php/
COPY ./files/d8.conf /etc/apache2/sites-available/000-default.conf

# install composer
RUN wget https://raw.githubusercontent.com/composer/getcomposer.org/1b137f8bf6db3e79a38a5bc45324414a6b1f9df2/web/installer -O - -q | php -- --quiet && \
    mv composer.phar /usr/local/bin/composer && \
    composer global require hirak/prestissimo && \
    echo 'export PATH="$PATH:$HOME/.composer/vendor/bin"' >> ~/.bashrc && \
    . ~/.bashrc

# install drush
RUN composer global require drush/drush ^9.2

# fix permission
RUN usermod -u 1000 www-data
