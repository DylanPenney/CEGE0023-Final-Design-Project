from fluid import *
import math

DIAMETER = 4.5
TOWER_DIAMETER = 4.2
ROTOR_DIAMETER = 112
ROTOR_AREA = math.pi * (ROTOR_DIAMETER**2) / 4


"""
TODO:
Rotor Thrust (LC 1.1)
Mudline Overturnign Moment
"""

C_T = 0.8
C_D_WIND_1_1 = 0.6
C_D_WIND_6_1 = 0.7


class LoadCase:
    def __init__(self, wavefile, windfile, wave_period, C_D, C_M, C_D_WIND) -> None:
        self.wave = Wave(1025, wavefile)
        self.wind = Wind(1.225, windfile)
        self.C_D = C_D
        self.C_M = C_M

        # as KC is always 0
        self.C_D_wind = C_D_WIND
        self.C_M_wind = 0
        self.w = 2 * math.pi / wave_period

    def F_D_wave_current(self, z):
        """
        Returns the wave-current drag force at a given depth
        """
        return 0.5 * self.wave.density * self.C_D * DIAMETER * (self.wave.u_t[z] ** 2)

    def F_I_wave(self, z):
        """
        Returns the wave inertia force at a given depth
        """
        return (
            self.wave.density
            * math.pi
            * 0.25
            * self.C_M
            * (DIAMETER**2)
            * (self.wave.u_a[z] * self.w)
        )

    def wave_current_force(self, z):
        """
        Returns the total load exerted by the waves and the current at a given depth
        """
        return self.F_D_wave_current(z), self.F_I_wave(z)

    def F_D_wind(self, z):
        """
        Returns (what would be) the total drag force on the wind turbine at a given depth
        """
        return (
            0.5
            * self.wind.density
            * self.C_D_wind
            * TOWER_DIAMETER
            * (self.wind.U[z] ** 2)
        )

    def F_T_wind(self):
        """
        Caclulates the rotor thrust force at a given depth
        """
        return 0.5 * C_T * self.wind.density * ((8.5) ** 2) * ROTOR_AREA

    def F_I_wind(self, z):
        """
        Returns the total wind inertia force on the wind turbine at a given height
        """
        return (
            self.wind.density
            * math.pi
            * 0.25
            * self.C_M_wind
            * (TOWER_DIAMETER**2)
            * (self.wind.U[z] * self.w)
        )

    def wind_force(self, z):
        """
        Returns the total load exerted on the wind turbine by the wind at a given height
        """
        return self.F_D_wind(z), self.F_I_wind(z)

    def mudline_overturning_moment(self):
        """
        Returns the mudline overturning moment
        """
        seabed = min(self.wave.U.keys())
        z = seabed
        higher = max(self.wind.U.keys())
        total = 0
        while z <= higher:
            if z < 0:
                total += sum(self.wave_current_force(z)) * (z - seabed)
                z += 0.01
            elif z >= 0:
                total += sum(self.wind_force(z)) * (z - seabed)
                z += 0.1
            z = round(z, 2)
        return total


# T = 5.8
# C_M(wave-Current) = 2.0
# C_D(Wave-Current) = 0.0
one_one = LoadCase(
    "../data/timeseries1.1.csv", "../data/wind1.1.csv", 5.0, 0, 2.0, C_D_WIND_1_1
)
# T = 7.6
# C_M = 1.8
# C_D = 0.62
six_one = LoadCase(
    "../data/timeseries6.1.csv", "../data/wind6.1.csv", 7.6, 0.62, 1.8, C_D_WIND_6_1
)


def integrate(lower, higher, precision, function):
    """
    Returns a numerical approximation of the integral of a function
    """
    current = lower
    # = [Wave-Current Force (Drag), Wave-Current Force (Inertia), Wind Force (Drag), Wind Force (Inertia)]
    total = [0, 0, 0, 0]

    while current <= higher:
        # Wave-Current
        total[0] += function(current)[0] * precision
        total[1] += function(current)[1] * precision
        current += precision
        current = round(current, 2)

    return total


print("\n" * 100)

print(
    f"Load Case 1.1\n{'-'*13}\nWave-Current Force (Drag): {round(integrate(-22.09, 0, 0.01, one_one.wave_current_force)[0], 2)} \nWave-Current Force (Inertia): {round(integrate(-22.09, 0, 0.01, one_one.wave_current_force)[1], 2)} \nWind Force (Drag): {round(integrate(0, 109.3, 0.1, one_one.wind_force)[0], 2)} \nWind Force (Inertia): {round(integrate(0, 109.3, 0.1, one_one.wind_force)[1], 2)}"
)
print(f"Rotor Thrust: {round(one_one.F_T_wind(), 2)}")
print(f"Mudline Overturning Moment: {round(one_one.mudline_overturning_moment(), 2)}")


print("\n")

print(
    f"Load Case 6.1c\n{'-'*13}\nWave-Current Force (Drag): {round(integrate(-27.31, 0, 0.01, six_one.wave_current_force)[0], 2)} \nWave-Current Force (Inertia): {round(integrate(-27.31, 0, 0.01, six_one.wave_current_force)[1], 2)} \nWind Force (Drag): {round(integrate(0, 104, 0.1, six_one.wind_force)[0], 2)} \nWind Force (Inertia): {round(integrate(0, 104, 0.1, six_one.wind_force)[1], 2)}"
)
print(f"Mudline Overturning Moment: {round(six_one.mudline_overturning_moment(), 2)}")
