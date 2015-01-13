import copy
from uranium.compat import UserDict
from six import string_types


class ResolveDictExeception(Exception):
    pass


class CyclicReferenceException(ResolveDictExeception):
    pass


class ResolveDict(UserDict, object):

    def __init__(self, values, resolve_values):
        self._resolve_values = resolve_values
        super(ResolveDict, self).__init__()
        # this is assigned directly on purpose.
        # we want any modification to the dict
        # to affect the object passed.
        self.data = values

    def get_with_tree(self, key, key_tree=None):
        """
        this accepts a 'key tree' argument, which is used to find
        cyclic definitions
        """
        val = self.data[key]

        if isinstance(val, string_types):
            return render(val, self._resolve_values, key_tree)
        elif isinstance(val, dict):
            return ResolveDict(val, self._resolve_values)
        else:
            return val

    def __getitem__(self, key):
        return self.get_with_tree(key)


def render(raw_string, values, key_tree=None):
    if key_tree is None:
        key_tree = []

    output = ""
    bracket_count = 0
    parsing_variable = False
    variable_name = None

    for char in raw_string:
        if not parsing_variable:
            output += char

            if char == '{':
                bracket_count += 1

            if bracket_count == 2:
                bracket_count = 0
                parsing_variable = True
                variable_name = ""
                output = output[:-2]  # remove the {{ at the end

        else:

            variable_name += char

            if char == '}':
                bracket_count += 1

            if bracket_count == 2:
                bracket_count = 0
                parsing_variable = False
                variable_name = variable_name[:-2]  # remove the }} at the end
                value = _get_variable(variable_name,  values, key_tree)
                output += str(value)

    return output


def _get_variable(name, values, key_tree):
    key_tree = copy.copy(key_tree)

    if name in key_tree:
        raise CyclicReferenceException(
            "value for {0} references itself.".format(name))

    key_tree.append(name)

    path = name.split('.')
    for element in path:
        name, index = _parse_element(element)

        if isinstance(values, ResolveDict):
            values = values.get_with_tree(name, key_tree)
        elif isinstance(values, dict):
            values = values[name]
        else:
            raise "unable to retrieve {0} from {1}".format(
                path, values
            )

        if index is not None:
            values = values[index]

    return values


def _parse_element(element):
    name, index = "", ""

    parsing_index = False

    for char in element:
        if char == "[":
            parsing_index = True
            continue

        if char == "]":
            index = int(index)
            continue

        if not parsing_index:
            name += char
        else:
            index += char

    return name, index if index != "" else None


def get_recursive_resolvedict(values):
    """
    this will generate a recursive dict, which
    """
    r_dict = ResolveDict(values, None)
    r_dict._resolve_values = r_dict
    return r_dict
