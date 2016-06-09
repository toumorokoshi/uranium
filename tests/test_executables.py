from uranium.exceptions import NonZeroExitCodeException


def test_hello_world(capfd, executables):
    desired_output = "hello, world"
    executables.run(["echo", "{0}".format(desired_output)],
                    subprocess_args={"stdin": None})
    out, err = capfd.readouterr()
    assert out.strip() == "hello, world"


def test_exception_contains_executable_name(capfd, executables):
    try:
        executables.run(["grep"])
    except NonZeroExitCodeException as e:
        assert "grep" in str(e)
    else:
        assert False
