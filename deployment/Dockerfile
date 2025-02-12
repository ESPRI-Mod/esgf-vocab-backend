FROM python:3.12-alpine AS esgvoc-backend

RUN apk update && apk upgrade && apk add git

WORKDIR /var/www
ADD https://github.com/ESPRI-Mod/esgf-vocab-backend.git#main esgvoc-backend

WORKDIR /var/www/esgvoc-backend
RUN pip install .

RUN esgvoc install

CMD ["python","-c","from esgvoc_backend.start import main; main()"]
