FROM public.ecr.aws/lambda/python:3.10

WORKDIR /var/task

COPY lambda_function.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD ["lambda_function.lambda_handler"]