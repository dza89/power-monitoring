from prometheus_client import start_http_server, Gauge
import time
import datetime
import sys
import serial
import logging
from smeterd.meter import SmartMeter


# Definitions
electricity_consumed_total = Gauge('electricity_consumed_total', 'Electricity consumption total year-to-date')
electricity_consumed_low = Gauge('electricity_consumed_low', 'Electricity consumption tariff low year-to-date')
electricity_consumed_high = Gauge('electricity_consumed_high', 'Electricity consumption tariff high year-to-date')
electricity_produced_total = Gauge('electricity_produced_total', 'Electricity produced total year-to-date')
electricity_produced_low = Gauge('electricity_produced_low', 'Electricity produced tariff low year-to-date')
electricity_produced_high = Gauge('electricity_produced_high', 'Electricity produced tariff high year-to-date')
gas_consumed_total = Gauge('p1_total_gas_used', 'Gas consumption total year-to-date')

def get_p1_metrics(p1_lines):
    # Convert to a list for simple parsing
    p1_list = str(p1_lines).splitlines()

    for p1_line in p1_list:
        match p1_line:
            case '1-0:1.8.1':
                logging.debug("[{}] electricity_consumed_low: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                electricity_consumed_low.set(markup_helper(p1_line))
            case '1-0:1.8.2':
                logging.debug("[{}] electricity_consumed_high: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                electricity_consumed_high.set(markup_helper(p1_line))
            case '1-0:2.8.1':
                logging.debug("[{}] electricity_produced_low: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                electricity_produced_low.set(markup_helper(p1_line))
            case '1-0:2.8.2':
                logging.debug("[{}] electricity_produced_high: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                electricity_produced_high.set(markup_helper(p1_line))
            case '1-0:1.7.0':    
                logging.debug("[{}] electricity_consumed_total: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                electricity_consumed_total.set(markup_helper(p1_line))
            case '1-0:2.7.0':   
                logging.debug("[{}] electricity_produced_total: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                electricity_produced_total.set(markup_helper(p1_line))
            case '0-1:24.2.1':      
                logging.debug("[{}] gas_consumed_total: {}" .format(datetime.datetime.now(), markup_helper(p1_line)))
                gas_consumed_total.set(markup_helper(p1_line))

def markup_helper(str_line):
    '''
    Read raw string and return only the value
    '''
    return int(str_line.split('(')[-1].split('*')[0].replace('.',''))


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        try:
            # Define device
            meter = SmartMeter('/dev/ttyUSB0', baudrate=115200)
            get_p1_metrics(meter.read_one_packet())
            meter.disconnect()
        except:
            sys.exit ("Serial port cannot be read. Will try again.")
        time.sleep(5)
