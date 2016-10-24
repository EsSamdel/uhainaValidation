# -*- coding: utf-8 -*-

from lxml import etree


def generateConfigFile(path):
    root = etree.Element("config")
    mesh = etree.SubElement(root, "mesh")
    aerosol = etree.SubElement(root, "aerosol")
    model = etree.SubElement(root, "model")
    # eos = etree.SubElement(root, "eos")
    discretisation = etree.SubElement(root, "discretisation")
    time = etree.SubElement(root, "time")

    mesh.append(etree.Element('iparam', {'key': 'dimension', 'val': '1'}))
    mesh.append(etree.Element('sparam', {'key': 'file', 'val': './'}))
    mesh.append(etree.Element('sparam', {'key': 'format', 'val': 'ParaGMSH'}))

    aerosol.append(etree.Element('iparam', {'key': 'debug', 'val': '0'}))
    aerosol.append(etree.Element('iparam', {'key': 'perf', 'val': '0'}))
    aerosol.append(etree.Element('iparam', {'key': 'matvect', 'val': '1'}))
    aerosol.append(etree.Element('iparam', {'key': 'prepartitioning', 'val': '1'}))
    aerosol.append(etree.Element('iparam', {'key': 'redistribution', 'val': '1'}))

    aerosol.append(etree.Element('sparam', {'key': 'visutype', 'val': 'cells'}))
    aerosol.append(etree.Element('sparam', {'key': 'output_format', 'val': 'XML'}))
    aerosol.append(etree.Element('sparam', {'key': 'visualisationVariables', 'val': ''}))

    aerosol.append(etree.Element('sparam', {'key': 'castest', 'val': 'testCase'}))
    aerosol.append(etree.Element('sparam', {'key': 'linearsolver', 'val': 'BLOCKDIAGONALSOLVER'}))
    aerosol.append(etree.Element('sparam', {'key': 'output_path', 'val': 'visu'}))
    aerosol.append(etree.Element('sparam', {'key': 'restartPath', 'val': 'restart'}))
    aerosol.append(etree.Element('sparam', {'key': 'restartPrefix', 'val': 'restart'}))

    model.append(etree.Element('sparam', {'key': 'name', 'val': 'ShallowWater'}))

    discretisation.append(etree.Element('iparam', {'key': 'continuous', 'val': '0'}))
    discretisation.append(etree.Element('iparam', {'key': 'degree', 'val': '0'}))
    discretisation.append(etree.Element('sparam', {'key': 'femtype', 'val': 'Lagrange'}))
    discretisation.append(etree.Element('sparam', {'key': 'numericalflux', 'val': 'WbswLaxFriedrich'}))

    time.append(etree.Element('sparam', {'key': 'inittype', 'val': 'interpolation'}))
    time.append(etree.Element('sparam', {'key': 'schemename', 'val': 'SSP'}))
    time.append(etree.Element('iparam', {'key': 'order', 'val': '1'}))
    time.append(etree.Element('sparam', {'key': 'stepping', 'val': 'CFL'}))
    time.append(etree.Element('fparam', {'key': 'CFL', 'val': '0.5'}))
    time.append(etree.Element('fparam', {'key': 'dtmax', 'val': '1.0'}))
    time.append(etree.Element('fparam', {'key': 'tmax', 'val': '0.0'}))
    time.append(etree.Element('iparam', {'key': 'Nmax', 'val': '1'}))
    time.append(etree.Element('iparam', {'key': 'kprint', 'val': '1'}))

    tree = etree.ElementTree(root)

    with open(path + '/config.xml', 'w') as iFile:
        iFile.write('<?xml version="1.0"?> \n')
        iFile.write('<!DOCTYPE aerosol_config SYSTEM "./aerosol_config.dtd"> \n')
        tree.write(iFile, pretty_print=True)
