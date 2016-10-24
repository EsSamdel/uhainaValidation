from CaseBump1d import *
from CaseCarrierGreenspanTrans import *


def main():
    # exePath = "/Home/delmas/Workspace/uhainaCurrentRevision/uhaina/Uhaina"
    exePath = "/Home/delmas/Workspace/uhainaWorkingRevision/uhaina/Uhaina"

    # casesList = {'Bump1d': Bump1d(exePath)}
    casesList = {'CarrierGreenspanTrans': CarrierGreenspanTrans(exePath)}

    for iName, iCase in casesList.iteritems():
        if iCase.hasExactSolution():
            iCase.runConvergenceTest()


if __name__ == "__main__":
    main()
