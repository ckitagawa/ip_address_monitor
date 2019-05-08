#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 ckitagawa
#
# Distributed under terms of the MIT license.

import email
import json
import logging
import os
import requests
import smtplib
import time

NO_OP = 0
INFO = 1
ALERT = 2

REMINDER_THRESHOLD_SECS = (6 * 24 + 23) * 3600


def GetExternalIp():
    """Gets External IP from web API."""
    return requests.get('https://api.ipify.org').text


def CheckAndUpdateCache(ip, filename='cache.txt'):
    """Checks cache file and updates. Returns the action to take.

    - Alerts if IP is changed since last run.
    - Sends reminders every REMINDER_THRESHOLD_SECS if IP is unchanged.

    Args:
      ip: the current IP address as a str.
      filename: the filename of the cache file.

    Returns:
      kind of action to take {NO_OP, INFO, ALERT}
    """
    if os.path.exists(filename):
        ret = ALERT
        with open(filename) as f:
            old_ip = f.readline()
        if old_ip.rstrip() == ip:
            ot = os.path.getmtime(filename)
            t = time.time()
            if (t - ot) >= REMINDER_THRESHOLD_SECS:
                ret = INFO
            else:
                return NO_OP
    with open(filename, 'w') as f:
        f.write('{}\n'.format(ip))
    return ret


def SendMessage(msg, usr, pwd, domain='smtp.gmail.com', port=587):
    """Sends an email message via SMTP.

    Args:
      msg: an EmailMessage object with To, From, Subject and content filled in.
      usr: the username for the SMTP service.
      pwd: the password for the SMTP service.
      domain: the SMTP domain (default is GMail).
      port: the SMTP port.

    Returns:
      Nothing, but will log any exceptions that occur.
    """
    try:
        server = smtplib.SMTP(domain, port)
        server.ehlo()
        server.starttls()
        server.login(usr, pwd)
        server.send_message(msg)
    except Exception as e:
        logging.exception('Error in SendMessage: {}'.format(e))


def LoadConfig(filename='conf.json'):
    """Loads configuration file (filename arg)."""
    with open(filename) as f:
        return json.loads(f.read())


def CreateEmail(data, ip, kind):
    """Creates an email with IP address information.

    Args:
      data: a dictionary like object with 'From' and 'To' keys.
      ip: the ip address to send as a str.
      kind: one of {INFO, ALERT} to specify email subject line.

    Returns:
      An EmailMessage object.
    """
    msg = email.message.EmailMessage()
    msg['From'] = data['From']
    msg['To'] = data['To']
    msg.set_content('Currently, the IP address is: {}'.format(ip))

    if kind == INFO:
        msg['Subject'] = 'Info: External IP Address Reminder'
    elif kind == ALERT:
        msg['Subject'] = 'Alert: External IP Address Changed'

    return msg


if __name__ == '__main__':
    ip = GetExternalIp()
    kind = CheckAndUpdateCache(ip)
    if kind != NO_OP:
        data = LoadConfig()
        msg = CreateEmail(data, ip, kind)
        SendMessage(msg, data['usr'], data['pwd'])
