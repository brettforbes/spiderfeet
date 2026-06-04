#
# Spiderfeet Dockerfile
#
# http://www.spiderfeet.net
#
# Written by: Michael Pellon <m@pellon.io>
# Updated by: Chandrapal <bnchandrapal@protonmail.com>
# Updated by: Steve Micallef <steve@binarypool.com>
# Updated by: Steve Bate <svc-spiderfeet@stevebate.net>
#    -> Inspired by https://github.com/combro2k/dockerfiles/tree/master/alpine-spiderfoot
#
# Usage:
#
#   sudo docker build -t spiderfeet .
#   sudo docker run -p 5001:5001 --security-opt no-new-privileges spiderfeet
#
# Using Docker volume for spiderfeet data
#
#   sudo docker run -p 5001:5001 -v /mydir/spiderfeet:/var/lib/spiderfeet spiderfeet
#
# Using Spiderfeet remote command line with web server
#
#   docker run --rm -it spiderfeet sfcli.py -s http://my.spiderfeet.host:5001/
#
# Running spiderfeet commands without web server (can optionally specify volume)
#
#   sudo docker run --rm spiderfeet sf.py -h
#
# Running a shell in the container for maintenance
#   sudo docker run -it --entrypoint /bin/sh spiderfeet
#
# Running spiderfeet unit tests in container
#
#   sudo docker build -t spiderfeet-test --build-arg REQUIREMENTS=test/requirements.txt .
#   sudo docker run --rm spiderfeet-test -m pytest --flake8 .

FROM alpine:3.12.4 AS build
ARG REQUIREMENTS=requirements.txt
RUN apk add --no-cache gcc git curl python3 python3-dev py3-pip swig tinyxml-dev \
 python3-dev musl-dev openssl-dev libffi-dev libxslt-dev libxml2-dev jpeg-dev \
 openjpeg-dev zlib-dev cargo rust
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin":$PATH
COPY $REQUIREMENTS requirements.txt ./
RUN ls
RUN echo "$REQUIREMENTS"
RUN pip3 install -U pip
RUN pip3 install -r "$REQUIREMENTS"



FROM alpine:3.13.0
WORKDIR /home/spiderfeet

# Place database and logs outside installation directory
ENV SPIDERFEET_DATA /var/lib/spiderfeet
ENV SPIDERFEET_LOGS /var/lib/spiderfeet/log
ENV SPIDERFEET_CACHE /var/lib/spiderfeet/cache

# Run everything as one command so that only one layer is created
RUN apk --update --no-cache add python3 musl openssl libxslt tinyxml libxml2 jpeg zlib openjpeg \
    && addgroup spiderfeet \
    && adduser -G spiderfeet -h /home/spiderfeet -s /sbin/nologin \
               -g "Spiderfeet User" -D spiderfeet \
    && rm -rf /var/cache/apk/* \
    && rm -rf /lib/apk/db \
    && rm -rf /root/.cache \
    && mkdir -p $SPIDERFEET_DATA || true \
    && mkdir -p $SPIDERFEET_LOGS || true \
    && mkdir -p $SPIDERFEET_CACHE || true \
    && chown spiderfeet:spiderfeet $SPIDERFEET_DATA \
    && chown spiderfeet:spiderfeet $SPIDERFEET_LOGS \
    && chown spiderfeet:spiderfeet $SPIDERFEET_CACHE

COPY . .
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

USER spiderfeet

EXPOSE 5001

# Run the application.
ENTRYPOINT ["/opt/venv/bin/python"]
CMD ["sf.py", "-l", "0.0.0.0:5001"]
