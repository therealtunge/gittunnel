import os

try:
	os.remove("out/outbound")
except Exception:
	pass
finally:
	open("out/outbound", "a").close()