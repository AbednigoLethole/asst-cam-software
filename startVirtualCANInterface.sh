#/bin/bash

### Enable virtual CAN interface
sudo modprobe vcan
sudo ip link add dev can0 type vcan
sudo ip link set up can0
sudo ip link show can0
