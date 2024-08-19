FROM public.ecr.aws/lambda/python:3.8

RUN mkdir -p /app
COPY fastapi_app.py flask_app.py requirements.txt supervisord.conf /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8060 8050
CMD ["supervisord", "-c", "/app/supervisord.conf"]