#!/bin/bash

set -u

THREADS=8

date_command() {
    date -u +%Y-%m-%dT%H:%M:%S
}

./monitor.py &

pushd linux

logfile_name="compile_log_$(date_command)"

i=1
while true; do
    make clean
    echo "build $i; $(date_command)" >> "../${logfile_name}"
    make -j"$THREADS"
    ((i++))
done

popd
