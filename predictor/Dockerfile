FROM python:slim AS builder
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]
