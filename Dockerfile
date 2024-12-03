FROM python:3.11.10-alpine3.20

# Set the working directory
COPY ./app /app
WORKDIR /app


# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]