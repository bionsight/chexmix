import chexmix.utils as utils


def test_iter_grouper():
    sample = range(0, 10)
    groups = [list(group) for group in utils.iter_grouper(2, sample)]
    assert all(len(group) == 2 for group in groups)
