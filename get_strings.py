import ast
import json
import traceback
import types
import re
import argparse

try:
    # Python 2.6
    StringTypes = (types.StringType, types.UnicodeType)
except AttributeError:
    # Python 3.0
    StringTypes = (str, bytes)

RegexType = type(re.compile('string'))
FStringType = type(f"fstring")

class Ancestor(ast.NodeTransformer):
    parent = None
    # this lets us walk back up the tree to find the parent nodes
    # it will let us compare to see the type of node it is, and 
    # see if the constant is a resultant of a statement, expression or variable

    def visit(self, node):
        node.parent = self.parent
        self.parent = node
        node = super().visit(node)
        if isinstance(node, ast.AST):
            self.parent = node.parent
        return node


class Constants(Ancestor):
    all_variables = []
    filename = None

    def visit_Constant(self, node):
        self.generic_visit(node)
        print_visits = True
        
        if isinstance(node.value, str):
            # We have found a constant string

            # first case is when its just a 
            # straight literal with no assignment

            if isinstance(node.parent, ast.Assign):
                targets = node.parent.targets[0].__dict__
                values = node.parent.value.__dict__

                try:
                    variable_id = targets.get('id')
                    variable_value = values.get('value')
                    variable_location = values.get('lineno')

                    if isinstance(variable_value, (str, RegexType, FStringType)):
                        item = {
                            "id": variable_id,
                            "value": variable_value,
                            "lineno": variable_location,
                            "filename": self.filename
                        }

                        self.all_variables.append(item)
                except:
                    traceback.print_exc()
                    pass

            else:
                item = {
                    "id": "plain_assignment",
                    "value": node.value,
                    "lineno": node.__dict__.get('lineno'),
                    "filename": self.filename

                }
                self.all_variables.append(item)

    def report(self):
        return self.all_variables

    def get_strings(self):
        with open(self.filename, "r") as source:
            nodes = ast.parse(source.read())
            self.visit(nodes)
            return self.report()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--file", help="file to parse")
    parser.add_argument('dump', help="dump to std out")
    args = parser.parse_args()

    source_file = "parse.py"
    if args.file:
        source_file = args.file

    with open(source_file, "r") as source:
        nodes = ast.parse(source.read())
        constants = Constants()
        constants.filename = source_file
        constants.visit(nodes)
        if args.dump:
            print(json.dumps(constants.report()))


if __name__ == '__main__':
    main()
