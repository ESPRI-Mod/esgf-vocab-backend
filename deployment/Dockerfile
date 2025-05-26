FROM python:3.13-alpine AS esgvoc-backend

RUN apk update && apk upgrade && apk add git

ARG UID=2000 # Default value.
ARG GID=2000 # Default value.
ARG USER="docker" # Default value.
ARG GROUP="${USER}"
RUN addgroup -S -g ${GID} "${GROUP}" && adduser -S -u ${UID} -G "${GROUP}" "${USER}"

WORKDIR "/home/docker"
ADD https://github.com/ESPRI-Mod/esgf-vocab-backend.git#main esgvoc-backend

WORKDIR "/home/docker/esgvoc-backend"
RUN pip install . # Install packages/scripts in every one path. Scripts are in /usr/local/bin

USER ${UID}
RUN esgvoc install

CMD ["python","-c","from esgvoc_backend.start import main; main()"]
