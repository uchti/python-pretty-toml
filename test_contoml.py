from collections import OrderedDict
import json
import contoml

def test_it_should_correctly_load_sample_file():

    toml_file = contoml.load('dateless_sample.toml')

    assert set(toml_file.keys()) == {'fruit', 'clients', '', 'owner', 'database', 'servers', 'extra'}

    json_file = json.load(open('dateless_sample.json'))

    assert json_file == toml_file.primitive


def test_works_fine_without_anonymous_section():

    toml =  """
[apple]
color = "green"
name = "yonagold"
"""

    file = contoml.loads(toml)
    assert set(file.keys()) == {'apple'}
    assert file['apple']['color'] == 'green'
    assert file['apple']['name'] == 'yonagold'


def test_table_should_insert_new_entries_right_after_last_entry():

    toml =  """
[apple]
color = "green"
name = "yonagold"


# Nevermind
"""

    file = contoml.loads(toml)

    file['apple']['other_name'] = 'nevermind'

    expected_toml = """
[apple]
color = "green"
name = "yonagold"
"other_name" = nevermind


# Nevermind
"""

    assert expected_toml == file.dumps()


def test_should_insert_with_sensible_indentation_in_tables():

    toml = """
[apple]
    color = "green"
    name = "yonagold"


# Nevermind
"""

    file = contoml.loads(toml)

    file['apple']['key'] = 23

    expected_toml = """
[apple]
    color = "green"
    name = "yonagold"
    key = 23


# Nevermind
"""

    assert file.dumps() == expected_toml


def test_setting_primitive_value_on_non_existing_section():

    f = contoml.new()
    f['details']['id'] = 12

    assert f.dumps() == '[details]\nid = 12\n\n'


def test_creating_an_array_of_tables():

    f = contoml.new()

    f.array('fruit')[0]['name'] = 'banana'
    f.array('fruit')[1]['name'] = 'grapes'
    f['fruit'][1]['name'] = 'grapes'

    assert f.dumps() == """[[fruit]]
name = banana

[[fruit]]
name = grapes

"""


def test_creating_tables_from_dicts():
    f = contoml.new()
    f['my table'] = OrderedDict((('really', False), ('noo', 'yeah!')))
    assert f.dumps() == """["my table"]
really = false
noo = "yeah!"
"""

    f['my table']['noo'] = 'indeed'
    assert f.dumps() == """["my table"]
really = false
noo = indeed
"""

    f['my table'] = OrderedDict((('another_dict', True), ('should replace other one', 'right')))
    assert f.dumps() == """["my table"]
"another_dict" = true
"should replace other one" = right
"""


def test_appending_to_an_array_of_tables():

    f = contoml.new()

    f.array('person').append(OrderedDict([('name', 'Chuck'), ('id', 12)]))

    assert f.dumps() == """[[person]]
name = Chuck
id = 12

"""

    f['person'].append(OrderedDict([('name', 'Kcuhc'), ('id', 21)]))

    assert f.dumps() == """[[person]]
name = Chuck
id = 12

[[person]]
name = Kcuhc
id = 21

"""
