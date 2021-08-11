FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN make

EXPOSE 9100

CMD [ "python", "./web/manage.py runserver 0.0.0.0:9100 --noreload" ]
