# IP Address Monitor

A simple external IP address monitoring solution that sends an email when the
external IP address is changed and a configurable reminder that is sent
periodically if the IP hasn't changed.

## Usage

Clone the repository and fill in the fields in the `conf.json` file as
outlined. The `usr` and `pwd` fields are for logging into the SMTP server.
Ideally, the `pwd` field or the entire `conf.json` would be encrypted...

If using Gmail I recommend creating a new dev account. You need to turn on
access for Less Secure Apps or if using 2FA get a token. The latter case
requires rewriting some of the SMTP code. If not using Gmail the SMTP domain in
the `ip_addr_mon.py` script needs to be updated.

Copy the following bash script and fill out the fields.

```bash
#!/usr/bin/sh

cd <directory>
/usr/bin/python <directory>/ip_addr_mon.py
```

Schedule a cron job to run at the desired monitoring frequency that runs the
aforementioned script. Use Crontab on Linux for example.

Good devices for this to run on are a server, BeagleBone or RaspberryPi.

## Motivation

It isn't always possible to get a static external IP as a non-business
customer. Some IOT, home entertainment servers and home security devices
require you to address/access them via IP. If away from home, checking your
external IP can be a hassle/challenge. This monitoring solution allows for
periodic checks to your external IP when away from home and alerting via email,
which is simple enough that anyone can use it.

## Requirements

Python 3, and the requests package (sometimes not in the default installation).

In theory this should work on any device that runs Python (Linux, Windows,
MacOS). Although I've only tested it on low power Linux devices.

