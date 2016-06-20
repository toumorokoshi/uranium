test:
	./uranium/scripts/uranium_standalone --uranium-dir=. test_no_deps ${ARGS}

test_full:
	./uranium/scripts/uranium_standalone --uranium-dir=. test ${ARGS} -v

build:
	./uranium/scripts/uranium_standalone --uranium-dir=.

distribute:
	./uranium/scripts/uranium_standalone --uranium-dir=. distribute
