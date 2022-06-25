import ast

def main():
    with open("lex.py", "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.stats = {}

    def visit_Assign(self, node):
        node_value = node.value
        if(isinstance(node_value, ast.Constant)):
            try:
                node_id = node.targets[0].id
                node_val = node.value.value
                self.stats[str(node_id)] = node_val
            except:
                pass
        pass


    def visit_Str(self, node):
        node_value = node.value
        print(node)
        print(node.s)
        if(isinstance(node_value, ast.Constant)):
            try:
                node_id = node.targets[0].id
                node_val = node.value.value
                self.stats[str(node_id)] = node_val
            except:
                pass
        pass

if __name__ == "__main__":
    main()

