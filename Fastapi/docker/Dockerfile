##base image
# Use the lightweight Python base image
FROM python:3.11-slim

##  working dir
WORKDIR /app

# #copy
COPY requirements.txt .

##run
RUN pip install -r requirements.txt

COPY . .

## port
EXPOSE 5000

#command
CMD ["python","./flaskapp_gemini.py"]
