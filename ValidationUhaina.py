from CaseBump1d import *
from CaseCarrierGreenspanTrans import *


def main():
    # exePath = "/Home/delmas/Workspace/uhainaCurrentRevision/uhaina/Uhaina"
    exePath = "/Home/delmas/Workspace/uhainaWorkingRevision/uhaina/Uhaina"

    # casesList = {'Bump1d': GmshMesh(1, lx=20, ly=0, nx=100, ny=0),
    #              'WellBalancing1d': GmshMesh(1, lx=2, ly=0, nx=100, ny=0),
    #              'WellBalancing2d': GmshMesh(2, lx=2, ly=1, nx=100, ny=50),
    #              'CarrierGreenspan': GmshMesh(1, lx=20, ly=0, nx=100, ny=0),
    #              'CarrierGreenspanPeriodic': GmshMesh(1, lx=20, ly=0, nx=100, ny=0)
    #              }

    # casesList = {'Bump1d': Bump1d(exePath)}
    casesList = {'CarrierGreenspanTrans': CarrierGreenspanTrans(exePath)}

    for caseName, case in casesList.iteritems():
        if case.hasExactSolution():
            case.runConvergenceTest()


if __name__ == "__main__":
    main()
