import os
import subprocess as sp


class GmshMesh:
    def __init__(self, dim, lx=1.0, ly=1.0, nx=1, ny=1):
        assert (dim < 3), "Error : Mesh generation only work for dim < 3!"

        self.dim = dim
        self.lx = lx
        self.ly = ly
        self.nx = nx
        self.ny = ny
        self.dx = lx / nx
        self.dy = 0
        if ny != 0:
            self.dy = ly / ny
        self.mshName = ""
        self.mshPath = ""

    def generateMesh(self, outputPath, outputName):
        if self.dim == 1:
            self.generate1dMesh(outputPath, outputName)
        elif self.dim == 2:
            self.generate2dMesh(outputPath, outputName)

    def generate1dMesh(self, outputPath, outputName):
        geoPath = "./tmpMesh.geo"
        self.mshName = outputName + "_" + str(self.lx) + "_" + str(self.nx) + ".msh"
        self.mshPath = outputPath + "/" + self.mshName

        with open(geoPath, 'w') as iFile:
            iFile.write("lx = " + str(self.lx) + ";\n")
            iFile.write("nx = " + str(self.nx) + ";\n")
            iFile.write("__lst=newp;\n")
            iFile.write("Point(__lst) = {0, 0, 0, 1.0};\n")
            iFile.write(
                "lineX[] = Extrude{" + str(self.lx) + ", 0, 0} { Point{__lst}; Layers{" + str(self.nx) + "}; };\n")

        print "Generate 1D Mesh with lenght = ", self.lx, " and ", self.nx, " cells."
        command = "gmsh -1 " + geoPath + " -o " + self.mshPath
        sp.check_output(command, shell=True)

        os.remove(geoPath)

    def generate2dMesh(self, outputPath, outputName):
        geoPath = "./tmpMesh.geo"
        self.mshName = outputName + "_" + str(self.lx) + "." + str(self.ly) + "_" + str(self.nx) + "." + str(
            self.ny) + ".msh"
        self.mshPath = outputPath + "/" + self.mshName

        with open(geoPath, 'w') as iFile:
            iFile.write("lx = " + str(self.lx) + ";\n")
            iFile.write("nx = " + str(self.nx) + ";\n")
            iFile.write("ly = " + str(self.ly) + ";\n")
            iFile.write("ny = " + str(self.ny) + ";\n")
            iFile.write("__lst=newp;\n")
            iFile.write("Point(__lst) = {0, 0, 0, 1.0};\n")
            iFile.write(
                "line[] = Extrude{" + str(self.lx) + ", 0, 0} { Point{__lst}; Layers{" + str(self.nx) + "}; };\n")
            iFile.write("surface[] = Extrude{0, " + str(self.ly) + ", 0} { Line{line[1]}; Layers{" + str(
                self.ny) + "}; Recombine;};\n")
            iFile.write("Physical Line(100) = {line[1]};\n")
            iFile.write("Physical Line(200) = {surface[0]};\n")
            iFile.write("Physical Line(300) = {surface[2]};\n")
            iFile.write("Physical Line(400) = {surface[3]};\n")
            iFile.write("Physical Surface(\"My Surface\") = {surface[1]};\n")

        print "Generate 2D Mesh with lenght = ", self.lx, " * ", self.ly, " and ", self.nx, " * ", self.ny, " cells."
        command = "gmsh -2 " + geoPath + " -o " + self.mshPath
        sp.check_output(command, shell=True)

        os.remove(geoPath)

    def getMeshPath(self):
        return self.mshPath

    def getMeshName(self):
        return self.mshName


if __name__ == "__main__":
    mesh = GmshMesh(1)
    mesh.generate1dMesh('./', 'toto')
