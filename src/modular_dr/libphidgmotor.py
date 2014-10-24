import modular_core.libfundamental as lfu
import Phidgets.Devices.Stepper as ST
import Phidgets.PhidgetException as phidg_except
#import modular_dr.Phidgets.Devices.Stepper as ST
#import modular_dr.Phidgets.PhidgetException as phidg_except

import os
import sys
import time

import pdb

max_offset = 55000

class motor_state(lfu.modular_object_qt):

	def __init__(self, parent = None, label = 'motor state', 
			motor = None, target_position = 0, target_tolerance = 1, 
			previous_state = None, max_time = 120, timed_out = False):
		self.motor = motor
		self.target_position = target_position
		self.target_tolerance = target_tolerance
		self.previous_state = previous_state
		self.max_time = max_time
		self.timed_out = timed_out
		lfu.modular_object_qt.__init__(self, 
			label = label, parent = parent)

	def set_in_state(self, *args, **kwargs):
		self.target_position = int(self.target_position)
		try:
			min_pos = int(self.parent.min_position)
			max_pos = int(self.parent.max_position)

		except AttributeError:
			min_pos = -max_offset
			max_pos =  max_offset

		if self.target_position < min_pos:
			print 'tried to moved below bounds'
			self.target_position = min_pos

		elif self.target_position > max_pos:
			print 'tried to moved above bounds'
			self.target_position = max_pos

		print 'motor going to:', self.target_position
		time_given = 0.0
		while not self.check_in_state() and not self.timed_out:
			try: self.motor.set_target_position(self.target_position)
			except AttributeError: print 'no motor!'; return
			time.sleep(0.1)
			time_given += 0.1
			if time_given > self.max_time:
				self.timed_out = True
				print 'set_in_state for state: ', self, ' timed out'

	def check_in_state(self):
		try: position = self.motor.get_position()
		except: position = None
		if not position is None:
			if position - self.target_tolerance < self.target_position and\
				position + self.target_tolerance > self.target_position:
				#print 'motor found in target state'
				return True

		else: print 'check_in_state() : no motor!'; return True
		#print 'motor not found in target state'
		return False
	
	def revert_to_previous(self):
		self.set_in_state(self.previous_state)

#55000 moves the syringes by ~31.5 cm
class motor_state_left(motor_state):

	def __init__(self, parent = None, motor = None):
		motor_state.__init__(self, parent = parent, 
			label = 'leftward state', motor = motor, 
			target_position = -max_offset)

	def set_in_state(self, *args, **kwargs):
		try: self.target_position = int(self.parent.min_position)
		except AttributeError: self.target_position = -max_offset
		motor_state.set_in_state(self, *args, **kwargs)

class motor_state_right(motor_state):

	def __init__(self, parent = None, motor = None):
		motor_state.__init__(self, parent = parent, 
			label = 'rightward state', motor = motor, 
			target_position = max_offset)

	def set_in_state(self, *args, **kwargs):
		try: self.target_position = int(self.parent.max_position)
		except AttributeError: self.target_position = max_offset
		motor_state.set_in_state(self, *args, **kwargs)

class motor_state_zero(motor_state):

	def __init__(self, parent = None, motor = None):
		motor_state.__init__(self, parent = parent, 
			label = 'zero state', motor = motor, 
			target_position = 0)

	def set_in_state(self, *args, **kwargs):
		try:
			min_pos = self.parent.min_position
			max_pos = self.parent.max_position
			self.target_position = int((int(max_pos) +\
								int(min_pos)) / 2.0)

		except AttributeError: self.target_position = 0
		motor_state.set_in_state(self, *args, **kwargs)

class motor_state_follow(motor_state):

	def __init__(self, parent = None, motor = None):
		motor_state.__init__(self, parent = parent, 
			label = 'follow state', motor = motor, 
			target_position = 0)

	def set_in_state(self, *args, **kwargs):
		self.target_position = args[0]
		motor_state.set_in_state(self, *args, **kwargs)

class motor_state_custom(motor_state):

	def __init__(self, motor, target):
		motor_state.__init__(self, label = 'custom state', 
				motor = motor, target_position = target)

	def set_settables(self, *args, **kwargs):
		self.handle_widget_inheritance(*args, from_sub = False)
		self.widg_templates.append(
			lgm.interface_template_gui(
				widget_layout = 'vert', 
				key = [	'label'	], 
				instance = [self], 
				widget = ['text'],
				box_label = 'Custom State Label', 
				initial = [self.label], 
				sizer_position = (0, 0)))
		self.widg_templates.append(
			lgm.interface_template_gui(
				widget_layout = 'vert', widget = ['spin'], 
				instance = [[self]], key = [['target_position']], 
				initial = [[self.target_position]], 
				value = [(-max_offset, max_offset)], 
				box_label = 'Target Position', 
				sizer_position = (0, 1)))
		super(motor_state_custom, self).set_settables(
								*args, from_sub = True)

'''
getAccel
setAccel
getMaxAccel
getMinAccel

getVel
getVelLimit
setVelLimit
getVelMax
getVelMin
'''

class motor(ST.Stepper):

	_connected_ = False

	def __init__(self, dex=0):
		try:
			ST.Stepper.__init__(self)

		except RuntimeError as e:
			print("RuntimeError:%s"%e.message)
			pdb.set_trace()

		try:
			self.openPhidget()

		except PhidgetException as e:
			print("PhidgetException%i:%s"%(e.code,e.detail))		
			exit(1)

		self.dex = dex
		try:
			self.waitForAttach(2000)
			self.setEngaged(self.dex, True)
			self._connected_ = True

		except phidg_except.PhidgetException:
			print 'motor couldnt be attached!'

	#within a valid range between AccerationMin and AccelerationMax
	def getAccel(self):
		return self.getAcceleration(self.dex)

	def setAccel(self, value):
		self.setAcceleration(self.dex, value)

	def get_position(self):
		try: return self.getCurrentPosition(self.dex)
		except: return None

	def getMaxAccel(self):
		return self.getAccelerationMax(self.dex)

	def getMinAccel(self):
		return self.getAccelerationMin(self.dex)

	#The units for this are steps per second
	def getVelLimit(self):
		return self.getVelocityLimit(self.dex)

	def setVelLimit(self, value):
		self.setVelocityLimit(self.dex, value)

	def getVel(self):
		return self.getVelocity(self.dex)

	def getVelMax(self):
		return self.getVelocityMax(self.dex)

	def getVelMin(self):
		return self.getVelocityMin(self.dex)

	def get_target_position(self):
		return self.getTargetPosition(self.dex)

	#Sets motors target position.		
	#If motor is engaged and it is between TargetMax and TargetMin, the motor will move
	def set_target_position(self, value):
		self.setTargetPosition(self.dex, value)

	#Resets default of current position
	#Will be useful if the defualt needs to be set to a specific location (0).
	def set_current_position(self, value):
		self.setCurrent(self.dex, value)

	def get_position_max(self):
		return self.getPositionMax(self.dex)

	def get_position_min(self):
		return self.getPositionMin(self.dex)

	def getCurrentLimit(self):
		return self.getCurrentLimit(self.dex)

	def setCurrentLimit(self, value):
		self.setCurrentLimit(self.dex, value)

	def get_stopped(self):
		return self.getStopped(self.dex)

	def get_serial_num(self):
		return self.getSerialNum(self.dex)

	def close_phidget(self):
		try: self.closePhidget(self.dex)
		except: print "Error in Close Phidget"

if __name__ == '__main__':
	print 'This is a library!'

if __name__ == 'modular_dr.libphidgmotor':
	if lfu.gui_pack is None: lfu.find_gui_pack()
	lgm = lfu.gui_pack.lgm







