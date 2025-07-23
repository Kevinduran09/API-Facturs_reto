import typer
import os
from injector import Module, provider, singleton, Injector
from fastapi import Depends, APIRouter
from tortoise import Tortoise, fields
from tortoise.models import Model
from pydantic import BaseModel

from templates.controller import generate_controller
from templates.repository import generate_repository
from templates.service import generate_service
app = typer.Typer()

BASE_DIR = "app/modules"
MAIN_FILE = "app/main.py"


def create_file(path: str, content: str):
    """Crea un archivo con el contenido especificado."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def update_main_file(name: str):
    """Añade automáticamente la nueva ruta al archivo main.py si no existe."""
    import_statement = f"from app.modules.{name}.controllers.{name}Controller import router as {name}_router"
    include_statement = f"app.include_router({name}_router, prefix='/{name}', tags=['{name}'])"

    if os.path.exists(MAIN_FILE):
        with open(MAIN_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        if import_statement not in content:
            content = f"{import_statement}\n" + content

        if include_statement not in content:
            content += f"\n{include_statement}\n"

        with open(MAIN_FILE, "w", encoding="utf-8") as f:
            f.write(content)
    else:
        typer.echo(
            "Archivo main.py no encontrado. Asegúrate de tener un archivo principal para FastAPI.")


def generate_feature(name: str):
    """Genera la estructura de archivos para una nueva feature con inyección de dependencias y Tortoise ORM."""
    feature_path = os.path.join(BASE_DIR, name)
    subdirs = ["controllers", "services",
               "repositories", "schemas", "models", "tests"]

    for subdir in subdirs:
        os.makedirs(os.path.join(feature_path, subdir), exist_ok=True)

    # __init__.py en cada subdirectorio
    for subdir in subdirs:
        create_file(os.path.join(feature_path, subdir, "__init__.py"), "")

    # models.py
    create_file(os.path.join(feature_path, "models", f"{name}Model.py"), f"""
from tortoise.models import Model
from tortoise import fields

class {name.capitalize()}(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    """)

    # repository.py
    repository_content = generate_repository(name)
    create_file(os.path.join(feature_path, "repositories",
                f"{name}Repository.py"), repository_content)
    # service.py
    service_content = generate_service(name)
    create_file(os.path.join(feature_path, "services", f"{name}Service.py"), service_content)
    # schemas.py
    create_file(os.path.join(feature_path, "schemas", f"{name}Schema.py"), f"""
from pydantic import BaseModel

class {name.capitalize()}Schema(BaseModel):
    name: str
    
class {name.capitalize()}Out({name.capitalize()}Schema):
    id: int
    
class {name.capitalize()}In({name.capitalize()}Schema):
    pass
    
class {name.capitalize()}Update({name.capitalize()}Schema):
    pass
    """)

    # module.py (para la inyección de dependencias con Injector)
    create_file(os.path.join(feature_path, "module.py"), f"""
from injector import Module, provider, singleton
from .repositories.{name}Repository import {name.capitalize()}Repository
from .services.{name}Service import {name.capitalize()}Service

class {name.capitalize()}Module(Module):
    @singleton
    @provider
    def provide_repository(self) -> {name.capitalize()}Repository:
        return {name.capitalize()}Repository()

    @singleton
    @provider
    def provide_service(self, repository: {name.capitalize()}Repository) -> {name.capitalize()}Service:
        return {name.capitalize()}Service(repository)
    """)

    # routes.py
    controller_content = generate_controller(name)
    create_file(os.path.join(feature_path, "controllers",
                f"{name}Controller.py"), controller_content)

    # tests/test_feature.py
    create_file(os.path.join(feature_path, "tests", f"test_{name}.py"), f"""
import pytest

@pytest.mark.asyncio
def test_dummy():
    assert 1 + 1 == 2
    """)

    # Actualizar main.py para registrar la nueva ruta
    update_main_file(name)

    typer.echo(f"Feature '{name}' generada con éxito en {feature_path} 🚀")


@app.command()
def feature(name: str):
    """Genera una nueva feature con estructura Clean Code, Tortoise ORM e inyección de dependencias."""
    generate_feature(name)


if __name__ == "__main__":
    app()
