import os

try:
	os.remove("outbound")
except Exception:
	pass
finally:
	open("outbound", "a").close()