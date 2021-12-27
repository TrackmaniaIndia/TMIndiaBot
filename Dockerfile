FROM python:3.9-slim

WORKDIR /bot 

COPY . .

CMD [ "python3", "-m", "bot"]