test:
	./uranium/scripts/uranium_standalone --uranium-dir=. test_no_deps ${ARGS}

test_full:
	./uranium/scripts/uranium_standalone --uranium-dir=. test ${ARGS}

build:
	./uranium/scripts/uranium_standalone --uranium-dir=.
