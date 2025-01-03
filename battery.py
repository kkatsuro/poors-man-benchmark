#!/usr/bin/python3
 
import json
import sys

'''
Shows battery information from result of benchmark
'''
 
if len(sys.argv) > 1:
    benchmark_file = sys.argv[1]
else:
    benchmark_file = 'benchmark_data'
 
with open(benchmark_file, 'r') as f:
    lines = f.read().splitlines()
 
start, end = lines[0], lines[-1]
seconds_up = float(json.loads(end)['timestamp']) - float(json.loads(start)['timestamp'])
 
watt_usage_list = []
voltage_usage_list = []
for line in lines:
    try:
        watt_usage = json.loads(line)['sensors'].get('BAT0-acpi-0', {}).get('power1', None)
        watt_usage = float(watt_usage[:-2])
        watt_usage_list.append(watt_usage)
    except:
        pass
 
    try:
        voltage_usage = json.loads(line)['sensors'].get('BAT0-acpi-0', {}).get('in0', None)
        voltage_usage = float(voltage_usage[:-2])
        voltage_usage_list.append(voltage_usage)
    except:
        pass
 
 
hours_up = seconds_up/3600
watt_average = sum(watt_usage_list) / len(watt_usage_list)
voltage_average = sum(voltage_usage_list) / len(voltage_usage_list)
 
print(f'laptop was up for {round(hours_up, 2)} hours')
print(f'with average battery usage of: {round(watt_average,2)}W and {round(voltage_average,2)}V')
print(f'battery performance is {round(hours_up*watt_average, 2)}Wh')
