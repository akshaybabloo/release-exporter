from release_exporter import version


def test_version():
    assert isinstance(version.__version__, str)
