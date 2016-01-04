#!/usr/bin/env python
"""
Script for sending encoder changes to osc

/up 

"""
__author__ = "Dominik Schmidt-Philipp"
__copyright__ = "Copyright 2015, dSP"
__credits__ = ["Stefan Mavrodiev", "Dominik Schmidt-Philipp"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "dsp@freakaria.com"

####
# libraries
##
import os
import sys
import argparse
import time
# gpio Olimex
from pyA20Lime2.gpio import gpio
from pyA20Lime2.gpio import connector
#from pyA20Lime2.gpio import port

# OSC Client:
from pythonosc import osc_message_builder
from pythonosc import udp_client

if not os.getegid() == 0:
    sys.exit('Script must be run as root')


####
# configuration
##
enc0A = connector.gpio1p5
enc0B = connector.gpio1p7
enc0  = "/enc0"
####
# initialisation
##
gpio.init()

gpio.setcfg(enc0A, gpio.INPUT)
gpio.setcfg(enc0B, gpio.INPUT)

gpio.pullup(enc0A, gpio.PULLUP)
gpio.pullup(enc0B, gpio.PULLUP)

#def read_config (path) :



def osc_send (value,channel) :
    msg = osc_message_builder.OscMessageBuilder(address = channel)
    msg.add_arg(value, "i")
    msg = msg.build()
    client.send(msg)

def send (value) :
    msg = osc_message_builder.OscMessageBuilder(address = "/test")
    msg.add_arg(value, "i")
    msg = msg.build()
    client.send(msg)



if __name__ == "__main__":

    ####
    # startup arguments:
    ##
    parser = argparse.ArgumentParser()

    parser.add_argument("--ip", default="192.168.1.10",
                        help="IP the OSC client is sending to")
    parser.add_argument("--port", type=int, default=4003,
                        help="Port the OSC client is sending to")
    parser.add_argument("--address", default="",
                        help="OSC address string")
    args = parser.parse_args()
  

    ####
    # Client (sending)
    ##
    client = udp_client.UDPClient(args.ip, args.port)  
    
    a = 0
    state = 0
    ####
    # LOOP
    ##
    #send()
    try:
        print ("Press CTRL+C to exit")
        while True:

            time.sleep(.1)        
            if(a != gpio.input(enc0A)):
                
                if(a == gpio.input(enc0B)):
                    state = state + 1
                else:
                    state = state - 1
                
                a = gpio.input(enc0A)
              
                print (state)
                osc_send(state,enc0)



    
    
    except KeyboardInterrupt:
        print ("Goodbye.")

    
