import pytest

from chexmix.table import gene


@pytest.fixture
def gene():
    return gene(
        'GENE:30245', 'wt1a', {
            'APPEARED_IN': [
                'ARTI:33297144', 'ARTI:32697314', 'ARTI:32633330', 'ARTI:29579206', 'ARTI:28738802', 'ARTI:28409341',
                'ARTI:27484451', 'ARTI:27417966', 'ARTI:27417964', 'ARTI:27078207', 'ARTI:25556170', 'ARTI:25446529',
                'ARTI:25145932', 'ARTI:25014653', 'ARTI:24722440', 'ARTI:24309184', 'ARTI:23860396', 'ARTI:23160512',
                'ARTI:22847133', 'ARTI:21871448', 'ARTI:21184241', 'ARTI:19666820', 'ARTI:17651719', 'ARTI:16292775'
            ]
        }
    )


def test_raw_id(gene):
    assert gene.raw_id == '30245'


def test_name(gene):
    assert gene.name == 'wt1a'
