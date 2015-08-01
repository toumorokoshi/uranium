def test_hello_world(capfd, executables):
    desired_output = "hello, world"
    executables.run(["echo", "{0}".format(desired_output)],
                    subprocess_args={"stdin": None})
    out, err = capfd.readouterr()
    assert out.strip() == "hello, world"
