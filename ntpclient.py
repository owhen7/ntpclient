#!/usr/bin/env python

'''
CS352 Assignment 1: Network Time Protocol
You can work with 1 other CS352 student

DO NOT CHANGE ANY OF THE FUNCTION SIGNATURES BELOW
'''


import socket
import struct
import datetime

#Authors: Cheyenne Pourkay and Owen Wexler

# format_string = '!cccciiq'
# bytesInFormat = struct.calcsize(format_string)
# new_packet = struct.pack(format_string,b'3',b'a',b'4',b'6', 7841,89154,9897765654)
# print(new_packet)
# (c0,c1,c2,c3,i0,i1,q0) = struct.unpack(format_string,new_packet)
# print ("got data " ,c0,c1,c2,c3,i0,i1,q0)
# modified_packet = bytearray(new_packet)
# modified_packet[0] = 6
# modified_packet[1] = 8
# modified_packet[4] = 0
# modified_packet[5] = 0
# modified_packet[6] = 0
# modified_packet[7] = 1
# print("the modified packet is", modified_packet)
# (c0,c1,c2,c3,i0,i1,q0) = struct.unpack(format_string,modified_packet)
# print ("Modified data " ,c0,c1,c2,c3,i0,i1,q0)

# 2b 3b 3b 8b 8b 8b 64 64 64 64 64 64 64 var var key? 128

def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    pkt = bytearray(48)
    # Set the first byte's bits to binary 00,011,011 for LI = 0, VN = 3, and Mode = 3.
    pkt[0] = 0b00011011

    #TODO: Construct an NTP Packet HERE.



    #Get the current time, locally on this machine.
    time_difference = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    timestamp_float = secs + float(time_difference.microseconds / 1000000.0)

    #We set T1, time 1, to timestamp_float.
    T1 = timestamp_float

    #TODO: Send the NTP Packet HERE.
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(server, port, family=socket.AF_INET, type=socket.SOCK_DGRAM)
    skt.sendto(pkt, addr[0][-1])
    #TODO: Retrieve the NTP Packet HERE.
    data, _ = skt.recvfrom(1024)
    # print(data, address)
    #TODO: Extract our T4 out of the NTP packet that we retrieved.
    sec, frac = struct.unpack('!II', data[40:48])
    T4tot = datetime.datetime(1900, 1, 1) + datetime.timedelta(seconds=sec + frac / 2 ** 32)
    time_difference2 = T4tot - datetime.datetime(1970, 1, 1)
    secs2 = time_difference2.days * 24.0 * 60.0 * 60.0 + time_difference2.seconds
    T4 = secs2 + float(time_difference2.microseconds / 1000000.0)


    return data, T1, T4
    #The above function returns a packet that is later used in ntpPktToRTTandOffset().
    

def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # fill in your code here

    #sample values
    rtt = 0.300 #<--- float
    offset = 0.050 #<--- Also a float


    return rtt, offset


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
    # byte_array = bytearray(b'Hello, World!')
    # time1 = 3.24
    # time2 = 1.54
    # realtime, offset = ntpPktToRTTandOffset(byte_array,time1,time2)
    # print(realtime)
    # print(offset)
    #
    # print("Beautiful! This printed!")
    print(getNTPTimeValue())