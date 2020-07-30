FROM python:3.6

ENV PORT=8111

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE $PORT

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]