import serial
import time

class Arduino:
	def __init__(self):
		#SETEO ARDUINO
		try:
			self.arduino = serial.Serial('COM3', 9600)
			self.arduinoOk = True
		except:
			self.arduinoOk= False
		time.sleep(2)

	def sendArduino(self, value):
		if(self.arduinoOk):
			self.arduino.write(value)
		else:
			print("no se pudo enviar el mensaje a Arduino")