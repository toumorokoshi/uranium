test:
	./uranium/scripts/uranium_standalone --uranium-dir=. test ${ARGS} -v -x -k develop_package_imports

build:
	./uranium/scripts/uranium_standalone --uranium-dir=.

publish:
	./uranium/scripts/uranium_standalone --uranium-dir=. publish

docs:
	./uranium/scripts/uranium_standalone --uranium-dir=. build_docs
