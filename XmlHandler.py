# -*- coding: utf-8 -*-
"""
Created on Thu May 21 10:50:40 2015

@author: simon
"""

import sys
from lxml import etree


class XmlHandler:
    root = None

    def __init__(self, path):
        try:
            self.tree = etree.parse(path)
        except NameError:
            print "Error : Unable to parse ", path
            sys.exit()

        self.root = self.tree.getroot()

    def getNodeByName(self, name):
        for child in self.root:
            if child.tag == name:
                return child

    def getAttributesByNode(self, name):
        node = self.getNodeByName(name)
        dico = dict()
        for child in node:
            dico[child.attrib['key']] = child.attrib['val']
        return dico

    def getAttribute(self, nodeName, key):
        node = self.getNodeByName(nodeName)
        for child in node:
            if child.attrib['key'] == key:
                return child.attrib['val']

    def setAttribute(self, nodeName, typeEl, key, val):
        node = self.getNodeByName(nodeName)
        isFind = False
        for child in node:
            if child.attrib['key'] == key:
                child.attrib['val'] = val
                isFind = True

        if not isFind:
            node.append(etree.Element(typeEl, {'key': key, 'val': val}))

    def write(self, path):
        with open(path, 'w') as iFile:
            iFile.write('<?xml version="1.0"?> \n')
            iFile.write('<!DOCTYPE aerosol_config SYSTEM "./aerosol_config.dtd"> \n')
            self.tree.write(iFile, pretty_print=True)
