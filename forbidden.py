import ast
import json
import traceback
import types
import re

try:
    # Python 2.6
    StringTypes = (types.StringType, types.UnicodeType)
except AttributeError:
    # Python 3.0
    StringTypes = (str, bytes)

RegexType = type(re.compile('string'))

def main():
    with open("lex2.py", "r") as source:
        nodes = ast.parse(source.read())
        transformer = CustomNodeTransformer()
        transformer.visit(nodes)

class CustomNodeTransformer(ast.NodeTransformer):
    variable_id = ""
    variable_value = ""
    all_variables = {}
    variable = () 

    def visit_Assign(self, node):
        targets = node.targets[0].__dict__
        #print(targets)
        values = node.value.__dict__
        #print(values)

        try:
            variable_id = targets['id']
            #print(variable_id)
            variable_value = values['value']
            #print(variable_value)
            variable_location = values['lineno']
            #print(variable_location)

            if isinstance(variable_value, (str, RegexType)):
                variable = (variable_id, variable_value, variable_location)
                self.all_variables[variable_id] = (variable_value, variable_location)
                print("\n")
                print(variable) 
            variable = ()
        except:
            traceback.print_exc()
            pass

        return node

    def visit_Constant(self, node):
        if(isinstance(node.value, str)):
            print(f"\nplain string: {node.value}, lineno: {node.lineno}" )


    def visit_args(self, node):
        tmp = node.args
        print("from visit args")
        print(tmp)

    def visit_FunctionDef(self, node):
        try:
            function_args = node.args.__dict__
            function_arguments = function_args['args'][0].arg
            function_string_values = ""
            try:
                function_string_values =  function_args['defaults'][0].value
            except IndexError:
                pass

            if function_arguments and function_string_values:
                print(f"\nfunction def args = {arguments}, values = {function_string_values}")

        except:
            traceback.print_exc()
            pass

if __name__ == '__main__':
    main()
