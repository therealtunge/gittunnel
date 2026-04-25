import argparse
import socket
import sys
from _thread import *
import subprocess
import os
try:
	listening_port = 10019
except KeyboardInterrupt:
	print("\n[*] User has requested an interrupt")
	print("[*] Application Exiting.....")
	sys.exit()

parser = argparse.ArgumentParser()

parser.add_argument('--max_conn', help="Maximum allowed connections", default=5, type=int)
parser.add_argument('--buffer_size', help="Number of samples to be used", default=8192, type=int)

args = parser.parse_args()
max_connection = args.max_conn
buffer_size = args.buffer_size

def start():	#Main Program
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind(('', listening_port))
		sock.listen(max_connection)
		print("[*] Server started successfully [ %d ]" %(listening_port))
	except Exception as e:
		print("[*] Unable to Initialize Socket")
		print(e)
		sys.exit(2)

	while True:
		try:
			conn, addr = sock.accept() #Accept connection from client browser
			data = conn.recv(buffer_size) #Recieve client data
			start_new_thread(conn_string, (conn,data, addr)) #Starting a thread
		except KeyboardInterrupt:
			sock.close()
			print("\n[*] Graceful Shutdown")
			sys.exit(1)

def conn_string(conn, data, addr):
	first_line = data.split(b'\n')[0]

	url = first_line.split()[1]

	http_pos = url.find(b'://') #Finding the position of ://
	if(http_pos==-1):
		temp=url
	else:
		temp = url[(http_pos+3):]
		
	port_pos = temp.find(b':')

	webserver_pos = temp.find(b'/')
	if webserver_pos == -1:
		webserver_pos = len(temp)
	webserver = ""
	port = -1
	if(port_pos == -1 or webserver_pos < port_pos):
		port = 80
		webserver = temp[:webserver_pos]
	else:
		port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
		webserver = temp[:port_pos]
	proxy_server(webserver, port, conn, addr, data)

def proxy_server(webserver, port, conn, addr, data):
	payload = f"http,"
	print(data, payload)
	try:
		os.remove("inbound")
	except Exception:
		pass
	finally:
		with open("inbound", "a+") as inbound_fd:
			inbound_fd.write(payload)
		subprocess.run(["git", "add", "."])
		subprocess.run(["git", "commit", "-m", "send outbound"])
		subprocess.run(["git", "push"])


if __name__== "__main__":
	start()