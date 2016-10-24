from CaseInterface import *


class Bump1d(CaseInterface):
    def __init__(self, exePath):
        CaseInterface.__init__(self, exePath)
        self.caseName = "Bump1d"
        self.testName = "Bump1d"
        self.dim = 1
        self.lx = 20
        self.ly = 0
        self.nx = 100
        self.ny = 0

        self.nMax = 10000.0
        self.tMax = 30.0

        self.studyPath = PathStudy(self.testName)
        self.studyPath.create(self.exePath)
        self.casePath = PathCase(self.studyPath)
        self.mesh = GmshMesh(1, lx=self.lx, ly=self.ly, nx=self.nx, ny=self.ny)

        self.orderList = [2, 3]

    def defineConfig(self, meshPath=None, degree=1, CFL=0.3):
        if meshPath is None:
            meshPath = self.mesh.getMeshPath()

        xmlHandler = XmlHandler(self.casePath.getConfigPath())

        xmlHandler.setAttribute('aerosol', 'sparam', 'castest', self.testName)
        xmlHandler.setAttribute('mesh', 'sparam', 'file', meshPath)

        xmlHandler.setAttribute('model', 'fparam', 'g', "9.8")
        xmlHandler.setAttribute('model', 'fparam', 'dryTolerance', "0.0001")

        xmlHandler.write(self.casePath.getConfigPath())

        self.setDegree(degree)
        self.setCFL(CFL)
        self.setTimePeriod(self.nMax, self.tMax)

    def hasExactSolution(self):
        return True


