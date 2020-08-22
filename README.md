# DSMR docker config

This repository is a simple docker configuration for scraping and visualising metrics which adhere to the DSMR (Dutch Smart Reader) standard. It deploys:

- Metrics scraper (sbkg0002)
- Prometheus
- Grafana

## Setup

You need to connect your device to your smart meter using an USB-RJ11 FT232R cable. These are relatively easy to come by, just google DSMR brand/model and FT232R.

Set up different credentials if needed in grafana/config.monitoring.

Once you've connected your device to your smartmeter, just run docker-compose up -d.
You can access Grafana by using <ip>:3000 and Prometheus by using <ip>:9090.

This repo is basically an opensource alternative to P1 Monitor.

Thanks to sbkg0002 for the metrics container.
