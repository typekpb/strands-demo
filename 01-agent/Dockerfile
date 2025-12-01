FROM public.ecr.aws/lambda/python:3.14

WORKDIR /var/task

COPY lambda_function.py agent.py requirements.txt ./

RUN python3.14 -m pip install --upgrade pip \
    && python3.14 -m pip install -r requirements.txt -t .

CMD ["lambda_function.lambda_handler"]
