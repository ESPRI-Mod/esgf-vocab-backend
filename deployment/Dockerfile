FROM python:3.12.3-alpine AS esgvoc-backend

RUN apk update && apk upgrade

WORKDIR /var/www
ADD https://github.com/ESPRI-Mod/esgf-vocab-backend.git#main esgvoc-backend

WORKDIR /var/www/esgvoc-backend
RUN pip install .

CMD ["python","-c","from esgvoc_backend.start import main; main()"]
