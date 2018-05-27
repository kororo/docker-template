FROM wordpress:4.9.6-php7.1-apache

# upgrade packages
RUN apt-get update && apt-get install -y \
    vim wget git iputils-ping telnet

# install composer
RUN wget https://raw.githubusercontent.com/composer/getcomposer.org/1b137f8bf6db3e79a38a5bc45324414a6b1f9df2/web/installer -O - -q | php -- --quiet && \
    mv composer.phar /usr/local/bin/composer && composer global require hirak/prestissimo
RUN composer global require wp-cli/wp-cli
