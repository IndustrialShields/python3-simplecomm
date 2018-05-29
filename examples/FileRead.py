#!/usr/bin/env python3

from SimpleComm import SimpleComm, SimplePacket

if __name__ == "__main__":
	SimpleComm.setAddress(0x11)

	with open("test.bin", "rb") as f:
		packet = SimpleComm.receive(f)

		if packet != None:
			print("packet:")
			print("\tsource: {0}".format(packet.getSource()))
			print("\ttype: {0}".format(packet.getType()))
			print("\tvalue: {0}".format(packet.getString()))
