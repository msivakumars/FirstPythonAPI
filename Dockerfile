FROM python:3.12
LABEL authors="SIVA KUMAR MANICKAM"
EXPOSE 5000
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

