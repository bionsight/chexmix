import json

import requests
from chexmix.datasources import pubtator

pubtator_post_mock = "\n".join([json.dumps(d) for d in [{
    "id": "2890742",
    "passages": [{
        "annotations": [{
            "id": "10", "infons": {"identifier": "-", "type": "Chemical"},
            "text": "aryltetralin lignan", "locations": [{"offset": 156, "length": 19}]}, {
            "id": "11", "infons": {"identifier": "93608", "type": "Species"},
            "text": "Podophyllum hexandrum", "locations": [{"offset": 220, "length": 21}]}, {
            "id": "12", "infons": {"identifier": "35933", "type": "Species"},
            "text": "P. peltatum", "locations": [{"offset": 246, "length": 11}]}, {
            "id": "13", "infons": {"identifier": "93608", "type": "Species"},
            "text": "P. hexandrum", "locations": [{"offset": 297, "length": 12}]}, {
            "id": "14", "infons": {"identifier": "MESH:D017705", "type": "Chemical"},
            "text": "lignans", "locations": [{"offset": 385, "length": 7}]}, {
            "id": "15", "infons": {"identifier": "35933", "type": "Species"},
            "text": "P. peltatum", "locations": [{"offset": 408, "length": 11}]}, {
            "id": "16", "infons": {"identifier": "MESH:D017705", "type": "Chemical"},
            "text": "lignan", "locations": [{"offset": 474, "length": 6}]}, {
            "id": "17", "infons": {"identifier": "93608", "type": "Species"},
            "text": "P. hexandrum", "locations": [{"offset": 492, "length": 12}]}]}],
    'pmid': 2890742,
    'year': 1987}, {
    "id": "76398",
    "passages": [{
        "annotations": [{
            "id": "3", "infons": {"identifier": "MESH:D003218", "type": "Disease"},
            "text": "penile condylomata acuminata", "locations": [{"offset": 21, "length": 28}]}, {
            "id": "4", "infons": {"identifier": "MESH:D011034", "type": "Chemical"},
            "text": "podophyllotoxin", "locations": [{"offset": 68, "length": 15}]}, {
            "id": "5", "infons": {"identifier": "MESH:D003078", "type": "Chemical"},
            "text": "colchicine", "locations": [{"offset": 88, "length": 10}]}]}, {
        "annotations": [{
            "id": "17", "infons": {"identifier": "35933", "type": "Species"},
            "text": "Podophyllum peltatum", "locations": [{"offset": 181, "length": 20}]}, {
            "id": "18", "infons": {"identifier": "93608", "type": "Species"},
            "text": "Podophyllum emodi", "locations": [{"offset": 206, "length": 17}]}, {
            "id": "19", "infons": {"identifier": "MESH:D011034", "type": "Chemical"},
            "text": "podophyllotoxin", "locations": [{"offset": 228, "length": 15}]}, {
            "id": "20", "infons": {"identifier": "MESH:D003078", "type": "Chemical"},
            "text": "colchicine", "locations": [{"offset": 252, "length": 10}]}, {
            "id": "21", "infons": {"identifier": "MESH:D003218", "type": "Disease"},
            "text": "penile condylomata acuminata", "locations": [{"offset": 280, "length": 28}]}, {
            "id": "22", "infons": {"identifier": "9606", "type": "Species"},
            "text": "men", "locations": [{"offset": 316, "length": 3}]}, {
            "id": "23", "infons": {"identifier": "9606", "type": "Species"},
            "text": "patients", "locations": [{"offset": 354, "length": 8}]}, {
            "id": "24", "infons": {"identifier": "MESH:D003078", "type": "Chemical"},
            "text": "colchicine", "locations": [{"offset": 561, "length": 10}]}, {
            "id": "25", "infons": {"identifier": "MESH:D011034", "type": "Chemical"},
            "text": "podophyllotoxin", "locations": [{"offset": 665, "length": 15}]}, {
            "id": "26", "infons": {"identifier": "9606", "type": "Species"},
            "text": "patients", "locations": [{"offset": 863, "length": 8}]}, {
            "id": "27", "infons": {"identifier": "MESH:D003078", "type": "Chemical"},
            "text": "colchicine", "locations": [{"offset": 1071, "length": 10}]}]}],
    'pmid': 76398,
    'year': 1978}]])


def test_fetch_annotations(monkeypatch, request):
    def res(*args, **kwargs):
        class MockResponse:
            text = pubtator_post_mock
        return MockResponse()

    monkeypatch.setattr(requests, 'post', res)
    pubtator_table = pubtator.fetch_annotations(['2890742', '76398'])
    request.config.cache.set('table', pubtator_table)
    assert pubtator_table == [{
        'id': '2890742',
        'passages': [{
            'annotations': [{
                'id': '10', 'infons': {'identifier': '-', 'type': 'Chemical'},
                'text': 'aryltetralin lignan', 'locations': [{'offset': 156, 'length': 19}]}, {
                'id': '11', 'infons': {'identifier': '93608', 'type': 'Species'},
                'text': 'Podophyllum hexandrum', 'locations': [{'offset': 220, 'length': 21}]}, {
                'id': '12', 'infons': {'identifier': '35933', 'type': 'Species'},
                'text': 'P. peltatum', 'locations': [{'offset': 246, 'length': 11}]}, {
                'id': '13', 'infons': {'identifier': '93608', 'type': 'Species'},
                'text': 'P. hexandrum', 'locations': [{'offset': 297, 'length': 12}]}, {
                'id': '14', 'infons': {'identifier': 'MESH:D017705', 'type': 'Chemical'},
                'text': 'lignans', 'locations': [{'offset': 385, 'length': 7}]}, {
                'id': '15', 'infons': {'identifier': '35933', 'type': 'Species'},
                'text': 'P. peltatum', 'locations': [{'offset': 408, 'length': 11}]}, {
                'id': '16', 'infons': {'identifier': 'MESH:D017705', 'type': 'Chemical'},
                'text': 'lignan', 'locations': [{'offset': 474, 'length': 6}]}, {
                'id': '17', 'infons': {'identifier': '93608', 'type': 'Species'},
                'text': 'P. hexandrum', 'locations': [{'offset': 492, 'length': 12}]}]}],
        'pmid': 2890742, 'year': 1987}, {
        'id': '76398',
        'passages': [{
            'annotations': [{
                'id': '3', 'infons': {'identifier': 'MESH:D003218', 'type': 'Disease'},
                'text': 'penile condylomata acuminata', 'locations': [{'offset': 21, 'length': 28}]}, {
                'id': '4', 'infons': {'identifier': 'MESH:D011034', 'type': 'Chemical'},
                'text': 'podophyllotoxin', 'locations': [{'offset': 68, 'length': 15}]}, {
                'id': '5', 'infons': {'identifier': 'MESH:D003078', 'type': 'Chemical'},
                'text': 'colchicine', 'locations': [{'offset': 88, 'length': 10}]}]}, {
            'annotations': [{
                'id': '17', 'infons': {'identifier': '35933', 'type': 'Species'},
                'text': 'Podophyllum peltatum', 'locations': [{'offset': 181, 'length': 20}]}, {
                'id': '18', 'infons': {'identifier': '93608', 'type': 'Species'},
                'text': 'Podophyllum emodi', 'locations': [{'offset': 206, 'length': 17}]}, {
                'id': '19', 'infons': {'identifier': 'MESH:D011034', 'type': 'Chemical'},
                'text': 'podophyllotoxin', 'locations': [{'offset': 228, 'length': 15}]}, {
                'id': '20', 'infons': {'identifier': 'MESH:D003078', 'type': 'Chemical'},
                'text': 'colchicine', 'locations': [{'offset': 252, 'length': 10}]}, {
                'id': '21', 'infons': {'identifier': 'MESH:D003218', 'type': 'Disease'},
                'text': 'penile condylomata acuminata', 'locations': [{'offset': 280, 'length': 28}]}, {
                'id': '22', 'infons': {'identifier': '9606', 'type': 'Species'},
                'text': 'men', 'locations': [{'offset': 316, 'length': 3}]}, {
                'id': '23', 'infons': {'identifier': '9606', 'type': 'Species'},
                'text': 'patients', 'locations': [{'offset': 354, 'length': 8}]}, {
                'id': '24', 'infons': {'identifier': 'MESH:D003078', 'type': 'Chemical'},
                'text': 'colchicine', 'locations': [{'offset': 561, 'length': 10}]}, {
                'id': '25', 'infons': {'identifier': 'MESH:D011034', 'type': 'Chemical'},
                'text': 'podophyllotoxin', 'locations': [{'offset': 665, 'length': 15}]}, {
                'id': '26', 'infons': {'identifier': '9606', 'type': 'Species'},
                'text': 'patients', 'locations': [{'offset': 863, 'length': 8}]}, {
                'id': '27', 'infons': {'identifier': 'MESH:D003078', 'type': 'Chemical'},
                'text': 'colchicine', 'locations': [{'offset': 1071, 'length': 10}]}]}],
        'pmid': 76398, 'year': 1978}]


def test_build_annotation_table(request):
    assert pubtator.build_annotation_table(request.config.cache.get('table', None)) == {
        76398: {
            'MSHD:D003078': {'id': 'MESH:D003078', 'locations': [{'length': 10, 'offset': 1071}],
                             'text': 'colchicine', 'type': 'Chemical'},
            'MSHD:D003218': {'id': 'MESH:D003218', 'locations': [{'length': 28, 'offset': 280}],
                             'text': 'penile condylomata acuminata', 'type': 'Disease'},
            'MSHD:D011034': {'id': 'MESH:D011034', 'locations': [{'length': 15, 'offset': 665}],
                             'text': 'podophyllotoxin', 'type': 'Chemical'},
            'TAXO:35933': {'id': '35933', 'locations': [{'length': 20, 'offset': 181}],
                           'text': 'Podophyllum peltatum', 'type': 'Species'},
            'TAXO:93608': {'id': '93608', 'locations': [{'length': 17, 'offset': 206}],
                           'text': 'Podophyllum emodi', 'type': 'Species'},
            'TAXO:9606': {'id': '9606', 'locations': [{'length': 8, 'offset': 863}],
                          'text': 'patients', 'type': 'Species'}},
        2890742: {
            'MSHD:D017705': {'id': 'MESH:D017705', 'locations': [{'length': 6, 'offset': 474}],
                             'text': 'lignan', 'type': 'Chemical'},
            'TAXO:35933': {'id': '35933', 'locations': [{'length': 11, 'offset': 408}],
                           'text': 'P. peltatum', 'type': 'Species'},
            'TAXO:93608': {'id': '93608', 'locations': [{'length': 12, 'offset': 492}],
                           'text': 'P. hexandrum', 'type': 'Species'}}}
