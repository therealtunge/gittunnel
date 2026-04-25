import subprocess
import sys
import requests
# "inbound" = what is sent the tunnel
# "outbound" = what is received by the tunnel

# this script will always execute on a new commit changing "inbound

def handle_inbound_http(inbound): # currently, http inbounds are one send and one recieve, no need to keep script alive
	match inbound[0]:
		case "get":
			print(f"got http get for {inbound[1]}")
			r = requests.get(inbound[1])
			o = ("http",r.status_code,r.text)
			print(f"got outbound: {r.status_code},{r.text[:100]}...")
			return (True, o)
		case _:
			print(f"invalid http request: {inbound[0]}")
			return (False)

def main():
	inbound_raw = ""
	with open("inbound") as inbound_fd:
		inbound_raw = inbound_fd.read()

	inbound = inbound_raw.split(',')
	print(f"recieved inbound: {inbound}")
	match (inbound[0]): # inbound type: "http"
		case "http":
			print("got http inbound")
			o = handle_inbound_http(inbound[1:])
			if (not o[0]):
				return 1

			with open("out/outbound", "wb") as outbound_fd:
				outbound_fd.write(bytes(o[1][2], "utf-8"))
			
			return 0
		case _:
			print("got invalid inbound")
			sys.exit(0)
main()