FROM nginx:1.15.8

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/
EXPOSE 80
ENV APP_HOST flask_app
ENV APP_PORT 5000
CMD ["nginx", "-g", "daemon off;"]