FROM nginx

ADD nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/media
RUN mkdir -p /var/www/static

WORKDIR /var/lib/media
RUN chown -R nginx:nginx /var/lib/media

WORKDIR /var/lib/static
RUN chown -R nginx:nginx /var/lib/static
