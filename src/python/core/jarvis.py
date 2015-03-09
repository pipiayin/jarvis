#!/usr/bin/env python3
# -*- coding: <encoding name> -*-

# Javis Core

import os
import platform
import socket
import configparser

class Jarvis:
    def __init__(self):
        self.tasks = []
        self.params = {}
        self.prepareConfig()
        self.detectEnv()


    def prepareConfig(self):
        ## read params from possible config file
        try:
            config = configparser.ConfigParser()
            config.read('jarvis.conf')
            self.params['config.file.check'] = True
            allSections =  config.sections()
            for s in allSections:
                if s.startswith('task.'):
                    self.tasks.append(s)
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
        


    def listParams(self):
        return (self.params)


    def listTasks(self):
        return self.tasks


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

#basic task to execute from commandline
class CmdTask(Task):
    def setParams(self, params):
        self.params = params
   
    def do(self):
        try:
            commands.getoutput(self.params['cmd']) 
        except:
            print("can't execute cmd:"+self.params['cmd'])


#######################################################################
# commandline run Jarvis
# 1. list properties, environments...
# 2. list tasks
# 3. pick-up tasks to run
#
if __name__ == '__main__':

    ai = Jarvis()
    print ai.listParams()
    print ai.listTasks()



