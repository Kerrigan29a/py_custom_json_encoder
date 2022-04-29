VERSION = $(shell python3 setup.py --version)

push:
	git push origin HEAD

release: clean
	git tag -a v$(VERSION) -m "Release version $(VERSION)"
	git push origin tag v$(VERSION)
