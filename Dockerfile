# Using the official Ubuntu base image
FROM ubuntu:20.04

# Setting environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Updating package list and installing Python 3.10
RUN apt-get update && apt-get install -y python3.10 python3-pip iproute2 can-utils pkg-config software-properties-common

# Setting the working directory
WORKDIR /app

# Copying asst code into the container
COPY . /app

# Installing Python dependencies
RUN pip3 install poetry && poetry install  
