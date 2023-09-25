#!/usr/bin/env python

'''
CS352 Assignment 1: Network Time Protocol
You can work with 1 other CS352 student

DO NOT CHANGE ANY OF THE FUNCTION SIGNATURES BELOW
'''

from socket import socket, AF_INET, SOCK_DGRAM
import struct
from datetime import datetime

#Authors: Dylan Pourkay and Owen Wexler

def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    #fill in your code here


    #TODO: Construct an NTP Packet HERE.



    #Get the current time, locally on this machine.
    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    timestamp_float = secs + float(time_difference.microseconds / 1000000.0)
    
    #We set T1, time 1, to timestamp_float.
    T1 = timestamp_float

    #TODO: Send the NTP Packet HERE.


    #TODO: Retrieve the NTP Packet HERE.


    #TODO: Extract our T4 out of the NTP packet that we retrieved.




    #return (pkt, T1, T4)
    #The above function returns a packet that is later used in ntpPktToRTTandOffset().
    

def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # fill in your code here

    #sample values
    rtt = 0.300; #<--- float
    offset = 0.050; #<--- Also a float


    return (rtt, offset)


    #This function takes an completed NTP data packet, as Python bytes, and input Unix
    #timestamps, as floating point numbers, and returns the Round Trip Time (RTT) and offset as a
    # Python two-tuple, with the first element being the round-trip time and the second element being
    # the offset. Both are floating point numbers in seconds.



def getCurrentTime(server="time.apple.com", port=123, iters=20) -> (float):
    # fill in your code here

    #currentTime = 
    pass
    #return currentTime

if __name__ == "__main__":
    #print(getCurrentTime())


    #This is a test call with made-up numbers to verify the function doesn't throw an error.
    byte_array = bytearray(b'Hello, World!')
    time1 = 3.24
    time2 = 1.54
    realtime, offffset = ntpPktToRTTandOffset(byte_array,time1,time2)
    print(realtime)
    print(offffset)

    print("Beautiful! This printed!")
