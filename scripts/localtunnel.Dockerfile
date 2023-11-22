# Start with an Ubuntu base image
FROM ubuntu:latest

# Update and install necessary packages
RUN apt-get update && \
    apt-get install -y curl python3-pip

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash - && \
    apt-get install -y nodejs

# Install localtunnel globally
RUN npm install -g localtunnel

# Install AWS CLI
RUN pip3 install awscli

# Create app directory
WORKDIR /usr/src/app

# Copy the script that runs localtunnel and updates AWS Lambda
COPY run_localtunnel_and_update_lambda.sh .

# Grant execution rights to the script
RUN ["chmod", "+x", "/usr/src/app/run_localtunnel_and_update_lambda.sh"]

# Expose the required port
EXPOSE 8000

# Command to run the script
CMD ["/bin/sh", "-c", "./run_localtunnel_and_update_lambda.sh"]

