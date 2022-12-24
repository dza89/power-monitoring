from prometheus_client import start_http_server, Gauge
import time
import datetime
import sys
import serial
import logging
from smeterd.meter import SmartMeter


# Definitions
electricity_consumption = Gauge('electricity_consumption_current', 'Current electricity consumption in 1 Watt resolution')
electricity_consumed_low = Gauge('electricity_consumed_low', 'Electricity consumed, tariff low, in 0,001 kWh')
electricity_consumed_high = Gauge('electricity_consumed_high', 'Electricity consumed, tariff high, in 0,001 kWh')
electricity_production = Gauge('electricity_production_current', 'Current electricity production in 1 Watt resolution')
electricity_produced_low = Gauge('electricity_produced_low', 'Electricity produced, tariff low, in 0,001 kWh')
electricity_produced_high = Gauge('electricity_produced_high', 'Electricity produced, tariff high, in 0,001 kWh')
gas_consumption = Gauge('gas_consumption', 'Gas consumption in mˆ3')

logging.debug('electricity_consumed_low: %s' 'test')

def get_p1_metrics(p1_lines):
    # Convert to a list for simple parsing
    p1_list = str(p1_lines).splitlines()

    for p1_line in p1_list:
        logging.debug("%s", p1_line)
        match p1_line:
            case '1-0:1.8.1.255':
                logging.info("electricity_consumed_low: %s", markup_helper(p1_line))
                electricity_consumed_low.set(markup_helper(p1_line))
            case '1-0:1.8.2.255':
                logging.info("electricity_consumed_high: %s", markup_helper(p1_line))
                electricity_consumed_high.set(markup_helper(p1_line))
            case '1-0:2.8.1.255':
                logging.info("electricity_produced_low: %s", markup_helper(p1_line))
                electricity_produced_low.set(markup_helper(p1_line))
            case '1-0:2.8.2.255':
                logging.info("electricity_produced_high: %s", markup_helper(p1_line))
                electricity_produced_high.set(markup_helper(p1_line))
            case '1-0:1.7.0.255':    
                logging.info("electricity_production: %s", markup_helper(p1_line))
                electricity_production.set(markup_helper(p1_line))
            case '1-0:2.7.0.255':   
                logging.info("electricity_consumption: %s", markup_helper(p1_line))
                electricity_consumption.set(markup_helper(p1_line))
            case '0-1:24.2.1.255':      
                logging.info("gas_consumption: %s", markup_helper(p1_line))
                gas_consumption.set(markup_helper(p1_line))

def markup_helper(str_line):
    '''
    Read raw string and return only the value
    '''
    return int(str_line.split('(')[-1].split('*')[0].replace('.',''))


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    logging.basicConfig(format='%(asctime)s %(message)s')
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
