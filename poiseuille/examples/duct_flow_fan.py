from poiseuille.components.blocks import PressureReservoir, Fan, ConstantDeliveryFan
from poiseuille.components.connectors import PoiseuilleConnector
from poiseuille.systems.system import IncompressibleSystem

def run():
    p1 = PressureReservoir(p=0.)
    p2 = PressureReservoir(p=0.)
    fan = ConstantDeliveryFan(flow_rate=5.)
    c1 = PoiseuilleConnector(r=1.34)
    c2 = PoiseuilleConnector(r=1.12)
    c1.connect(p1.node, fan.input)
    c2.connect(fan.output, p2.node)

    system = IncompressibleSystem([p1, p2, fan])

    system.solve()

    for connector in system.connectors():
        print connector.flow_rate

    for node in system.nodes():
        print node.p, type(node)

if __name__ == '__main__':
    run()