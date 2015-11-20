
lib-pyc:
	@python3 -m compileall libexec/ | grep -Ev '^Listing '
	@python3 -m compileall tsadm/ | grep -Ev '^Listing '
	@python3 -m compileall tsadmcli/ | grep -Ev '^Listing '


lib-pyo:
	@python3 -O -m compileall libexec/ | grep -Ev '^Listing '
	@python3 -O -m compileall tsadm/ | grep -Ev '^Listing '
	@python3 -O -m compileall tsadmcli/ | grep -Ev '^Listing '


compileall: lib-pyc lib-pyo


COMPILE_PHONY = lib-pyc lib-pyo compileall
