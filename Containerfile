FROM docker.io/library/alpine:3.18

RUN :\
    && install -d -o 1000 -g 1000 /pystebin \
    && adduser -h /pystebin -D -s /bin/sh -H -u 1000 pystebin \
    && apk --update add --upgrade --no-cache \
    python3 python3-dev py3-pip libpq build-base

USER pystebin

COPY --chown=1000:1000 . /pystebin

RUN pip install --user --no-warn-script-location /pystebin

LABEL org.opencontainers.image.source https://github.com/pwr-pro/websec

CMD [ "/pystebin/.local/bin/pystebin" ]
