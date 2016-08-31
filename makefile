test:
	./uranium/scripts/uranium_standalone --uranium-dir=. test ${ARGS} -v

build:
	./uranium/scripts/uranium_standalone --uranium-dir=.

distribute:
	./uranium/scripts/uranium_standalone --uranium-dir=. distribute

docs:
	./uranium/scripts/uranium_standalone --uranium-dir=. build_docs
