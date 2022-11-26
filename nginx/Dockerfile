FROM nginx:1.17
ADD conf /etc/nginx/conf.d
ADD uwsgi_params /etc/nginx/uwsgi_params

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stdout /var/log/nginx/error.log