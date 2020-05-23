FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python3 web/manage.py migrate \
    && python3 web/manage.py loaddata dpstype \
    && python web/manage.py createsuperuser --username admin --password admin --email admin@admin.com

CMD [ "python", "./web/manage.py runserver" ]