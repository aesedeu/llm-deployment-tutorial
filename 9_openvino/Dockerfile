FROM openvino/ubuntu20_dev:latest

# Install required Python packages
COPY requirements.txt /app/requirements.txt
WORKDIR /app

RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# Expose the port for the server
EXPOSE 8000

# Start the server
CMD ["python3", "server.py"] 