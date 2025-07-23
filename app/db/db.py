import os
from tortoise import Tortoise
from dotenv import load_dotenv

load_dotenv()
import importlib



host = os.getenv("DB_HOST", "localhost")
port = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USER", "user")
password = os.getenv("MYSQL_PASSWORD", "password")
db_name = os.getenv("MYSQL_DATABASE", "mydb")



async def init_db():
    base_path = "app/modules"
    base_package = "app.modules"
    models_list = []

    
    for module_name in os.listdir(base_path):
        module_path = os.path.join(base_path, module_name, "models")

 
        if os.path.isdir(module_path):
            for file in os.listdir(module_path):
                if file.endswith(".py") and file != "__init__.py":
                    model_module = f"{base_package}.{module_name}.models.{file[:-3]}"
                    models_list.append(model_module)

                    try:
                       
                        importlib.import_module(model_module)
                    except ModuleNotFoundError as e:
                        print(f"⚠️ No se pudo importar {model_module}: {e}")

    # print(models_list)
    # Configurar TortoiseORM con los modelos encontrados
    await Tortoise.init(
        db_url=f"mysql://{user}:{password}@{host}/{db_name}",
        modules={"models": models_list}
    )
    await Tortoise.generate_schemas()
