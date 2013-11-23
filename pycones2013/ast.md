# Haciendo código que analiza código con AST

## Ejemplo mínimo

import ast

code = """
def add(x, y):
    return x + y
"""

tree = ast.parse(code)

`ast.fix_missing_locations` si modificamos el árbol

## Visitor

class Visitor(ast.NodeVisitor):
    def visit(self, node):
        print(node)

v = Visitor()
v.visit(tree)

- Visitor no muta el AST
- Para realizar transformaciones usamos `ast.NodeTransformer`

## Utilidades

- Análisis estático
- Generación de pruebas
- Conversión de código (AST como representación intermedia)
