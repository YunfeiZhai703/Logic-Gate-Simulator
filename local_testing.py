from scanner import Scanner, Symbol
from names import Names
from parse import Parser
from devices import Devices
from network import Network
from monitors import Monitors


name = Names()
scan = Scanner("./tests/parser/test_device_error.txt", name)
devices = Devices(name)
networks = Network(name, devices)
monitors = Monitors(name, devices, networks)
parser = Parser(name, devices, networks, monitors, scan)
parser.parse_network()

print(parser.errors)

devices = parser.devices.devices_list

for device in devices:
    print(device)


devs = parser.monitors.monitors_dictionary

print(devs)
