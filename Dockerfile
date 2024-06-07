FROM ubuntu:20.04

RUN apt-get update && \
    apt-get -y install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get -y install python3.9 && \
    ln -sfn /usr/bin/python3.9 /usr/bin/python3 && \
    apt-get -y install python3-pip && \
    apt-get -y clean

RUN DEBIAN_FRONTEND=noninteractive apt-get -y install ca-certificates curl --no-install-recommends && \
    curl -H 'Cache-Control: no-cache' \
        https://raw.githubusercontent.com/nimbix/jarvice-desktop/master/install-nimbix.sh \
        | bash

# APP
COPY --chmod=755 poetry.lock pyproject.toml README.md /tmp/jarvice_cli/
COPY --chmod=755 jarvice_cli /tmp/jarvice_cli/jarvice_cli

RUN pip3 install /tmp/jarvice_cli

COPY NAE/ /etc/NAE/
RUN curl --fail -X POST -d @/etc/NAE/AppDef.json https://cloud.nimbix.net/api/jarvice/validate
