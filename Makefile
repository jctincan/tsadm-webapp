SHELL = /bin/bash
SRC_DIR = $(shell pwd)
UTILS_DIR = $(SRC_DIR)/mk/_utils
BASE_DIR = $(shell dirname $(shell dirname $(shell dirname $(SRC_DIR))))


default:
	@echo 'No default task'


include mk/compile/Makefile
include mk/django/Makefile


clean: test-clean
	@find . -type d -name __pycache__ | xargs rm -vrf
	@find . -type f -name '*.py[co]' | xargs rm -vrf


uwsgi-reload: clean compileall
	touch /tmp/uwsgi-tsadm.reload


config-grep:
	@echo "*** Domains"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'tsadm.local' * || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'test.tsadm.tincan' * || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ --exclude-dir=templates 'tsadm.tincan' * || true
	@echo
	@echo "*** Debug"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ -i 'debug' * || true
	@echo
	@echo "*** Ports"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'PORT' * || true
	@echo
	@echo "*** Sockets"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'socket' etc/ || true
	@echo
	@echo "*** Certificates"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ '.crt' * || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ '.key' * || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ '.pem' * || true
	@echo
	@echo "*** Apache"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'DocumentRoot' etc/apache/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'Alias ' etc/apache/ || true
	@echo
	@echo "*** UWSGI"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'chdir ' etc/uwsgi/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'touch-reload ' etc/uwsgi/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'path ' etc/uwsgi/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'id ' etc/uwsgi/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'pidfile ' etc/uwsgi/ || true
	@echo
	@echo "*** xinetd"
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'server ' etc/xinetd/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'server_args ' etc/xinetd/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'user ' etc/xinetd/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'group ' etc/xinetd/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'log_type ' etc/xinetd/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'only_from ' etc/xinetd/ || true
	@grep -rnF --exclude=Makefile --exclude-dir=__pycache__ 'id ' etc/xinetd/ || true
	@echo
	@echo "*** DB"
	@grep -nE --exclude=Makefile --exclude-dir=__pycache__ -H 'USER|PASSWORD|PORT|DATABASE|HOST' tsadm/db/config.py || true
	@echo
	@echo "*** VERSION.txt"
	@cat VERSION.txt


enc-check:
	@echo '*** ENCODE'
	@grep -rnF '.encode(' .
	@echo
	@echo '*** DECODE'
	@grep -rnF '.decode(' .
	@echo
	@echo '*** OPEN'
	@grep -rnF ' open(' .
	@echo
	@echo '*** CONTENT-TYPE'
	@grep -rnF --exclude=Makefile 'content_type=' .


install-deps:
	apt-get install python3-django
	apt-get install python3-mysql.connector
	apt-get install python3-lxml

.PHONY: default clean uwsgi-reload config-grep enc-check install-deps $(DJANGO_PHONY) $(COMPILE_PHONY)
