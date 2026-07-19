# base image
FROM python:3.14-slim

# worddir 
WORKDIR /app

# copy
COPY . /app

# run
RUN pip install --no-cache-dir -r requirements.txt

# port
EXPOSE 8000

# command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]