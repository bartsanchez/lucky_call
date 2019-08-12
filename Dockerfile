FROM debian:stable-slim

RUN apt update && \
    apt install -y python3-pip \
                   python3-psycopg2

RUN mkdir -p /opt/luckycall/
WORKDIR /opt/luckycall

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /opt/luckycall/

ENV DJANGO_SETTINGS_MODULE lucky_call.settings.prod

WORKDIR /opt/luckycall/lucky_call/

CMD /opt/luckycall/entrypoint.sh
