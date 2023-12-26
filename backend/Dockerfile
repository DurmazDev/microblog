FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
ENV MONGO_URI=mongodb://mongo:27017/microblog
ENV REDIS_URI=redis://redis:6379/0
CMD ["python", "run.py"]