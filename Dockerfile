FROM            gambler1541/yapen-docker-hub:base
MAINTAINER      gambler1541@gmail.com


# production
ENV             BUILD_MODE              production
ENV             DJANGO_SETTINGS_MODULE  config.settings.${BUILD_MODE}
ENV             PROJECT_DIR             /srv/project


RUN             mkdir /var/log/django


COPY            .   ${PROJECT_DIR}
WORKDIR         ${PROJECT_DIR}


# Nginx 설정파일들 복사 및 enabled로 링크
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/nginx.conf \
                        /etc/nginx/nginx.conf && \
                cp -f   /srv/project/.config/${BUILD_MODE}/nginx_app.conf \
                        /etc/nginx/sites-available/ && \
#                rm -f   /etc/nginx/sites-enabled/* && \
                ln -s  /etc/nginx/sites-available/nginx_app.conf \
                        /etc/nginx/sites-enabled/

RUN             mv /srv/project/front/*     /srv/front/

# supervisor설정 복사
RUN             cp -f   /srv/project/.config/${BUILD_MODE}/supervisor.conf \
                        /etc/supervisor/conf.d/

EXPOSE          7000
WORKDIR         /srv/front
# supervisord실행
CMD             pkill nginx; supervisord -n