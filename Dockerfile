FROM python:3.6

ARG PORT=8000

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE ${PORT}

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]
CMD [ "./web/manage.py", "runserver", "0.0.0.0:${PORT}", "--noreload" ]
