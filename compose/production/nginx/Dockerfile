FROM nginx:alpine

RUN chmod -R a+w /var/log/nginx
COPY nginx.conf /etc/nginx/conf.d/

EXPOSE 80

CMD ["nginx"]
