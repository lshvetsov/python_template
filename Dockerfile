FROM public.ecr.aws/lambda/python:3.8

RUN mkdir -p /app
COPY . fastapi.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8060
CMD [ "fastapi.py" ]
ENTRYPOINT [ "python" ]