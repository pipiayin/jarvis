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
        self.prepareConfig()
        self.detectEnv()


    def prepareConfig(self):
        ## read params from possible config file
        try:
            config = configparser.ConfigParser()
            config.read('jarvis.conf')
            self.params['config.file.check'] = True
        except:
            self.params['config.file.check'] = False

    def detectEnv(self):
        ## detect environment
        self.params['platform.system'] = platform.system()
        try:
            if len(socket.getaddrinfo('whitehouse.gov', 80)) >= 1:
                self.params['internet.check'] = True
        except:
                self.params['internet.check'] = False
        

    def showParams(self):
        print(self.params)


    def doTask(self, task):
        task.setParams(self.params)
        task.do()
        

# Task for javis
class Task:
    def setParams(self, params):
        raise NotImplementedError("Should have implemented 'setParams'")
    
    def do(self):
        raise NotImplementedError("Should have implemented 'do'")


#basic task, to install necessary packages
class InstallPackages(Task):
    def setParams(self, params):
        self.params = params

    def do(self):
        if self.params['internet.check'] :
            commands.getoutput("apt-get install python3")
# 
if __name__ == '__main__':
    ai = Jarvis()
    ai.showParams()
