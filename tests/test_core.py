import os
import papercut.args
import papercut.core


def pytest_generate_tests(metafunc):
    if 'resource' in metafunc.fixturenames:
        parent = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
        resources = [directory for directory, _, _ in os.walk(parent)]
        metafunc.parametrize('resource', resources)


def test_run(resource, tmpdir):
    args = papercut.args.Arguments()
    args.input = resource
    args.output = str(tmpdir)

    papercut.core.run(args)

    assert tmpdir.listdir()


def test_dryrun(resource, tmpdir):
    args = papercut.args.Arguments()
    args.dryrun = True
    args.input = resource
    args.output = str(tmpdir)

    papercut.core.run(args)

    assert not tmpdir.listdir()


def test_size(tmpdir):
    print tmpdir


def test_orientation_portrait(tmpdir):
    print tmpdir


def test_orientation_landscape(tmpdir):
    print tmpdir


def mtime(directory):
    def mtimes():
        for path in directory.visit('*.*'):
            yield path.stat().mtime

    return max(mtimes())


def test_overwrite(resource, tmpdir):
    args = papercut.args.Arguments()
    args.input = resource
    args.output = str(tmpdir)

    papercut.core.run(args)
    before = mtime(tmpdir)

    papercut.core.run(args)
    after = mtime(tmpdir)

    assert before != after


def test_no_overwrite(resource, tmpdir):
    args = papercut.args.Arguments()
    args.input = resource
    args.output = str(tmpdir)

    papercut.core.run(args)
    before = mtime(tmpdir)

    args.overwrite = False

    papercut.core.run(args)
    after = mtime(tmpdir)

    assert before == after