def generate_repository(name: str):
    """Genera un repositorio completo con manejo de errores como en tu ejemplo"""
    repository_template = f"""from ..models.{name.lower()}Model import {name.capitalize()}
from typing import List, Optional
from ..schemas.{name.lower()}Schema import {name.capitalize()}In, {name.capitalize()}Out
from tortoise.exceptions import DoesNotExist, IntegrityError

class {name.capitalize()}Repository:

    async def get_all(self) -> List[{name.capitalize()}]:
        \"\"\"Obtener todos los {name.lower()}s\"\"\"
        return await {name.capitalize()}.all()

    async def get_by_id(self, id_{name.lower()}: int) -> Optional[{name.capitalize()}]:
        \"\"\"Obtener {name.lower()} por ID\"\"\"
        try:
            {name.lower()} = await {name.capitalize()}.get(id=id_{name.lower()})
            return {name.lower()}
        except DoesNotExist:
            print(f"{name.capitalize()} with id {{id_{name.lower()}}} does not exist.")
            return None
        except Exception as e:
            print(f"Error fetching {name.lower()} by id: {{e}}")
            return None

    async def store(self, {name.lower()}_data: {name.capitalize()}In) -> {name.capitalize()}Out:
        \"\"\"Crear nuevo {name.lower()}\"\"\"
        try:
            return await {name.capitalize()}.create(**{name.lower()}_data.model_dump())
        except IntegrityError as e:
            print(f"IntegrityError while creating {name.lower()}: {{e}}")
            return None
        except Exception as e:
            print(f"Unexpected error creating {name.lower()}: {{e}}")
            return None

    async def update(self, {name.lower()}: {name.capitalize()}, update_data: dict) -> {name.capitalize()}Out:
        \"\"\"Actualizar {name.lower()} existente\"\"\"
        try:
            for field, value in update_data.items():
                setattr({name.lower()}, field, value)
            await {name.lower()}.save(update_fields=list(update_data.keys()))
            return {name.lower()}
        except DoesNotExist:
            print(f"{name.capitalize()} with id {{{name.lower()}.id}} does not exist.")
            return None
        except IntegrityError as e:
            print(f"IntegrityError while updating {name.lower()}: {{e}}")
            return None
        except Exception as e:
            print(f"Unexpected error updating {name.lower()}: {{e}}")
            return None

    async def delete(self, id_{name.lower()}: int) -> bool:
        \"\"\"Eliminar {name.lower()} por ID\"\"\"
        try:
            deleted_count = await {name.capitalize()}.filter(id=id_{name.lower()}).delete()
            return deleted_count > 0
        except Exception as e:
            print(f"Error deleting {name.lower()}: {{e}}")
            return False
"""
    return repository_template
