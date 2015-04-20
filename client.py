import struct
import random
import socket
from uuid import getnode as get_mac
BUFSIZE =65525

def gen_tranid():
	output=random.randint(0,429496729)
	return output
	
def gen_mac():
	tempt=[]
	for i in range(6):
		tempt.append(random.randint(0,255))
	for i in range(10):
		tempt.append(0)
	return tempt

class DhcpPacket:

	def __init__(self,op=0,htype=0,hlen=0,hops=0,tran_id=0,seconds=0,flags=0,ciaddr=[],yiaddr=[],siaddr=[],giaddr=[],chaddr=[],mesg=0) :
		self.Opcode=op
		self.Hardware_type=htype
		self.Hardware_addrlen=hlen
		self.Hops=hops
		self.Transaction_id=tran_id
		self.Seconds=seconds
		self.Flag=flags
		self.Client_ip_address=ciaddr
		self.Your_ip_address=yiaddr
		self.Server_ip_address=siaddr
		self.Relay_ip_address=giaddr
		self.Client_Ethernet_address=chaddr
		self.sname=[0 for i in range(64)]
		self.file=[0 for i in range(128)]
		self.mesg=mesg
		
	def outputbinary_packet(self):
		packet=b''
		packet += struct.pack('!B', self.Opcode)
		packet += struct.pack('!B', self.Hardware_type)
		packet += struct.pack('!B', self.Hardware_addrlen)
		packet += struct.pack('!B', self.Hops)
		packet += struct.pack('!I', self.Transaction_id)
		packet += struct.pack('!H', self.Seconds)
		packet += struct.pack('!H', self.Flag)
		packet += struct.pack('!4B', *(self.Client_ip_address))
		packet += struct.pack('!4B', *(self.Your_ip_address))
		packet += struct.pack('!4B', *(self.Server_ip_address))
		packet += struct.pack('!4B', *(self.Relay_ip_address))
		packet += struct.pack('!' + 'B'*16, *(self.Client_Ethernet_address))
		packet += struct.pack('!'+'B'*64, *(self.sname))
		packet += struct.pack('!'+'B'*128, *(self.file))
		if self.mesg==1:
			packet += b'\x35\x01\x01'   #Option: (t=53,l=1) DHCP Message Type = DHCP Discover
		elif self.mesg==3:
			packet += b'\x35\x01\x03'	#Option: (t=53,l=3) DHCP Message Type = DHCP Request
		packet += b'\xff'   #End Option
		return packet
		
class Packet_resolve:

	def __init__(self, packet):
		self.op=(struct.unpack('!B', packet[0:1]))[0]
		
		self.htype=(struct.unpack('!B', packet[1:2]))[0]
		
		self.hlen=(struct.unpack('!B', packet[2:3]))[0]
		
		self.hops=(struct.unpack('!B', packet[3:4]))[0]
		
		self.tran=(struct.unpack('!I', packet[4:8]))[0]
		
		self.sec=(struct.unpack('!H', packet[8:10]))[0]
		
		self.flag=(struct.unpack('!H', packet[10:12]))[0]
		
		data=struct.unpack('!4B', packet[12:16])
		self.ciaddr=[i for i in data]
		
		data=struct.unpack('!4B', packet[16:20])
		self.yiaddr=[i for i in data]
		
		data=struct.unpack('!4B', packet[20:24])
		self.siaddr=[i for i in data]
		
		data=struct.unpack('!4B', packet[24:28])
		self.giaddr=[i for i in data]
		
		data=struct.unpack('!' + 'B'*16, packet[28:44])
		self.chaddr=[i for i in data]
		
		data=struct.unpack('!3B', packet[236:239])
		self.option=[i for i in data]	
	
	def printmesg(self):
		print('Opcode is: %d\n' %self.op)
		print('Transaction_id is: %x\n' %self.tran)
		print('be assigned IP_address is: ')
		print('%d.%d.%d.%d\n' %(self.yiaddr[0],self.yiaddr[1],self.yiaddr[2],self.yiaddr[3]))
		print('Option code is : %d, its value is: %d\n ' %(self.option[0],self.option[2]))
		print('------------------------------------------------------------------')
if __name__=='__main__':

	xid=gen_tranid()
	mac=gen_mac()
	sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	#sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('',68))
	discover_packet=DhcpPacket(1,1,6,0,xid,0,1,[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],mac,1)
	sock.sendto(discover_packet.outputbinary_packet(),('255.255.255.255',67))
	data= sock.recv(BUFSIZE)
	offer_packet=Packet_resolve(data)
	print('DHCP Offer message:')
	offer_packet.printmesg()
	request_packet=DhcpPacket(1,1,6,0,xid+1,0,1,[0,0,0,0],offer_packet.yiaddr,offer_packet.siaddr,[0,0,0,0],mac,3)
	sock.sendto(request_packet.outputbinary_packet(),('255.255.255.255',67))
	data= sock.recv(BUFSIZE)
	ack_packet=Packet_resolve(data)
	print('DHCP ACK message:')
	ack_packet.printmesg()