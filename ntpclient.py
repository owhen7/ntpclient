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


#https://tf.nist.gov/tf-cgi/servers.cgi <---- List of NTP servers to try. 

def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    pkt = bytearray(48)
    # Set the first byte's bits to binary 00,011,011 for LI = 0, VN = 3, and Mode = 3.
    pkt[0] = 0b00011011

    
    #Send the NTP Packet HERE.
    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = socket.getaddrinfo(server, port, family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #Snapshot exactly right before we sent the packet out so we have exact time. This is timestamp one.
    timeStampOne = datetime.datetime.utcnow()
    skt.sendto(pkt, addr[0][-1])


    #Retrieve the NTP Packet HERE.
    data, _ = skt.recvfrom(1024) #Retrieve the packet.
    # print(data, address)

    TimeStampFour = datetime.datetime.utcnow() #As soon as we collect it, timestamp now. This is timestamp four.
    #The packet should contain two timestamps, T2 and T3. We get to them later.
    

    #Calculate float time for Timestamp 1.
    time_difference = timeStampOne - datetime.datetime(1970, 1, 1)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    timestamp_float = secs + float(time_difference.microseconds / 1000000.0)
    #We set T1, time 1, to timestamp_float.
    T1 = timestamp_float

    #Calculate float time for Timestamp 4.
    time_difference = TimeStampFour - datetime.datetime(1970, 1, 1)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    timestamp_float = secs + float(time_difference.microseconds / 1000000.0)
    #We set T4, time 4, to timestamp_float.
    T4 = timestamp_float


    return data, T1, T4
    #The above function returns a packet that is later used in ntpPktToRTTandOffset().
    


#This function is probably wrong right now. It's saying rtt time is 1 millisecond. That's not right. That's definitely too short.
def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):

    #Find time 2 (I THINK?!) inside the byte array.
    sec, frac = struct.unpack('!II', pkt[32:40])
    T4tot = datetime.datetime(1900, 1, 1) + datetime.timedelta(seconds=sec + frac / 2 ** 32)
    time_difference2 = T4tot - datetime.datetime(1970, 1, 1)
    secs2 = time_difference2.days * 24.0 * 60.0 * 60.0 + time_difference2.seconds
    T2 = secs2 + float(time_difference2.microseconds / 1000000.0)


    #Find Time 3 (I THINK?!) inside the byte array.
    sec, frac = struct.unpack('!II', pkt[40:48])
    T4tot = datetime.datetime(1900, 1, 1) + datetime.timedelta(seconds=sec + frac / 2 ** 32)
    time_difference2 = T4tot - datetime.datetime(1970, 1, 1)
    secs2 = time_difference2.days * 24.0 * 60.0 * 60.0 + time_difference2.seconds
    T3 = secs2 + float(time_difference2.microseconds / 1000000.0)

    print(f"Time2 is: {T2:.10f}")
    print(f"Time3 is: {T3:.10f}")


    #Now we have T1, T2, T3, and T4. We can now calculate RTT and Offset.

    rtt = (T4 - T1) - (T3-T2)
    offset = ((T2-T1) + (T3-T4))/2


    print(f"rtt is: {rtt:.10f} seconds.")
    print(f"That is equal to : {rtt * 1000:.10f} milliseconds.")
    print(f"offset is: {offset:.10f} second.")

    return rtt, offset

    #This function takes an completed NTP data packet, as Python bytes, and input Unix
    #timestamps, as floating point numbers, and returns the Round Trip Time (RTT) and offset as a
    # Python two-tuple, with the first element being the round-trip time and the second element being
    # the offset. Both are floating point numbers in seconds.



def getCurrentTime(server="time.apple.com", port=123, iters=20) -> (float):

    offsets = []

    for i in range(iters):
        #print(f"Iteration {i}")
        (pkt,T1,T4) = getNTPTimeValue(server, port)
        (RTT,offset) = ntpPktToRTTandOffset(pkt,T1,T4)
        offsets.append(offset)

    averageOffset = sum(offsets) / len(offsets)

    time_difference = datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    timestamp_float = secs + float(time_difference.microseconds / 1000000.0)
    currentTime = timestamp_float + averageOffset

    return currentTime

if __name__ == "__main__":

    #print(getNTPTimeValue())


    packet, time1, time4 = getNTPTimeValue()
    print(f"Time1 is: {time1:.10f}")
    print(f"Time4 is: {time4:.10f}")
    
    #Now call the function that disects the packet right here.
    ntpPktToRTTandOffset(packet, time1, time4)

    
    
    #This is the final print statement. Turn off all other prints inside the repeating functions when you use it.
    #print(getCurrentTime())
