
import serial


def getUsage():
	usage = "\n"
	usage += "Commands:\n"
	usage += " 1. GET <SERVO_NUMBER>\n"
	usage += " 2. SET <SERVO_NUMBER> <POSITION>\n"
	usage += "(Note:\n"
	usage += " - The servo number starts from 0.\n"
	usage += " - The position should be within range 0 ~ 180)\n"
	usage += "\n"
	return usage

if __name__ == "__main__":
	arduino = serial.Serial('/dev/cu.usbmodem14121', 9600)
	while True:
		command = raw_input(">>> ")
		if command.lower().startswith("h"):
			print(getUsage())
		else:
			arduino.write(command)
			print "RESPONSE: " + arduino.readline()
