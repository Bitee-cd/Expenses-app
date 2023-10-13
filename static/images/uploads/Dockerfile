FROM python:3.8
WORKDIR /fastapiapp
COPY ./backend/ ./fastapiapp
RUN pip install -r fastapiapp/requirements.txt
ENV FASTAPI_APP=docker_fastapi.py
EXPOSE 8000
CMD ["uvicorn","fastapiapp.docker_fastapi:app","--reload","--host","0.0.0.0"]
