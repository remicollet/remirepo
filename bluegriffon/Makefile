SRCDIR := $(shell pwd)
NAME := $(shell basename $(SRCDIR))
include ../common/Makefile


checkcvs:
	for file in fire* moz* fin*; \
	do \
		if [ -f /home/extras/CVS/firefox/devel/$$file ]; then \
			echo "--------- $$file (firefox)"; \
			diff -u /home/extras/CVS/firefox/devel/$$file $$file; \
		elif [ -f /home/extras/CVS/xulrunner/devel/$$file ]; then \
			echo "--------- $$file (xulrunner)"; \
			diff -u /home/extras/CVS/xulrunner/devel/$$file $$file; \
		else \
			echo "--------- $$file NOTFOUND"; \
		fi; \
	done
