from __future__ import print_function

import sys, json
from util import SerialCorrespondent
from move import Move


class RoboEmotion(object):

	_DEFAULT_EMOTION_MOVES = {
		"happy":    None,
		"sad":      None,
		"fear":     None,
		"anger":    None,
		"surprise": None,
		"disgust":  None
	}
	_DEFAULT_EMOTION_CONFIG = "robo_emotion_config.json"

	def __init__(self, defaultEmotionConfig=None, serialIdentifier="", baudRate=9600):
		#
		# initialize _DEFAULT_EMOTION_MOVES
		#
		if defaultEmotionConfig is not None:
			RoboEmotion._DEFAULT_EMOTION_CONFIG = defaultEmotionConfig
		fileContent = json.load(open(RoboEmotion._DEFAULT_EMOTION_CONFIG, 'r'))
		try:
			assert type(fileContent) == type({})
		except:
			raise ValueError("should be a dictionary mapping emotion name to its move (%s)" % (RoboEmotion._DEFAULT_EMOTION_CONFIG))
		for emotionName in fileContent:
			RoboEmotion._DEFAULT_EMOTION_MOVES[emotionName.lower()] = Move(fromServoConfig=fileContent[emotionName])
		#
		# initialize SerialCorrespondent
		#
		self.serialCorrespondent = SerialCorrespondent(serialIdentifier=serialIdentifier, baudRate=9600)
		self.serialCorrespondent.connect()

	def perform(self, move, finishCriteria=Move._FINISH_CRITERIA_ALL):
		print('performing move with criteria = %d' % (finishCriteria))
		print('this move config has %d servos.' % (move.getNumServos()))
		
		positions = move.getNext()
		print('positions: %s' % (str(positions)))
		self.serialCorrespondent.write(" ".join(str(pos) for pos in positions))
		while not move.isFinished(criteria=finishCriteria):
			positions = move.getNext()
			print('positions: %s' % (str(positions)))
			self.serialCorrespondent.write(" ".join(str(pos) for pos in positions))

		print()

	def performEmotion(self, emotionName, finishCriteria=Move._FINISH_CRITERIA_ALL):
		emotionMove = RoboEmotion._DEFAULT_EMOTION_MOVES.get(emotionName.lower())
		if emotionMove is not None:
			print('performing %s' % (emotionName.lower()))
			self.perform(emotionMove, finishCriteria=finishCriteria)
		else:
			raise ValueError('cannot recognize this emotion: %s' % (emotionName))



if __name__ == "__main__":
	roboEmotion = RoboEmotion(serialIdentifier=sys.argv[1])
	"""
	test the emotions
	"""
	for emotionName in RoboEmotion._DEFAULT_EMOTION_MOVES:
		roboEmotion.performEmotion(emotionName)
