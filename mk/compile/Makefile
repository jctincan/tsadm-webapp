# $Id: Makefile 12370 2015-01-14 23:59:02Z jrms $

lib-pyc:
	@python3 -m compileall libexec/ | grep -Ev '^Listing '
	@python3 -m compileall tsadm/ | grep -Ev '^Listing '


lib-pyo:
	@python3 -O -m compileall libexec/ | grep -Ev '^Listing '
	@python3 -O -m compileall tsadm/ | grep -Ev '^Listing '


compileall: lib-pyc lib-pyo


COMPILE_PHONY = lib-pyc lib-pyo compileall
