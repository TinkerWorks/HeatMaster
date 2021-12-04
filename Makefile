NT=nose2

MAINPACKAGE=heatmaster
TESTFOLDER=tests

NOSEOPTIONS= --with-coverage --junit-xml
prepare:
	pip3 install --user -r requirements.txt
prepare-test: prepare
	pip3 install --user -r tests/requirements.txt

nosetest: prepare-test
	PYTHONPATH=$(MAINPACKAGE) $(NT) $(NOSEOPTIONS) $(TESTFOLDER)
