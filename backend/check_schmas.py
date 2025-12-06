# check_schemas.py
import os
import ast

def find_missing_update_classes():
    schemas_dir = "schemas"
    for filename in os.listdir(schemas_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(schemas_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Verifica se tem classes *Update
            if "Update" in content:
                print(f"✓ {filename}: Tem classes Update")
            else:
                print(f"✗ {filename}: Faltam classes Update")
                
                # Encontra todas as classes Create para inferir Update
                tree = ast.parse(content)
                classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                create_classes = [c for c in classes if 'Create' in c]
                
                for create_class in create_classes:
                    base_class = create_class.replace('Create', '')
                    update_class = f"{base_class}Update"
                    if update_class not in classes:
                        print(f"  - Falta: {update_class}")

if __name__ == "__main__":
    find_missing_update_classes()