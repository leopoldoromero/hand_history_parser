# FROM python:3.9-slim

# WORKDIR /app

# RUN pip install --no-cache-dir poetry

# COPY pyproject.toml ./

# RUN poetry install --no-root

# COPY . .

# EXPOSE 8000

# CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]


FROM public.ecr.aws/lambda/python:3.10

WORKDIR /app

ARG DEBIAN_FRONTEND=noninteractive

RUN yum update -y
RUN yum install -y ffmpeg libsm6 libxext6 python3-pip git

COPY . .

RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

ENV PYTHONPATH=${LAMBDA_TASK_ROOT}

COPY . ${LAMBDA_TASK_ROOT}

CMD ["app.main.handler"]
