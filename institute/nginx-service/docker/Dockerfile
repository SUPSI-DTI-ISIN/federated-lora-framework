FROM nginx:1.29.4-alpine

COPY docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY nginx/nginx.conf.template /etc/nginx/templates/

EXPOSE 80
CMD ["/docker-entrypoint.sh"]