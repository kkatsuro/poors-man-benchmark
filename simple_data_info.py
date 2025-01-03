#!/usr/bin/python3
 
import json
import sys

'''
Shows battery information from result of benchmark
'''

def average(some_list):
    return sum(some_list) / len(some_list)
 
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
average_frequency = []
average_temperature = []
average_rpm_speed = []
for line in lines:
    line = json.loads(line)
    try:
        watt_usage = line['sensors'].get('BAT0-acpi-0', {}).get('power1', None)
        watt_usage = float(watt_usage[:-2])
        watt_usage_list.append(watt_usage)
    except:
        pass
 
    try:
        voltage_usage = line['sensors'].get('BAT0-acpi-0', {}).get('in0', None)
        voltage_usage = float(voltage_usage[:-2])
        voltage_usage_list.append(voltage_usage)
    except:
        pass

    try:
        average_frequency.append(sum(line['cpu_frequency'].values()))
    except:
        pass

    try:
        cpu_temp = line['sensors']['thinkpad-isa-0000']['CPU']
        rpm_speed = line['sensors']['thinkpad-isa-0000']['fan1']

        cpu_temp = float(cpu_temp[1:][:-2])
        rpm_speed = int(rpm_speed[:-4])

        average_temperature.append(cpu_temp)
        average_rpm_speed.append(rpm_speed)
    except:
        pass
               
 
hours_up = seconds_up/3600
watt_average = average(watt_usage_list)
voltage_average = average(voltage_usage_list)

average_frequency = average(average_frequency)
average_rpm_speed = average(average_rpm_speed)
average_temperature = average(average_temperature)
 
print(f'laptop was up for {round(hours_up, 2)} hours')
print(f'with average battery usage of: {round(watt_average,2)}W and {round(voltage_average,2)}V')
print(f'battery performance is {round(hours_up*watt_average, 2)}Wh')
print(f'average sum of frequency of all cores at which cpu was running: {round(average_frequency,2)}')
print(f'which means average frequency per core: {round(average_frequency/8, 2)}')
print(f'average RPM of fan: {round(average_rpm_speed,2)}; average temp: {round(average_temperature,2)}')


