class SimplePacket:
	def __init__(self):
		self.source = 0
		self.destination = 0
		self.type = 0
		self.data = bytearray()

	def getSource(self):
		return self.source

	def setSource(self, source):
		self.source = int(source)

	def getDestination(self):
		return self.destination

	def setDestination(self, destination):
		self.destination = int(destination)

	def getType(self):
		return self.type

	def setType(self, type):
		self.type = int(type)

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = bytearray(data);

	def setChar(self, value, signed = True):
		self.data = value.to_bytes(1, byteorder = "little", signed = signed)

	def setShort(self, value, signed = True):
		self.data = value.to_bytes(2, byteorder = "little", signed = signed)

	def setInt(self, value, signed = True):
		self.data = value.to_bytes(4, byteorder = "little", signed = signed)

	def setLong(self, value, signed = True):
		self.data = value.to_bytes(8, byteorder = "little", signed = signed)

	def setString(self, value):
		self.data = bytearray(value, "utf-8")
		self.data.append(0x00)

	def getChar(self, signed = True):
		return int.from_bytes(self.data[:1], byteorder = "little", signed = signed)

	def getShort(self, signed = True):
		return int.from_bytes(self.data[:2], byteorder = "little", signed = signed)

	def getInt(self, signed = True):
		return int.from_bytes(self.data[:4], byteorder = "little", signed = signed)

	def getLong(self, signed = True):
		return int.from_bytes(self.data[:8], byteorder = "little", signed = signed)

	def getString(self):
		return self.data[0:-1].decode(encoding = "utf-8", errors = "ignore")

class SimpleComm:
	SYN = 0x02
	address = 0

	def __init__(self, address = 0):
		SimpleComm.setAddress(address)

	def setAddress(address):
		SimpleComm.address = address

	def getAddress():
		return SimpleComm.address

	def send(stream, packet, destination = None, type = None):
		packet.setSource(SimpleComm.getAddress())

		if destination != None:
			packet.setDestination(destination)

		if type != None:
			packet.setType(type)

		data = packet.getData()
		buffer = bytearray()
		buffer.append(SimpleComm.SYN)
		buffer.append(len(data) + 4)
		buffer.append(packet.getDestination())
		buffer.append(packet.getSource())
		buffer.append(packet.getType())
		buffer += data
		buffer.append(SimpleComm.calcCRC(buffer[2:]))

		stream.write(bytes(buffer))

	def receive(stream):
		try:
			while True:
				r = stream.read(1)
				if len(r) == 0:
					break

				if r[0] != SimpleComm.SYN:
					continue

				r = stream.read(1)
				if len(r) == 0:
					break

				tlen = r[0]
				if tlen < 4:
					continue

				buffer = stream.read(tlen)
				if len(buffer) != tlen:
					break;

				crc = SimpleComm.calcCRC(buffer[0:-1])
				if crc != buffer[-1]:
					continue

				packet = SimplePacket()
				packet.setDestination(buffer[0])
				packet.setSource(buffer[1])
				packet.setType(buffer[2])
				packet.setData(buffer[3:-1])

				return packet

		except:
			return None

		return None

	def calcCRC(buffer):
		return sum(buffer) & 0xff
