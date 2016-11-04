from MeshGenerator import *
from RunCase import *
from PathHandler import *
import datetime
from XmlHandler import *
from math import log
import vtk
import numpy as np
from vtk.util import numpy_support as vn
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


def getSlopeFromError(error):
    dh = log(error[-1][0]) - log(error[0][0])
    du1 = log(error[-1][1]) - log(error[0][1])
    assert dh != 0
    slope = du1 / dh
    return slope


class CaseInterface:
    _cflDict = {1: 0.9, 2: 0.2, 3: 0.1}

    def __init__(self, exePath):
        self.exePath = exePath
        self.caseName = "caseInterface"
        self.testName = "testInterface"

        # Space attribute :
        self.dim = 1
        self.lx = 20
        self.ly = 0
        self.nx = 100
        self.ny = 0

        # Time attribute :
        self.nMax = 0
        self.tMax = 0.

        # Path and mesh
        self.studyPath = PathStudy()
        self.casePath = PathCase(self.studyPath)
        self.mesh = GmshMesh(self.dim, lx=self.lx, ly=self.ly, nx=self.nx, ny=self.ny)

        # Other
        self.orderList = []
        self.output = ""

    def createCase(self, name=None):
        self.studyPath.checkingTree()

        if name is None:
            now = datetime.datetime.now()
            self.caseName = now.strftime("%d-%m-%Y_%H:%M")
        else:
            self.caseName = name

        self.casePath = PathCase(self.studyPath, name)
        self.casePath.createTree()

    def createDefaultCase(self):
        self.generateMesh()
        self.createCase()
        self.defineConfig()

    def runCase(self, pathToCase=None):
        if pathToCase is None:
            pathToCase = self.casePath
        run = RunCase(pathToCase)
        print "Running case ", self.caseName, "..."
        run.run()
        run.checkRun()
        run.printLogToFile()
        return run

    def printTailLog(self, nLines=10):
        for iLine in range(nLines, 0, -1):
            print self.output[-iLine]

    def generateMesh(self):
        self.mesh.generateMesh(self.studyPath['MESH'], self.caseName)

    def setDegree(self, degree):
        xmlHandler = XmlHandler(self.casePath.getConfigPath())
        xmlHandler.setAttribute('discretisation', 'iparam', 'degree', str(degree))
        xmlHandler.setAttribute('time', 'iparam', 'order', str(degree + 1))
        xmlHandler.write(self.casePath.getConfigPath())

    def setCFL(self, cfl):
        xmlHandler = XmlHandler(self.casePath.getConfigPath())
        xmlHandler.setAttribute('time', 'fparam', 'CFL', str(cfl))
        xmlHandler.write(self.casePath.getConfigPath())

    def setTimePeriod(self, nMax, tMax):
        xmlHandler = XmlHandler(self.casePath.getConfigPath())
        xmlHandler.setAttribute('time', 'iparam', 'Nmax', str(nMax))
        xmlHandler.setAttribute('time', 'fparam', 'tmax', str(tMax))
        xmlHandler.write(self.casePath.getConfigPath())

    def defineConfig(self, meshPath=None, degree=1, CFL=0.3):
        raise NotImplementedError("Error : defineConfig not implemented in CaseInterface")

    def hasExactSolution(self):
        return False

    def specificCasePostProcess(self):
        pass

    def plotFinalSolution(self):
        if self.dim != 1:
            print "Warning :: plotFinalSolution only available with one dimensional problems"
        else:
            savePath = self.casePath.getRootPath() + "/finalSolution"
            x, eta, z = self.getFinalSolutionFromVtk()

            plt.clf()
            plt.plot(x, z, label='Bathymetry', color='k')
            plt.plot(x, eta, label='Water level', color='b')
            plt.fill_between(x, eta, z, color='b')
            plt.fill_between(x, z, 0, color='k')
            plt.xlabel('x')
            plt.ylabel('h')
            plt.legend(loc='lower right', shadow=True)

            plt.savefig(savePath + '.png')

    def getFinalSolutionFromVtk(self):
        dataPath = self.casePath['visu']

        fileName = "outputfinal.vtu"
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(dataPath + "/" + fileName)
        reader.Update()
        dataSet = reader.GetOutput()
        eta = vn.vtk_to_numpy(dataSet.GetPointData().GetArray('eta'))
        nPoints = dataSet.GetNumberOfPoints()

        x = np.arange(nPoints)
        x *= self.lx / x[-1]

        fileName = "bathymetry.vtu"
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(dataPath + "/" + fileName)
        reader.Update()
        dataSet = reader.GetOutput()
        z = vn.vtk_to_numpy(dataSet.GetPointData().GetArray('z'))

        return x, eta, z

    def runConvergenceTest(self):
        if self.hasExactSolution():
            # Generate meshes :
            meshList = []
            nx = 10
            for iSize in range(5):
                nx *= 2
                meshList.append(GmshMesh(self.dim, lx=self.lx, ly=self.ly, nx=nx, ny=nx))
                meshList[-1].generateMesh(self.studyPath['MESH'], self.caseName)

            # For each order and each mesh prepare case :
            for iOrder in self.orderList:
                errorL1 = []
                errorL2 = []
                for iMesh in meshList:
                    caseName = self.testName + '_order' + str(iOrder) + '_h' + str(iMesh.nx)
                    self.createCase(name=caseName)
                    self.defineConfig(meshPath=iMesh.getMeshPath(), degree=(iOrder - 1), CFL=CaseInterface._cflDict[iOrder])
                    run = self.runCase()
                    errorL1.append(run.getErrorL1())
                    errorL2.append(run.getErrorL2())
                    self.specificCasePostProcess()
                    self.plotFinalSolution()

                slope = getSlopeFromError(errorL2)
                print "Slope L2 = ", slope
                fileName = "Order_" + str(iOrder) + "_convergenceL2.txt"
                with open(self.studyPath.getRootPath() + "/" + fileName, 'w') as iFile:
                    iFile.write("# Slope : " + str(slope) + "\n")
                    for iErrorL2 in errorL2:
                        for iVal in iErrorL2:
                            iFile.write(str(iVal) + '\t')
                        iFile.write('\n ')

                slope = getSlopeFromError(errorL1)
                print "Slope L1 = ", slope
                fileName = "Order_" + str(iOrder) + "_convergenceL1.txt"
                with open(self.studyPath.getRootPath() + "/" + fileName, 'w') as iFile:
                    iFile.write("# Slope : " + str(slope) + "\n")
                    for iErrorL1 in errorL1:
                        for iVal in iErrorL1:
                            iFile.write(str(iVal) + '\t')
                        iFile.write('\n ')
