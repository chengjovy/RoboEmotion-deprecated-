import serial

class SerialCorrespondent(object):

	def __init__(self, serialIdentifier=None, baudRate=None):
		self.serialIdentifier = serialIdentifier
		self.baudRate = baudRate
		self.device = None

	def connect(self):
		try:
			self.device = serial.Serial(self.serialIdentifier, self.baudRate)
		except Exception as e:
			print('cannot initiate serial connection: ' + str(e))

	def isConnected(self):
		return isinstance(self.device, serial.serialposix.Serial)

	def write(self, msg='', end=''):
		if not self.isConnected():
			raise Exception('not connected')
		self.device.write(msg + end)
