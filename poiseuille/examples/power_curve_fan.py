from poiseuille.components.blocks import PressureReservoir, PowerCurveFan
from poiseuille.components.connector import Connector
from poiseuille.components.resistance_functions import Resistance
from poiseuille.systems.system import IncompressibleSystem

import math

def power_curve(x):
    return -0.102351 * x**2 + 0.0235120 * x + 10

def run():
    p1 = PressureReservoir(p=3.)
    p2 = PressureReservoir(p=2)
    fan = PowerCurveFan(fcn=power_curve)
    c1 = Connector(r_func=Resistance(r=1.))
    c2 = Connector(r_func=Resistance(r=1.))
    c1.connect(p1.node, fan.input)
    c2.connect(fan.output, p2.node)

    fan.update_properties()

    system = IncompressibleSystem([p1, p2, fan])
    system.solve()

    for c in system.connectors():
        print(c.flow_rate)

    print(fan.dp, fan.flow_rate)

run()