FROM python:3

WORKDIR /app
COPY ./test/requirements.txt ./
RUN pip install -r requirements.txt
CMD ["python", "-m", "unittest", "discover", "--verbose", "test"]
