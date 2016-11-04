# -*- coding: utf-8 -*-

import sys
from subprocess import check_output


class RunCase:
    def __init__(self, casePath, nbProc=1, restart=False):
        self.casePath = casePath
        self.nbProc = nbProc
        self.restart = restart
        self.exePath = casePath.getExePath()
        self.output = ""
        self.formatedOutput = ""
        self.terminated = False

    def run(self):
        if self.restart:
            print "Error : Restart not implement yet!"
            sys.exit()
        else:
            commands = ['cd ' + self.casePath.rootPath + '; ' +
                        'mpirun -np ' + str(self.nbProc) + ' ' + self.exePath + ' -i ' + self.casePath.getConfigPath()]

        # print commands[0]
        self.output = check_output(commands[0], shell=True)
        self.formatedOutput = self.output.splitlines()

        self.terminated = True

    def getOutput(self):
        if self.output == "":
            print "Error : (RunCase.getOutput) No output yet! Run not launch yet or failed."
            sys.exit()
        else:
            return self.output

    def getErrorL2(self):
        if self.terminated and self.output is not "":
            for line in self.formatedOutput[-10:-1]:
                if 'Erreur L2 = ' in line:
                    tab = line.split('=')[-1]
                    tab = tab.split()
                    result = []
                    for iVal in tab:
                        result.append(float(iVal))
                    return result
        else:
            print "Error : (RunCase.getErrorL2) No output yet! Run not launch yet or failed."
            sys.exit()

    def getErrorL1(self):
        if self.terminated and self.output is not "":
            for line in self.formatedOutput[-10:-1]:
                result = []
                if 'Erreur L2 = ' in line:
                    tab = line.split('=')[-1]
                    tab = tab.split()
                    result.append(float(tab[0]))
                if 'Erreur L1 = ' in line:
                    tab = line.split('=')[-1]
                    tab = tab.split()
                    for iVal in tab:
                        result.append(float(iVal))
                    return result
        else:
            print "Error : (RunCase.getErrorL2) No output yet! Run not launch yet or failed."
            sys.exit()

    def checkRun(self):
        if self.terminated:
            for line in self.formatedOutput:
                if "Error" in line:
                    print "Find error in run log :"
                    print line

    def printLogToFile(self):
        with open(self.casePath.getRootPath() + "/logFile.txt", 'w') as iFile:
            iFile.write(self.output)
            # for line in self.formatedOutput[-10:-1]:
            #     iFile.write(line + '\n')
