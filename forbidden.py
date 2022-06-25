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
            variable_id = targets.get('id')
            #print(variable_id)
            variable_value = values.get('value')
            #print(variable_value)
            variable_location = values.get('lineno')
            #print(variable_location)

            if isinstance(variable_value, (str, RegexType)):
                variable = (variable_id, variable_value, variable_location)
                self.all_variables[variable_id] = (variable_value, variable_location)
            variable = ()
        except:
            traceback.print_exc()
            pass

        return node

    def visit_Constant(self, node):
        if(isinstance(node.value, str)):
            # print(f"\nplain string: {node.value}, lineno: {node.lineno}" )
            self.all_variables["barestring"] = (node.value)
            print("\n")


    def visit_FunctionDef(self, node):

        num_of_arguments = len(node.args.__dict__.get('args'))

        for i in range(0, num_of_arguments):
            try:
                function_args = node.args.__dict__.get('args')
                function_variable_id = function_args[i].arg

                strings_assigned_in_function = node.args.__dict__.get('defaults')
                if strings_assigned_in_function[i] is not None:
                    function_string_value = strings_assigned_in_function[i].value


                if function_variable_id and function_string_value:
                    self.all_variables[function_variable_id] = (function_variable_id, function_string_value)

            except:
                traceback.print_exc()
                pass


    def report(self):
        print(json.dumps(self.all_variables))

def main():
    with open("parse.py", "r") as source:
        nodes = ast.parse(source.read())
        transformer = CustomNodeTransformer()
        transformer.visit(nodes)
        transformer.report()


if __name__ == '__main__':
    main()
