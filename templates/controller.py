
def generate_controller(name: str):
    """Genera un controller completo con CRUD similar a tu ejemplo"""
    controller_template = f"""from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from injector import Injector
from ..services.{name.lower()}Service import {name.capitalize()}Service
from ..schemas.{name.lower()}Schema import {name.capitalize()}Schema, {name.capitalize()}Out, {name.capitalize()}In, {name.capitalize()}Update
from ..module import {name.capitalize()}Module

router = APIRouter()

injector = Injector([{name.capitalize()}Module()])

def get_service() -> {name.capitalize()}Service:
    return injector.get({name.capitalize()}Service)


@router.get("/", response_model=List[{name.capitalize()}Out])
async def get_all_{name.lower()}s(service: {name.capitalize()}Service = Depends(get_service)):
    \"\"\"Obtener todos los {name.lower()}s\"\"\"
    return await service.get_all()


@router.get("/{{id}}", response_model={name.capitalize()}Out)
async def get_{name.lower()}_by_id(id: int, service: {name.capitalize()}Service = Depends(get_service)):
    \"\"\"Obtener un {name.lower()} por ID\"\"\"
    {name.lower()} = await service.get_by_id(id)
    if not {name.lower()}:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="{name.capitalize()} no encontrado")
    return {name.lower()}


@router.post("/", response_model={name.capitalize()}Out, status_code=status.HTTP_201_CREATED)
async def create_{name.lower()}(data: {name.capitalize()}In, service: {name.capitalize()}Service = Depends(get_service)):
    \"\"\"Crear un nuevo {name.lower()}\"\"\"
    {name.lower()} = await service.store(data)
    if not {name.lower()}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Error al crear el {name.lower()}")
    return {name.lower()}


@router.put("/{{id}}", response_model={name.capitalize()}Out)
async def update_{name.lower()}(id: int, data: {name.capitalize()}Update, service: {name.capitalize()}Service = Depends(get_service)):
    \"\"\"Actualizar un {name.lower()} existente\"\"\"
    {name.lower()} = await service.update(id, data)
    if not {name.lower()}:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="{name.capitalize()} no encontrado o error al actualizar")
    return {name.lower()}


@router.delete("/{{id}}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{name.lower()}(id: int, service: {name.capitalize()}Service = Depends(get_service)):
    \"\"\"Eliminar un {name.lower()}\"\"\"
    success = await service.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="{name.capitalize()} no encontrado")
"""
    return controller_template
