test:
	./uranium/scripts/uranium_standalone --uranium-dir=. test_no_deps ${ARGS}

build:
	./uranium/scripts/uranium_standalone --uranium-dir=.
