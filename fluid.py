class Fluid:
    def __init__(self, name, density, filename):
        self.name = name
        self.density = density
        self.filename = filename
        self.U = {}

    def __str__(self) -> str:
        return self.name


class Wind(Fluid):
    def __init__(self, density, file):
        super().__init__("Wind", density, file)
        self.index()

    def index(self):
        with open(self.filename) as f:
            data = f.readlines()
            for line in data[1:]:
                line = line.strip("\n").split(",")
                self.U[float(line[0])] = float(line[1])
            f.close()


class Wave(Fluid):
    def __init__(self, density, file):
        super().__init__("Wave", density, file)
        self.u_a = {}
        self.u_t = {}
        self.index()

    def index(self):
        with open(self.filename) as f:
            data = f.readlines()
            for line in data[1:]:
                line = line.strip("\n").split(",")
                self.U[float(line[0])] = float(line[1])
                self.u_a[float(line[0])] = float(line[2])
                self.u_t[float(line[0])] = float(line[3])
            f.close()
