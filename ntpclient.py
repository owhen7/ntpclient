from socket import socket, AF_INET, SOCK_DGRAM
import struct
from datetime import datetime

#Authors: Dylan Pourkay and Owen Wexler

def getNTPTimeValue(server="time.apple.com", port=123) -> (bytes, float, float):
    #fill in your code here
    pass
    #return (pkt, T1, T4)

def ntpPktToRTTandOffset(pkt: bytes, T1: float, T4: float) -> (float, float):
    # fill in your code here
    pass
    #return (rtt, offset)

def getCurrentTime(server="time.apple.com", port=123, iters=20) -> (float):
    # fill in your code here
    pass
    #return currentTime

if __name__ == "__main__":
    #print(getCurrentTime())

    time_difference = datetime.utcnow() - datetime(1970, 1, 1, 0, 0, 0)
    secs = time_difference.days*24.0*60.0*60.0 + time_difference.seconds
    timestamp_float = secs + float(time_difference.microseconds / 1000000.0)
    print("The number of seconds since Jan. 1, 1970 is: %f" % (timestamp_float))
