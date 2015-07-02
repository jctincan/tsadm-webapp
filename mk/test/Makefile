# $Id: Makefile 12370 2015-01-14 23:59:02Z jrms $

REGR_TESTS_OPTS := ''


test-all: test-urls-digest test-regression


test-clean:
	@rm -fv fail-report-*.txt


test-gen-urls-digest:
	@cat tsadm_tests/test_urls.txt | python3 -m tsadm_tests.gen_urls_digest >tsadm_tests/test_urls_digest.txt
	@cat tsadm_tests/test_urls_digest.txt


test-urls-digest:
	@cat tsadm_tests/test_urls.txt | python3 -m tsadm_tests.gen_urls_digest >/tmp/test_urls_digest.txt
	@md5sum tsadm_tests/test_urls_digest.txt /tmp/test_urls_digest.txt


test-regression: test-clean
	@python3 -m tsadm_tests.regression $(REGR_TESTS_OPTS)


test-regression-ssl: test-clean
	@TSADM_REGR_TESTS_SSL=1 python3 -m tsadm_tests.regression $(REGR_TESTS_OPTS)


TEST_PHONY = test-all test-clean test-gen-urls-digest test-urls-digest test-regression test-regression-ssl
