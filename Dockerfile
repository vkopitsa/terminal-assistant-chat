# syntax=docker/dockerfile:1
FROM ubuntu:jammy

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y python3-pip ddgr sudo apt-utils nmap html2text \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python3", "main.py", "telegram"]