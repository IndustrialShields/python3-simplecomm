#!/usr/bin/env python3

from SimpleComm import SimpleComm, SimplePacket

if __name__ == "__main__":
	SimpleComm.setAddress(0x10)

	packet = SimplePacket()
	packet.setDestination(0x11)
	packet.setType(0x03)
	packet.setString("Hello")

	with open("test.bin", "wb") as f:
		SimpleComm.send(f, packet)
