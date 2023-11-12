# Using the official Ubuntu base image
FROM ubuntu:20.04

# Setting environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Apt update
RUN apt-get update -y
RUN apt-get install software-properties-common -y

# Getting Lely canopen 
RUN add-apt-repository ppa:lely/ppa -y

# Updating package list and installing Python 3.10
RUN apt-get install -y python3.10 python3-pip iproute2 can-utils pkg-config software-properties-common liblely-coapp-dev liblely-co-tools python3-dcf-tools

# Setting the working directory
WORKDIR /app

# Copying asst code into the container
COPY . /app

# Installing Python dependencies
RUN pip3 install poetry && poetry install  
