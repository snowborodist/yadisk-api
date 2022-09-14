FROM python:3.10

WORKDIR /code

# Copy utils
COPY ./deploy/wait-for-it /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Copy and install requirements
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy code
COPY . .
COPY ./deploy/entrypoint.sh ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/code/entrypoint.sh"]