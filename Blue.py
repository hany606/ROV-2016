#################################
#This code is made by: Hammer Heads
#ROV2016
#################################
#import libraries
from __future__ import division  #import division function to return float in division because python 2.7 do not support that in defult  
import smbus  #I2c library
import math   #math library to use log
import time   #time library to make function like millis in arduino
bus=smbus.SMBus(1)  #make object of i2c and set the setting
class Motor:  #make class for motors to make indiviual setting for each motor
	def __init__(self,add): #make function that run every time created the object
		self.add=add #make private variable to the address
		self.start=time.time()  #set the initial time point
		bus.write_byte(self.add,0)

		bus.write_word_data(self.add,0x00,0)
		bus.write_word_data(self.add,0x01,0)
		self.bbuffer=[0 for h in range(9)]
		self.read_reg=[0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0A]
		self.rpm1=0
		self.voltage_raw=0
		self.temp_raw=0
		self.current_raw=0
		self.identifier=0
		self.rpmTimer=0

	def millis(self):
		self.s2=time.time()
		self.s2=self.s2-self.start
		self.out=int(self.s2*1000)
		return (self.out)

	def setspeed(self,speed):
		self.speed=speed
		bus.write_word_data(self.add,0x00,self.speed>>8)
		bus.write_word_data(self.add,0x01,self.speed)
	
	def setzeros(self):
		bus.write_word_data(self.add,0x00,0)
		bus.write_word_data(self.add,0x01,0)

	def readBuff(self):
		for s in range(0,9):
			self.bbuffer[s]=bus.read_byte_data(self.add,self.read_reg[s])

	def update(self):
		self.bbuffer[8]= 0x00
		self.readBuff()
		self.rpm1 = (self.bbuffer[0] << 8) | self.bbuffer[1]
		self.voltage_raw = (self.bbuffer[2] << 8) | self.bbuffer[3]
		self.temp_raw = (self.bbuffer[4] << 8) | self.bbuffer[5]
		self.current_raw = (self.bbuffer[6] << 8) | self.bbuffer[7]
		self.identifier = self.bbuffer[8]
  		self.rpm1 = float(self.rpm1)/((self.millis()-self.rpmTimer)/1000.000000)*60/float(6)
  		self.rpmTimer=self.millis()

	def isAlive(self):
		#suppose to be 0xab
		return (self.identifier == 0xab)

	def voltage(self):
		return float(self.voltage_raw)/65536.000000*5.000000*6.450000
		#return (format((self.voltage_raw*0.0004921),'.2f'))

	def current(self):
		return (float(self.current_raw)-32767)/65535.000000*5.000000*14.706000
		#return (format(((self.current_raw-32767)*0.001122),'.2f'))

	def currentwi(self):
                self.bbuffer[6]=bus.read_byte_data(self.add,self.read_reg[6])
                self.bbuffer[7]=bus.read_byte_data(self.add,self.read_reg[7])
                self.current_raw = (self.bbuffer[6] << 8) | self.bbuffer[7]
		return (float(self.current_raw)-32767)/65535.000000*5.000000*14.706000
		#return (format(((self.current_raw-32767)*0.001122),'.2f'))

	def temperature(self):
		self.resistance = 3300/(65535/float(self.temp_raw)-1)
		#self.steinhart=0
		self.steinhart = self.resistance / 10000
		self.steinhart = math.log(self.steinhart)
		self.steinhart /= 3900
		self.steinhart += 1.0 / (25 + 273.15)
		self.steinhart -= 273.15
		return self.steinhart

	def rpm(self):
		return self.rpm1





		
