#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Javis Core

import os
import sys
import platform
import socket
import configparser

#simple function to get class via name
def get_class(kls):
    thismodule = sys.modules[__name__]
    parts = kls.split('.')
    if len(parts) <= 1:
        return getattr(thismodule, 'CmdTask')
    else:
        module = ".".join(parts[:-1])
        m = __import__( module )
        for comp in parts[1:]:
            m = getattr(m, comp)            
        return m

class Jarvis:
    def __init__(self):
        #try to add package path  
        workingPath = os.getcwd()
        absPath = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(workingPath)
        sys.path.append(absPath)
        if absPath.endswith("/core"):
            sys.path.append(absPath[0:-5])

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
            self.config = config
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


    def doTask(self, taskClass):
        taskConfig = self.config.items(taskClass)
        configParams = {}
        for k,v in taskConfig:
            configParams[k] = v

        #print configParams
        #print configParams['class']

        taskClass = get_class(configParams[u'class'])
        task = taskClass()
        task.setParams(configParams.copy())
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
            import commands
            print commands.getoutput(self.params['cmd']) 
        except:
            print('except...')
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
    for task in ai.listTasks():
        ai.doTask(task)



