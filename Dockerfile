FROM ubuntu:20.04

RUN apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get -y install python3.9 python3-pip && \
    apt-get -y clean

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install ca-certificates curl --no-install-recommends && \
    curl -H 'Cache-Control: no-cache' \
        https://raw.githubusercontent.com/nimbix/jarvice-desktop/master/install-nimbix.sh \
        | bash

# APP
COPY poetry.lock pyproject.toml jarvice_cli /tmp/
RUN cd /tmp/ && pip3 install .

COPY NAE/ /etc/NAE/
RUN curl --fail -X POST -d @/etc/NAE/AppDef.json https://cloud.nimbix.net/api/jarvice/validate
