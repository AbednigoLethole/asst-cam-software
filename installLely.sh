#!/bin/sh
cd /app
git clone https://gitlab.com/lely_industries/lely-core.git
cd lely-core
autoreconf -i
mkdir -p build
cd build
../configure --disable-cython --prefix /usr/
make
make install
