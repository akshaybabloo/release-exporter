from release_exporter import version


def test_vesion():
    assert type(version.__version__) == str
