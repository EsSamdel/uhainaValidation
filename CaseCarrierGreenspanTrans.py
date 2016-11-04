from CaseInterface import *

import os
import vtk
from vtk.util import numpy_support as vn

import numpy as np
from math import sqrt
from scipy.optimize import fsolve

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')


class CarrierGreenspanTrans(CaseInterface):
    def __init__(self, exePath):
        CaseInterface.__init__(self, exePath)
        self.caseName = "CarrierGreenspanTrans"
        self.testName = "CarrierGreenspanTrans"
        self.dim = 1
        self.lx = 20
        self.ly = 0
        self.nx = 100
        self.ny = 0

        self.g = 9.8
        self.dryTolerance = 0.0001
        self.L = self.lx
        self.alpha = 1.0
        self.e = 0.2
        self.initTime = 0.0
        self.nMax = 10000
        self.tMax = 1.5

        self.studyPath = PathStudy(self.testName)
        self.studyPath.create(self.exePath)
        self.casePath = PathCase(self.studyPath)
        self.mesh = GmshMesh(1, lx=self.lx, ly=self.ly, nx=self.nx, ny=self.ny)

        self.orderList = [2, 3]

    def defineConfig(self, meshPath=None, degree=1, CFL=0.3):
        if meshPath is None:
            meshPath = self.mesh.getMeshPath()

        xmlHandler = XmlHandler(self.casePath.getConfigPath())

        xmlHandler.setAttribute('mesh', 'sparam', 'file', meshPath)

        xmlHandler.setAttribute('aerosol', 'sparam', 'castest', self.testName)
        xmlHandler.setAttribute('aerosol', 'sparam', 'visualisationVariables', "h")

        xmlHandler.setAttribute('model', 'fparam', 'g', str(self.g))
        xmlHandler.setAttribute('model', 'fparam', 'dryTolerance', str(self.dryTolerance))
        xmlHandler.setAttribute('model', 'fparam', 'velocityCutOff', "0.001")

        xmlHandler.setAttribute('model', 'iparam', 'artificialViscosity', "1")
        xmlHandler.setAttribute('model', 'fparam', 'thViscosityScaling', "0.2")

        xmlHandler.setAttribute('model', 'fparam', 'L', str(self.lx))
        xmlHandler.setAttribute('model', 'fparam', 'alpha', str(self.alpha))
        xmlHandler.setAttribute('model', 'fparam', 'e', str(self.e))
        xmlHandler.setAttribute('model', 'fparam', 'initTime', str(self.initTime))

        xmlHandler.setAttribute('time', 'iparam', 'kprint', "100")

        # xmlHandler.setAttribute('discretisation', 'sparam', 'numericalflux', "WellBalancedLaxFriedrich")
        # xmlHandler.setAttribute('model', 'fparam', 'epsilon', str(self.dryTolerance))

        xmlHandler.write(self.casePath.getConfigPath())

        self.setDegree(degree)
        self.setCFL(CFL)
        self.setTimePeriod(self.nMax, self.tMax)

    def hasExactSolution(self):
        return True

    def getShorelineFromVTK(self):
        dataPath = self.casePath['visu']
        filesList = os.listdir(dataPath)
        filesList = [iFile for iFile in filesList if "output0" in iFile]
        filesList.sort(key=lambda name: int(name.split("output")[-1].split(".")[0]))

        shoreline = np.zeros(len(filesList))
        for fileNumber, iFile in enumerate(filesList):
            reader = vtk.vtkXMLUnstructuredGridReader()
            reader.SetFileName(dataPath + "/" + iFile)
            reader.Update()
            dataSet = reader.GetOutput()
            h = vn.vtk_to_numpy(dataSet.GetPointData().GetArray('h'))[2:]

            for i, val in enumerate(h):
                if val <= self.dryTolerance:
                    shoreline[fileNumber] = dataSet.GetPoint(i + 2)[0]
                    break

        time = np.linspace(0., self.tMax, num=len(filesList))
        return time, shoreline

    def exactShoreline(self, dt=0.05):
        a = 1.5 * sqrt(1.0 + 0.9 * self.e)
        x0 = 0.7

        tt = []
        ut = []
        xt = []

        nMax = int(self.tMax / dt)
        tDim = -dt
        for i in range(nMax):
            tDim += dt
            t = tDim * sqrt(self.alpha * self.g / self.lx)

            # ------
            def ftemp3(u3tmp):
                u3tmp = u3tmp[0]
                numer = 5.0 * (2.0 / a * (u3tmp + t)) ** 3.0 - (2.0 / a * (u3tmp + t)) ** 5.0
                denom = (1.0 + 4.0 / a ** 2.0 * (u3tmp + t) ** 2.0) ** 4.0
                return u3tmp - 8.0 * self.e / a * numer / denom

            u3 = fsolve(ftemp3, 0.)[0]
            lam3 = 2.0 / a * (u3 + t)
            x3 = -0.5 * u3 ** 2.0 + self.e - self.e * (1.0 + 3 * lam3 ** 2.0 - 2.0 * lam3 ** 4.0) / \
                                                      (1.0 + lam3 ** 2.0) ** 3.0

            tt.append(tDim)
            ut.append(u3 * sqrt(self.g * self.alpha * self.lx))
            xt.append((x3 + x0) * self.lx)

        return tt, xt, ut

    def plotShoreline(self):
        savePath = self.casePath.getRootPath() + "/shoreline"
        t = 0
        x = 1
        exactSol = self.exactShoreline()
        numSol = self.getShorelineFromVTK()

        pos = 10
        plt.clf()
        plt.plot(numSol[t][pos:], numSol[x][pos:], label='Numerical')
        plt.plot(exactSol[t], exactSol[x], label='Exact')
        plt.xlabel('t')
        plt.ylabel('x')
        plt.legend(loc='lower right', shadow=True)

        plt.savefig(savePath + '.png')
        # plt.show()

    def specificCasePostProcess(self):
        self.plotShoreline()


if __name__ == '__main__':
    testCase = CarrierGreenspanTrans('')
    caseName = testCase.testName + '_order' + str(3) + '_h' + str(320)
    testCase.casePath.setRootPath(testCase.studyPath.getRootPath() + '/' + caseName)
    testCase.plotShoreline()


