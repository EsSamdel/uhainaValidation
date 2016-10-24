# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:14:40 2015

@author: simon
"""

import os
import datetime
from XmlHandler import *
from ConfigTemplate import generateConfigFile


class PathStudy(dict):
    __directories = ['MESH', 'EXE', 'DATA', 'CONFIG']

    def __init__(self, name=None, **kwargs):
        super(PathStudy, self).__init__(**kwargs)

        self.exePath = ''
        self.name = name
        if name is None:
            self.rootPath = os.getcwd()
        else:
            self.rootPath = os.getcwd() + '/' + name

        for iName in PathStudy.__directories:
            self.update({iName: self.rootPath + '/' + iName})

    def getRootPath(self):
        return self.rootPath

    def setRootPath(self, path):
        self.rootPath = path
        for iName in PathStudy.__directories:
            self.update({iName: self.rootPath + '/' + iName})

    def createTree(self):
        assert (self.name is not None), "Error : Cannot create study without name!"
        try:
            os.makedirs(self.rootPath)
        except OSError:
            print 'Warning : Study : ', self.rootPath, ' already exist!'
            self.checkingTree()
            return

        for key, value in self.iteritems():
            try:
                os.makedirs(value)
            except OSError:
                print 'Error : ', value, ' already exist!'
                sys.exit()

        self.checkingTree()

    def checkingTree(self):
        for key, value in self.iteritems():
            if not os.path.exists(value):
                print "Error :: Study ", self.rootPath, " not correctly set! (missing : ", value, ")"
                sys.exit()

    def create(self, exePath):
        self.exePath = exePath
        self.createTree()

        generateConfigFile(self.get('CONFIG'))
        xmlHandler = XmlHandler(self.get('CONFIG') + '/config.xml')
        xmlHandler.setAttribute('mesh', 'sparam', 'file', self.get('MESH'))
        xmlHandler.write(self.get('CONFIG') + '/config.xml')

        try:
            os.symlink(exePath, self.get('EXE') + '/' + exePath.split("/")[-1])
        except OSError:
            print 'Error : Path to exe seems incorrect : ', exePath


class PathCase(dict):
    __directories = ['restart', 'visu', 'stat']

    def __init__(self, studyPath, name=None, **kwargs):
        super(PathCase, self).__init__(**kwargs)

        self.studyPath = studyPath

        if name is None:
            now = datetime.datetime.now()
            self.name = now.strftime("%d-%m-%Y_%H:%M")
        else:
            self.name = name

        self.rootPath = self.studyPath.getRootPath() + '/' + self.name
        if os.path.isdir(self.rootPath):
            i = 0
            name = ""
            while os.path.isdir(self.rootPath):
                name = self.name + "_run" + str(i)
                self.rootPath = self.studyPath.getRootPath() + '/' + name
            self.name = name

        for iName in PathCase.__directories:
            self.update({iName: self.rootPath + '/' + iName})

    def createTree(self):
        assert (self.name != ''), "Error : Cannot create study without a name!"

        self.studyPath.checkingTree()
        try:
            os.makedirs(self.rootPath)
        except OSError:
            print 'Warning : Case ', self.rootPath, ' already exist!'
            # sys.exit()

        for key, value in self.iteritems():
            try:
                os.makedirs(value)
            except OSError:
                print 'Warning : ', value, ' already exist!'
                # sys.exit()

        self.checkingTree()
        self.copyingConfigFile()
        self.linkingToExe()

    def checkingTree(self):
        for key, value in self.iteritems():
            if not os.path.exists(value):
                print "Error : In Case ", self.rootPath, ", ", value, " is missing)"
                sys.exit()

    def copyingConfigFile(self):
        xmlHandler = XmlHandler(self.studyPath['CONFIG'] + '/config.xml')
        xmlHandler.setAttribute('mesh', 'sparam', 'file', '../MESH/')
        xmlHandler.setAttribute('aerosol', 'sparam', 'visutype', 'points')
        xmlHandler.setAttribute('aerosol', 'sparam', 'output_path', './visu')
        xmlHandler.setAttribute('aerosol', 'sparam', 'restartPath', './restart')
        # xmlHandler.setAttribute('aerosol', 'sparam', 'postProcPath', './stat')
        xmlHandler.write(self.rootPath + '/config.xml')

    def linkingToExe(self):
        for exeName in os.listdir(self.studyPath['EXE']):
            relativePath = os.path.relpath(self.studyPath['EXE'] + "/" + exeName, self.rootPath)
            os.symlink(relativePath, self.rootPath + '/' + exeName)

    def getExePath(self):
        for exeName in os.listdir(self.studyPath['EXE']):
            return self.rootPath + '/' + exeName

    def getConfigPath(self):
        return self.rootPath + '/config.xml'

    def getRootPath(self):
        return self.rootPath

    def setRootPath(self, path):
        self.rootPath = path
        for iName in PathCase.__directories:
            self.update({iName: self.rootPath + '/' + iName})
