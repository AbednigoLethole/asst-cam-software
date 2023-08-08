#/bin/bash

### Enable virtual CAN interface
ip link add dev can0 type vcan
ip link set up can0
ip link show can0
