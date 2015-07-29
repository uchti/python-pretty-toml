
from contoml.elements import traversal as t, factory as element_factory


def table_assignment_spacing(toml_file_elements):
    for table_element in (e for e in toml_file_elements if t.predicates.table(e)):
        _style_table(table_element)


def _style_table(table_element):

    elements = table_element.sub_elements

    # Our iterator index
    i = float('-inf')

    def next_key():
        return t.find_following(elements, t.predicates.non_metadata, i)

    def next_assignment():
        return t.find_following(elements, t.predicates.op_assignment, next_key())

    def next_value():
        return t.find_following(elements, t.predicates.non_metadata, next_assignment())

    while next_key() >= 0:

        del elements[next_key()+1:next_assignment()]
        del elements[next_assignment()+1:next_value()]

        elements.insert(next_assignment(), element_factory.create_whitespace_element(1))
        elements.insert(next_value(), element_factory.create_whitespace_element(1))

        i = t.find_following(elements, t.predicates.newline, i)