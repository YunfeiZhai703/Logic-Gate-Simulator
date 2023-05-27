from scanner import Scanner, Symbol
from names import Names
from parse import Parser
from devices import Devices
from network import Network
from monitors import Monitors


name = Names()
scan = Scanner("./tests/test2.txt", name)
devices = Devices(name)
networks = Network(name, devices)
monitors = Monitors(name, devices, networks)
parser = Parser(name, devices, networks, monitors, scan)
parser.parse_devices_block()
print(parser.errors)

devs = parser.devices.devices_list


for dev in devs:
    print(dev)
