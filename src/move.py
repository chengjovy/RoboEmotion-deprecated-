import sys
import json


class ServoMove(object):

	_LEGAL_TYPE = ("action", "loop", "posture")
	_LEGAL_POSITION_RANGE = (0, 180)
	_LEGAL_SPEED = ("high", "med", "low")
	_SPEED_TO_STEP = {
		'high': 180,
		'med': 18,
		'low': 6
	}

	def __init__(self, type=None, startPosition=None, endPosition=None, speed="med", totalTimes=float('INF')):
		# configuration variables
		self.type = type
		self.startPosition = startPosition
		self.endPosition = endPosition
		self.speed = speed
		self.totalTimes = totalTimes
		self.verify()
		# performing variables
		self.performedTimes = 0
		self.currentPosition = None
		self.stepVector = None
		self.goingForward = None

	def verify(self):
		# type
		if self.type not in ServoMove._LEGAL_TYPE:
			raise ValueError('move type should be one of the following: %s (%s given).' % (str(ServoMove._LEGAL_TYPE), self.type))
		# startPosition
		if not isinstance(self.startPosition, int):
			raise TypeError('startPosition should be an integer. (%s given)' % (str(self.startPosition)))
		if not (ServoMove._LEGAL_POSITION_RANGE[0] <= self.startPosition <= ServoMove._LEGAL_POSITION_RANGE[1]):
			raise ValueError('startPosition should be inside range: %s, and %d given' % (ServoMove._LEGAL_POSITION_RANGE, self.startPosition))
		# endPosition
		if self.type != "posture":
			if not isinstance(self.endPosition, int):
				raise TypeError('endPosition should be an integer. (%s given)' % (str(self.endPosition)))
			elif not (ServoMove._LEGAL_POSITION_RANGE[0] <= self.endPosition <= ServoMove._LEGAL_POSITION_RANGE[1]):
				raise ValueError('endPosition should be inside range: %s, and %d given' % (ServoMove._LEGAL_POSITION_RANGE, self.endPosition))
		# speed
		if self.speed not in ServoMove._LEGAL_SPEED:
			raise ValueError('move speed should be one of the following: %s (%s given).' % (str(ServoMove._LEGAL_SPEED), self.speed))

	def getNext(self):
		"""
			This function should be called 10 times / sec.
		"""
		if self.currentPosition is None:
			self.initCurrentPosition()
		else:
			self.updateCurrentPosition()
		return self.currentPosition
	
	def initCurrentPosition(self):
		self.currentPosition = self.startPosition
		if self.type == 'action' or self.type == 'loop':
			self.stepVector = ServoMove._SPEED_TO_STEP[self.speed] * (self.endPosition - self.startPosition) / abs(self.endPosition - self.startPosition)
			self.goingForward = True
		elif self.type == 'posture':
			self.stepVector = 0
		else:
			raise ValueError('cannot recognize this type: ' + self.type)

	def updateCurrentPosition(self):
		if self.type == 'action' or self.type == 'loop':
			if self.type == 'action' and self.performedTimes > 0:
				pass
			elif self.type == 'loop' and self.performedTimes > self.totalTimes:
				pass
			elif self.goingForward:
				if abs(self.stepVector) >= abs(self.endPosition - self.currentPosition):
					self.currentPosition = self.endPosition
					self.goingForward = False
					self.performedTimes += 1
				else:
					self.currentPosition += self.stepVector
			else:
				if abs(self.stepVector) >= abs(self.startPosition - self.currentPosition):
					self.currentPosition = self.startPosition
					self.goingForward = True
					self.performedTimes += 1
				else:
					self.currentPosition -= self.stepVector
		elif self.type == 'posture':
			pass
		else:
			raise ValueError('cannot recognize this type: ' + self.type)

	def isFinished(self):
		ret = (self.type == 'posture')
		ret |= (self.type == 'action' and self.performedTimes > 0)
		ret |= (self.type == 'loop' and self.performedTimes > self.totalTimes)
		return ret

	def reset(self):
		self.performedTimes = 0
		self.currentPosition = None
		self.stepVector = None
		self.goingForward = None

class Move(object):

	# finish criteria (pseudo enum)
	_FINISH_CRITERIA_ANY = 0
	_FINISH_CRITERIA_ALL = 1

	def __init__(self, fromServoMoves=None, fromFile=None, fromServoConfig=None):

		self.servoMoves = []

		if fromServoMoves is not None:
			if not all(isinstance(sm, ServoMove) for sm in fromServoMoves):
				raise ValueError('(Move) __init__(): bad argument (fromServoMoves)')
			self.servoMoves = fromServoMoves
		elif fromFile is not None:
			try:
				fileContent = json.load(open(fromFile, 'r'))
			except IOError as err:
				print('cannot open file: %s (%s)' % (fromFile, err))
				sys.exit(1)
			except ValueError as err:
				print('bad JSON file: %s (%s)' % (fromFile, err))
				sys.exit(1)
			except:
				print('error loading file (unknown)')
				sys.exit(1)
			if not type(fileContent) == type([]):
				raise ValueError('not an array (%s)' % (fromFile))
			self.servoMoves = [ServoMove(**d) for d in fileContent]
		elif fromServoConfig is not None:
			self.servoMoves = [ServoMove(**d) for d in fromServoConfig]
		else:
			raise ValueError('class Move must be instantiate using a file or an array of ServoMove')

	def getNext(self):
		"""
			This function should be called 10 times / sec.
		"""
		return [s.getNext() for s in self.servoMoves]

	def getNumServos(self):
		return len(self.servoMoves)

	def isFinished(self, criteria=_FINISH_CRITERIA_ANY):
		if criteria == Move._FINISH_CRITERIA_ANY:
			return any(s.isFinished() for s in self.servoMoves)
		elif criteria == Move._FINISH_CRITERIA_ALL:
			return all(s.isFinished() for s in self.servoMoves)
		else:
			raise ValueError('cannot recognize finish criteria: %s' % (str(criteria)))

	def reset(self):
		for sm in self.servoMoves:
			sm.reset()
