from socket import *
import _thread
import threading
global account_arry
import time
account_arry={

'Sam':['samisgood',0,0,0],   #[0]:password,[1]:online:1 or offline:0,[2]:socket,[3]:hate_list
'Mary':['haha',0,0,0],
'God':['ohmygod',0,0,0],
'Frank':['frankeatsin',0,0,0],
'Win':['justdoit',0,0,0],
'Mark':['smart',0,0,0],
'Siang':['genius',0,0,0],
'John':['gogo',0,0,0],
'name':['password',0,0,0],
'simple':['simple',0,0,0]
}

def process_conversation(username,to_user):
	stop=0
	while stop==0:
		data = (account_arry[username][2].recv(1024).decode('ascii'))
		if(data=="End"):
			print("yes")
			stop=1
			break
		else:
			msg="Conversation message from "+username+": "+data
			if((account_arry[to_user][1]==1)and(account_arry[to_user][2]!=0)):
				account_arry[to_user][2].send(msg.encode('ascii'))
			elif((account_arry[to_user][1]==0)and(account_arry[to_user][2]==0)):
				thread.start_new_thread(wait_useronline, (to_user,msg))


#no online_user buffer queuing
def wait_useronline(user,message):
	stop=0
	while stop==0:
		if((account_arry[user][1]==1)and(account_arry[user][2]!=0)):
			account_arry[user][2].send(message.encode('ascii'))
			stop=1

#process other request
def process_anthor_request(username, clientaddr):
	global account_arry
	special=0
	success=0
	logout=0
	bro=0
	msg=""
	data = (account_arry[username][2].recv(1024).decode('ascii'))
	if(data=="listuser"):
		for a in list(account_arry.keys()):
			msg=msg+a+"\n"
	elif (data=="list_online_user"):
		for a in list(account_arry.keys()):
			if(account_arry[a][1]==1):
				msg=msg+a+"\n"
	elif (data=="logout"):
		msg="Logout successfully!!"
		account_arry[username][1]=0
		logout=1
	elif (data[0:9]=="broadcast"):
		msg="Broadcast message from "+username+": "
		msg=msg+data[10:]
		bro=1
	elif (data[0:4]=="hate"):
		data=data.split()
		account_arry[username][3]=data[1]
		msg="Put "+ data[1]+" in hate_list Successfully!! "
	elif (data[0:6]=="unhate"):
		data=data.split()
		account_arry[username][3]=0
		msg="Exclude "+ data[1]+" from hate_list Successfully!! "		
	elif (data[0:4]=="send"):
		special=1
		data=data.split()
		string=""
		for b in data[2:]:
			string=string+b+" "
		
		#check exist user or not and if he is online
		for a in list(account_arry.keys()):
			#online
			if((a==data[1])and(account_arry[a][1]==1)):
				success=1
				if(account_arry[data[1]][3]!=username):
					msg="Message from "+username+": "+string
					account_arry[data[1]][2].send(msg.encode('ascii'))
				break
			#offline
			elif((a==data[1])and(account_arry[a][1]==0)):
				success=1
				if(account_arry[data[1]][3]!=username):
					msg=msg="Message from "+username+": "+string
					_thread.start_new_thread(wait_useronline, (data[1],msg))
				break
		#no this user
		if(success==0):
			msg="Error!! "+data[1]+" is an invalid user"
			special=0
			
	elif(data[0:4]=="talk"):
		special=1
		data=data.split()
		to_user=data[1]
		#msg="Message from "+to_user+": "
		msg="Talk conversation setup successfully!!"
		account_arry[username][2].send(msg.encode('ascii'))
		process_conversation(username,to_user)
			
	else:
		msg="No this command"
		
	#broadcast 2nd if it used to exclude hate_list
	if(bro==1):
		for a in list(account_arry.keys()):
			if((account_arry[a][1]==1) and (a!=username)):
				if(account_arry[a][3]!=username):
					account_arry[a][2].send(msg.encode('ascii'))
	#process self request
	elif(special==0):
		account_arry[username][2].send(msg.encode('ascii'))
	
	
	if (logout==1):
		account_arry[username][2].close()
	else:
		process_anthor_request(username, clientaddr)

#process login
def handler(clientsocket, clientaddr):
	valid=0
	print ("Accepted connection from: ", clientaddr)
	data = (clientsocket.recv(1024).decode('ascii'))
	new_data=data.split(',')
	msg='0,Input account is wrong!!\nPlease Login again'
	# new_data[0]=login_username
	
	global account_arry
	for a in list(account_arry.keys()):
		if new_data[0]==a and account_arry[a][0]==new_data[1]:
			valid=1
			msg='1,Login Successfully!!'
			break
	if valid==0:
		clientsocket.send(msg.encode('ascii'))
		handler(clientsocket, clientaddr)
	else:
		account_arry[new_data[0]][1]=1
		account_arry[new_data[0]][2]=clientsocket
		account_arry[new_data[0]][2].send(msg.encode('ascii'))	
		
		#Note other_user login 
		for b in list(account_arry.keys()):
			if((account_arry[b][1]==1) and (new_data[0]!=b)):
				msg="@@@@@"+new_data[0]+" login just a moment ago!!"
				account_arry[b][2].send(msg.encode('ascii'))
				
		#process other request
		process_anthor_request(new_data[0], clientaddr)
	
	
 
if __name__ == "__main__":

	host = 'localhost'
	port = 55567
	buf = 1024
 
	addr = (host, port)
 
	serversocket = socket(AF_INET, SOCK_STREAM)
 
	serversocket.bind(addr)
 
	serversocket.listen(10) #可以listen10個
	
	while 1:
		print ("Server is listening for connections\n")
 
		clientsocket, clientaddr = serversocket.accept()
		_thread.start_new_thread(handler, (clientsocket, clientaddr))
	serversocket.close()