# -*- coding: utf-8 -*-

import os
from PathHandler import PathStudy
from ConfigTemplate import generateConfigFile
from XmlHandler import XmlHandler


def createStudy(studyName, exePath):

    studyPath = PathStudy(studyName)
    studyPath.createTree()

    generateConfigFile(studyPath['CONFIG'])
    xmlHandler = XmlHandler(studyPath['CONFIG'] + '/config.xml')
    xmlHandler.setAttribute('mesh', 'sparam', 'file', studyPath['MESH'])
    xmlHandler.write(studyPath['CONFIG'] + '/config.xml')

    try:
        os.symlink(exePath, studyPath['EXE'] + '/' + exePath.split("/")[-1])
    except OSError:
        print 'Error : Path to exe seems incorrect : ', exePath

    return studyPath
