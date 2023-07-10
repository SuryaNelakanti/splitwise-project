FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . /app/

CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--reload"]