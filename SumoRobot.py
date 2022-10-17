### Boilerplate code for animating robots
### Facilitates synchronzing different motor movements
### Author: Anton Mindstorms Hacks
### Source: https://antonsmindstorms.com/
### Tutorials: https://www.youtube.com/c/AntonsMindstormsHacks/

from projects.mpy_robot_tools.motor_sync import Mechanism, AMHTimer, sine_wave, linear_interpolation, linear, block_wave
from projects.mpy_robot_tools.serialtalk import SerialTalk
from projects.mpy_robot_tools.mshub import MSHubSerial
from projects.mpy_robot_tools.helpers import clamp_int
from hub import port
from mindstorms import Motor, MotorPair, MSHub

# Constants
BTN_X = 0x01
BTN_O = 0x02
BTN_SQUARE = 0x04
BTN_TRIANGLE = 0x08
BTN_L1 = 0x10
BTN_R1 = 0x20
BTN_L2 = 0x40
BTN_R2 = 0x80
BTN_LSTICK = 0x100
BTN_RSTICK = 0x200

DPAD_UP = 0x01
DPAD_DOWN = 0x02
DPAD_RIGHT = 0x04
DPAD_LEFT = 0x08


AXIS_SCALE = 5.12
THROTLE_SCALE = 10.24

# Setup
moveMotors = [ port.C.motor, port.D.motor ]
flipMotors = [ port.E.motor, port.F.motor ]
ur = SerialTalk( MSHubSerial('B'), timeout=20)
# Motion functions for syncronized motors
strafeLeftFuncs = [
    sine_wave(), sine_wave(100, 1000, 250)
]

strafeRightFuncs = [
    sine_wave(), sine_wave(100, 1000, 250)
]

legoHub = MSHub()
wheelPair = port.C.motor.pair(port.D.motor)
flipPair = port.E.motor.pair(port.F.motor)
#moveMech = Mechanism(moveMotors, strafeLeftFuncs)
#moveMech.shortest_path_reset()

# Start control loop
timer= AMHTimer()

while 1:
    ack, pad = ur.call('gamepad')
    if ack=="gamepadack":
        btns, dpad, left_x, left_y, right_x, right_y, throtle, back = pad
    else:
        btns, dpad, left_x, left_y, right_x, right_y, throtle, back = [0]*8
    #get scaled turn value between -100 and 100
    turn = left_x/AXIS_SCALE/2
    
    #flip function
    if btns & BTN_X:
        flipPair.run_to_position(-150, 150)
    else:
        flipPair.run_to_position(0, 0)


    if btns & BTN_R2:
        #get scaled speed value between -100 and 100
        speed = throtle/THROTLE_SCALE
        wheelPair.pwm(clamp_int(-speed - turn), clamp_int(speed - turn))
    elif btns & BTN_L2:
        speed = back/THROTLE_SCALE
        wheelPair.pwm(clamp_int(speed - turn), clamp_int(-speed - turn))
    else:
        wheelPair.pwm(0,0)



    #print(ack, pad) # Debug

    

#moveMech.stop()

