import serial
import time

from calcLRC import calcLRC

# this will be specific to your setup
comp_port = 'COM6'

class MFC_Controller():
	def __init__(self):
		self.ser = serial.Serial(com_port, 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=3)
		time.sleep(1)
		print("Starting MFC Controller")
		print("Connected over serial at " + str(self.ser.name))
		self.turn_on()

	def is_healthy(self):
		# this serial code will be specific to your MFC
		if ('Srnm?????\x0d\x0a\r' in self.cmd_controller("?Srnm")):
			return(True)
		else:
			return(False)

	def set_setpoint(self, setpoint):
		rsp = "!setr" + ('%.2f' % setpoint)
		rsp = rsp + calcLRC(rsp) + '\x0d'
		if (self.cmd_controller("!Sinv" + ('%.3f' % setpoint)) == rsp):
			return(True)
		else:
			return(False)

	def read_flow(self):
		self.cmd_controller("?Flow")

	def cmd_controller(self, cmd):
		lrc = calcLRC(cmd)
		cmd = cmd + (lrc) + '\x0d\x0a'
		print(cmd)
		self.ser.write(cmd)
		ser_rsp = self.ser.read(200)
		print("Output from MFC Controller cmd with repr(): " + repr(ser_rsp))
		print("Output from MFC Controller cmd *without* repr(): " + ser_rsp)
		return(ser_rsp)

	def turn_on(self):
		# optional depending on what initial state you want to assert
		# having this on 'On' can cause some chattiness on the serial port
		#self.set_streaming_state("Echo")
		pass

def check_health():
	mc = MFC_Controller()
	if (mc.is_healthy() == True):
		# mfc controller is healthy and can continue
		print("MFC Controller is healthy, moving forward.\n\n")
		return(True)
	else:
		# something is wrong and need to trip a pause and alarm and wait for user input
		err_msg = "MFC is unhealthy, stopping calibration.\n\n"
		print(err_msg)
		return(False)

def run_cmds():
	mc_1 = MFC_Controller_One()
	# test responsiveness
	if mc_1.is_healthy():
		print("We're healthy!!!")
	# run various commands to test MFC
	#mc_1.set_setpoint(150)
	mc_1.read_flow()
	
run_cmds()


