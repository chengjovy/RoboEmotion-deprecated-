import sys
import tkinter as tk
import thread, time
import serial

SERIAL_PORT_IDENTIFIER = "/dev/cu.usbmodem14111"
BAUD_RATE = 9600
ARDUINO = serial.Serial(SERIAL_PORT_IDENTIFIER, BAUD_RATE)

SERVO_NAMES = ["Finger", "Wrist-I", "Wrist-II", "Elbow", "Shoulder", "Base"]
SERVO_DEFAULT_POSITION = (180, 90, 90, 90, 90, 90)
SERVO_SLIDER = []


def sendServoPositionOverSerial():
	global SERVO_SLIDER, ARDUINO
	last = ()
	while True:
		current = tuple([s.get() for s in SERVO_SLIDER])
		if str(current) != str(last):
			print(current)
			sys.stdout.flush()
			last = current
			# write to serial port to arduino
			print('--- debug ---')
			msg = " ".join([str(pos) for pos in current]) + "\n"
			print(msg)
			ARDUINO.write(msg)
			# print "RESPONSE: " + ARDUINO.readline()
		time.sleep(0.05)

def main():
	root = tk.Tk()

	# initialize the slider in Tkinter
	for name in SERVO_NAMES:
		w = tk.Label(root, text=name)
		w.pack(padx=10)

		if name == "Finger":
			w = tk.Scale(root,
				from_=120,
				to_=180,
				orient=tk.HORIZONTAL,
				length=600,
				tickinterval=10)
		else:
			w = tk.Scale(root,
				from_=0,
				to_=180,
				orient=tk.HORIZONTAL,
				length=600,
				tickinterval=10)
		w.pack(padx=10)
		SERVO_SLIDER.append(w)

	# set to default positions
	for i, s in enumerate(SERVO_SLIDER):
		s.set(SERVO_DEFAULT_POSITION[i])

	thread.start_new_thread(sendServoPositionOverSerial, ())
	# start Tkinter
	root.mainloop()


if __name__ == "__main__":
	main()
