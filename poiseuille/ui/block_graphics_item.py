from PyQt5 import QtWidgets, QtCore, QtGui

from poiseuille.components.blocks import *

from .block_dialog import BlockDialog
from .connector_graphics_path_item import ConnectorGraphicsPathItem

class NodeGraphicsItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, node, block, x=0, y=0):
        super(NodeGraphicsItem, self).__init__(x, y, 10, 10, parent=block)
        self.node = node
        self.block = block
        self.connector = None

    def mousePressEvent(self, QGraphicsSceneMouseEvent):
        if not self.node.connector:
            self.connector = ConnectorGraphicsPathItem(self)
            self.scene().addItem(self.connector)

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        if self.connector:
            self.connector.setPathTo(QGraphicsSceneMouseEvent.scenePos())

    def mouseReleaseEvent(self, QGraphicsSceneMouseEvent):
        if self.connector:
            self.scene().removeItem(self.connector)
            item = self.scene().itemAt(QGraphicsSceneMouseEvent.scenePos(), QtGui.QTransform())

            if isinstance(item, NodeGraphicsItem):
                if self.connector.connect(item):
                    self.connector.update_path()
                    self.scene().addItem(self.connector)
                else:
                    self.connector = None
            else:
                self.connector = None

class BlockGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, block=None, file='resources/default'):
        super(BlockGraphicsItem, self).__init__(QtGui.QPixmap(file), None)
        self.block = block
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.nodes = []
        self.init_nodes()

    def init_nodes(self):
        raise NotImplementedError('Block graphics items must implement node placement.')

    def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
        dialog = BlockDialog(self.block)
        dialog.exec_()

    def mouseMoveEvent(self, QGraphicsSceneMouseEvent):
        super(BlockGraphicsItem, self).mouseMoveEvent(QGraphicsSceneMouseEvent)

        for node in self.nodes:
            if node.connector:
                node.connector.update_path()

class PressureReservoirGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=PressureReservoir()):
        super(PressureReservoirGraphicsItem, self).__init__(block=block, file='resources/pressure_reservoir')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.node, self, x=-10, y=17.5))

class FanGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=Fan()):
        super(FanGraphicsItem, self).__init__(block=block, file='resources/fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-10, y=17.5))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))


class ConstFlowFanGraphicsItem(BlockGraphicsItem):
    def __init__(self, block=ConstantDeliveryFan()):
        super(ConstFlowFanGraphicsItem, self).__init__(block=block, file='resources/const_flow_fan')

    def init_nodes(self):
        self.nodes.append(NodeGraphicsItem(self.block.input, self, x=-5, y=10))
        self.nodes.append(NodeGraphicsItem(self.block.output, self, x=47.5, y=17.5))

def construct_block(type):
    if type == 'Pressure Reservoir':
        return PressureReservoirGraphicsItem()
    elif type == 'Fan':
        return FanGraphicsItem()
    elif type == 'Constant Delivery Fan':
        return ConstFlowFanGraphicsItem()
    else:
        raise ValueError('Unrecognized block type "{}".'.format(type))