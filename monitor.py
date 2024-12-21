#!/usr/bin/python3

import time
import subprocess
import json

def ignore_failure(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except:
            return 'N/A'
        return result
    return inner

@ignore_failure
def parse_cpuinfo():
    '''
    returns frequency for each core, could be modified to actually do whole cpuinfo
    '''
    with open('/proc/cpuinfo', 'r') as f:
        cores = f.read().split('\n\n')[:-1]

    cores_dict = {}
    for core in cores:
        split = [ line.split(': ', maxsplit=1) for line in core.splitlines() if ': ' in line ]
        core = { name.rstrip(): value for name, value in split }
        cores_dict[core['processor']] = core

    return { core: float(data['cpu MHz']) for core, data in cores_dict.items() }


@ignore_failure
def get_memory():
    result = subprocess.run(['free', '-m'], stdout=subprocess.PIPE)
    columns, mem, swap = result.stdout.decode().splitlines()

    total, used, free, shared, buff_cache, available = [ int(x) for x in mem.split()[1:] ]
    swap_total, swap_used, swap_free = [ int(x) for x in swap.split()[1:] ]

    memdict = {
        'memory': {
            'total': total,
            'used': total - available
        },
        'swap': {
            'total': swap_total,
            'used': swap_used
        }
    }

    return memdict


@ignore_failure
def get_iostat_cpu():
    result = subprocess.run(['iostat', '-c'], stdout=subprocess.PIPE)

    # parsing this output of command:
    #  avg-cpu:  %user   %nice %system %iowait  %steal   %idle
    #             1,53    0,00    0,81    0,03    0,00   97,63

    columns, values = result.stdout.decode().splitlines()[2:4]
    columns = [ c[1:] for c in columns.split()[1:] ]  # remove avg-cpu column and % from name
    values = [ float(v.replace(',', '.')) for v in values.split() ]
    return { k:v for k, v in zip(columns, values) }


@ignore_failure
def sensors_parse_single_metric(metric):
    metric = metric.splitlines()
    metric_name, adapter, values = metric[0], metric[1], metric[2:]
    
    metric_dict = {}
    for line in values:
        if line[0] == ' ':  # sometimes you get lines which are continuation of previous line info, ignore them
            continue
        name, value = line.split(':  ')
        value = value.strip()

        # in case of lines like: Sensor 1:     +41.9°C  (low  = -273.1°C, high = +65261.8°C)
        # ignore that low/high information
        if '  ' in value:  
            value, _ = value.split('  ', maxsplit=1) 

        # @todo: parse value from string
        metric_dict[name] = value

    return metric_name, metric_dict


@ignore_failure
def get_sensors(metrics_filter=None):
    result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
    metrics = result.stdout.decode().split('\n\n')[:-1]
    metrics_dict = {}
    for metric in metrics:
        name, value = sensors_parse_single_metric(metric)
        if metrics_filter and name not in metrics_filter:
            continue
        metrics_dict[name] = value

    return metrics_dict

def main():
    sensors_metrics_filter = [ 'amdgpu-pci-2600', 'k10temp-pci-00c3' ]
    while True:
        # get all the metrics
        stats = {
            'timestamp': time.time(),
            'cpu_frequency': parse_cpuinfo(),
            'iostat': get_iostat_cpu(),
            'sensors': get_sensors(sensors_metrics_filter),
            'memory_info': get_memory()  # @todo: make ignore_failure decorator work with **get_memory()
        }
        time.sleep(1)

        with open('benchmark_data', 'a') as f:
            f.write(json.dumps(stats)+'\n')

if __name__ == '__main__':
    main()
