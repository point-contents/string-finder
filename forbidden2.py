import ast

def main():
    with open("parse.py", "r") as source:
        extract_all(source)


def extract_all(source):
    root = ast.parse(source.read())

    for node in ast.walk(root):
        if isinstance(node, ast.Assign):
            found_node = ()
            for assign_nodes in ast.walk(node):
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    print(node.id)
                elif(isinstance(node, ast.Constant) and isinstance(node.value.s, str)):
                    print(f"Value of : {node.value}")
        



if __name__ == '__main__':
    main()
