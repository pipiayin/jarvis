#!/usr/bin/env python3
# -*- coding: <encoding name> -*-

# Javis

import os
import platform
import socket
import configparser

class Jarvis:
    def __init__(self):
        self.params = {}
        self.prepare_config()
        self.detect_env()

    def prepare_config(self):
        ## read params from possible config file
        try:
            config = configparser.ConfigParser()
            config.read('jarvis.conf')
            self.params['config.file.check'] = True
        except:
            self.params['config.file.check'] = False

    def detect_env(self):
        ## detect environment
        self.params['platform.system'] = platform.system()
        try:
            if len(socket.getaddrinfo('whitehouse.gov', 80)) >= 1:
                self.params['internet.check'] = True
        except:
                self.params['internet.check'] = False
        

    def show_params(self):
        print(self.params)

# Task for javis
class Task:
    pass

# 
if __name__ == '__main__':
    ai = Jarvis()
    ai.show_params()
