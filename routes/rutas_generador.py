from fastapi import APIRouter, HTTPException
from typing import List
from models.modelo_generador import GeneradorDataModel
from controllers.controladores_generador import (create_generador_data, get_generador_byID, get_all_generador_data,
                                                         delete_generador_byID, update_generador_byID,
                                                         delete_all_generador_data, get_last_20_generador_data,
                                                         get_last_generador_data)


def get_router(variables_collection):
    router = APIRouter()

    # Crear registro
    @router.post("/generador", response_model=dict)
    def create_data(sensor_data: GeneradorDataModel):
        result = create_generador_data(sensor_data, variables_collection)
        if "error" in result:
            raise HTTPException(status_code=500, detail="Error interno del servidor")
        return result

    # Actualizar registro por ID
    @router.put("/generador/{sensor_id}", response_model=dict)
    def update_sensor(sensor_id: str, updated_data: GeneradorDataModel):
        result = update_generador_byID(sensor_id, updated_data, variables_collection)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    # Leer registro por ID
    @router.get("/generador/{sensor_id}", response_model=GeneradorDataModel)
    def read_sensor_byID(sensor_id: str):
        sensor_data = get_generador_byID(sensor_id, variables_collection)
        if sensor_data:
            return sensor_data
        else:
            raise HTTPException(status_code=404, detail="Variable no encontrada")

    # Leer todos los registros
    @router.get("/generador", response_model=List[GeneradorDataModel])
    def read_all_sensor_data():
        sensor_data_list = get_all_generador_data(variables_collection)
        if sensor_data_list:
            return sensor_data_list
        else:
            raise HTTPException(status_code=404, detail="No se encontraron registros de las variables")

    # Leer los últimos 20 registros
    @router.get("/generador/get/last20", response_model=List[GeneradorDataModel])
    def read_last_20_sensor_data():
        sensor_data_list = get_last_20_generador_data(variables_collection)
        if sensor_data_list:
            return sensor_data_list
        else:
            return []

    # Leer el último registro
    @router.get("/generador/get/last", response_model=GeneradorDataModel)
    def read_last_sensor_data():
        sensor_data = get_last_generador_data(variables_collection)
        if sensor_data:
            return sensor_data
        else:
            raise HTTPException(status_code=404, detail="No se encontraron registros de las variables")

    # Eliminar registro por ID
    @router.delete("/generador/{sensor_id}", response_model=dict)
    def delete_sensor(sensor_id: str):
        result = delete_generador_byID(sensor_id, variables_collection)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    # Eliminar todos los registros
    @router.delete("/generador", response_model=dict)
    def delete_all_sensors():
        result = delete_all_generador_data(variables_collection)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    return router
