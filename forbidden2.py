import ast

def main():
    with open("parse.py", "r") as source:
        extract_all(source)


def extract_all(source):
    root = ast.parse(source.read())

    for node in ast.walk(root):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            print(node.id)
        
        if(isinstance(node, ast.Constant) and isinstance(node.value, str)):
            print(f"Value of : {node.value}")



if __name__ == '__main__':
    main()
