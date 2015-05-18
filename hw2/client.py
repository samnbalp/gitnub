from socket import *
from getpass import getpass
import time
import _thread
import sys

#recv message
def handler(clientsocket):
	valid=1
	while valid==1:
		data = (clientsocket.recv(1024).decode('ascii'))
		if (data[0:9]=="Broadcast"):
			print("\n"+data+"\n>>",end="")
		elif(data[0:7]=="Message"):
			print("\n"+data+"\n>>",end="")
		elif(data[0:5]=="@@@@@"):
			print("\n"+data[5:]+"\n>>",end="")
		else:
			print(data)
		if data=="Logout successfully!!":
			valid=0
			clientsocket.close()
		
#input request
def enter_command_mod(clientsocket):
	loop=1
	input_data=""
	output_data=""
	while loop==1:
		time.sleep(2)
		print ("\n>>",end="")
		data = input("")
		if(data[0:4]=="talk"):
			output_data=output_data+data+"\n"
			print("")
			input_data = input("")
			while(input_data!='End'):
				output_data=output_data+input_data+'\n'
				input_data = input("")
			clientsocket.send(output_data.encode('ascii'))
		else:
			clientsocket.send(data.encode('ascii'))				
			if(data=="logout"):
				loop=0
			
if __name__ == '__main__':
 
	host = 'localhost'
	port = 55567
	buf = 1024
 
	addr = (host, port)
 
	clientsocket = socket(AF_INET, SOCK_STREAM)
 
	clientsocket.connect(addr)
	
	msg=''
	valid=0
	while valid==0:
		msg=""
		data = input(">>Please input account: ")
		if(data=="exit"):
			sys.exit(0)
		msg=msg+data+','
		data =getpass(prompt='>>Please input Password: ')
		msg=msg+data
		if not msg:
			break
		else:
			clientsocket.send(msg.encode('ascii'))
			data = clientsocket.recv(buf)
			if not data:
				break
			else:
				out=(data.decode('ascii')).split(',')
				#valid user
				if out[0]=='1':
					print(out[1])
					#thread to recv message
					_thread.start_new_thread(handler, (clientsocket,))
					#function let user to request
					enter_command_mod(clientsocket)
					time.sleep(3)
					clientsocket = socket(AF_INET, SOCK_STREAM)
					clientsocket.connect(addr)
				#unvalid user
				elif out[0]=='0':
					print(out[1])