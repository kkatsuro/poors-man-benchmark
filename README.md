# Poor's man benchmark

1. run `download_kernel.sh`
2. change number of threads in `benchmark.sh`
3. you can customize saved metrics from lm_sensors by modifying `sensors_metrics_filter`
4. charge your laptop to 100% battery and unplug
5. run `./benchmark.sh` and wait until laptop goes out of battery
6. use `simple_data_info.py` to check some basic info about benchmark data

If running on laptop, consider changing fan settings to run at 100% (I have some issues on tested thinkpads, it doesn't go even close to 100% RPM, but throttling occurs)
