FROM python:3.10-slim

# used https://www.caktusgroup.com/blog/2017/03/14/production-ready-dockerfile-your-python-django-app/ for inspiration

# Create a group and user to run our app

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
#   postgresql-client -- for running database commands
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}

RUN set -ex \
    && RUN_DEPS=" \
    libpcre3 \
    mime-support \
    libmariadb-dev-compat \
    libmariadb-dev \
    mariadb-client \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
ADD ticket_scheduler_app/requirements.txt /requirements.txt

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
# ADD requirements /requirements

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    libpcre3-dev \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /code/
WORKDIR /code/
ADD ./ticket_scheduler_app/ /code/
RUN chown -R appuser:appuser /code/

# uWSGI will listen on this port
EXPOSE 8045

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=ticket_scheduler.settings


# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=ticket_scheduler/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTPS=:8045 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/assets/=/code/assets/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start uWSGI
CMD ["uwsgi", "--module", "ticket_scheduler.wsgi"]
#CMD ["python", "./manage.py", "runserver", "0.0.0.0:8045", "--settings=ticket_scheduler.settings"]
