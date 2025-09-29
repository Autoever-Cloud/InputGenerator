FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY kmsg_inputgenerator6.py .
EXPOSE 8080
CMD ["python", "kmsg_inputgenerator6.py"]
