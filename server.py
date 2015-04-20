import struct
import random
import socket
BUFSIZE =65525

def gen_ipaddress():
	output=[]
	for i in range(4):
		output.append(random.randint(1,255))
	return output

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
		self.mesg=mesg
		self.sname=[0 for i in range(64)]
		self.file=[0 for i in range(128)]
		
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
		if self.mesg==2:
			packet += b'\x35\x01\x02'   #Option: (t=53,l=2) DHCP Message Type = DHCP Offer
		elif self.mesg==5:
			packet += b'\x35\x01\x05'	#Option: (t=53,l=5) DHCP Message Type = DHCP ACK
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
		print('Client mac_address is: %x-%x-%x-%x-%x-%x\n' %(self.chaddr[0],self.chaddr[1],self.chaddr[2],self.chaddr[3],self.chaddr[4],self.chaddr[5]))
		print('Option code is : %d, its value is: %d\n ' %(self.option[0],self.option[2]))
		print('------------------------------------------------------------------')

if __name__=='__main__':

	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock.bind(('',67))
	print('Listening for datagrams at {}'.format(sock.getsockname()))
	while True:
			data= sock.recv(BUFSIZE)
			rec_packet=Packet_resolve(data)
			print('DHCP Discover message:')
			rec_packet.printmesg()
			if(rec_packet.option[2]==1):
				socket_offer=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				socket_offer.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				offer_packet=DhcpPacket(2,1,6,0,rec_packet.tran,0,1,[0,0,0,0],gen_ipaddress(),[192,168,21,123],[0,0,0,0],rec_packet.chaddr,2)
				socket_offer.sendto(offer_packet.outputbinary_packet(),('255.255.255.255',68))
			data= sock.recv(BUFSIZE)
			request_packet=Packet_resolve(data)
			print('DHCP Request message:')
			request_packet.printmesg()
			if(request_packet.option[2]==3):
				socket_ack=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				socket_ack.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
				ack_packet=DhcpPacket(2,1,6,0,request_packet.tran,0,1,[0,0,0,0],request_packet.yiaddr,[192,168,21,123],[0,0,0,0],request_packet.chaddr,5)
				socket_ack.sendto(ack_packet.outputbinary_packet(),('255.255.255.255',68))
			
			