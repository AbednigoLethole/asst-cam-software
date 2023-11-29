#!/bin/sh

cd /app/src/antenna_simulator

g++ -std=c++14 -Wall -Wextra -pedantic -g -O2 \
    $(pkg-config --cflags liblely-coapp) \
    slave.cpp \
    AntennaSimulate.cpp \
    PidController.cpp \
    -o slave \
    $(pkg-config --libs liblely-coapp) -pthread