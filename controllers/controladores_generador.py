from pymongo.errors import PyMongoError
from pymongo.collection import Collection
from typing import List, Type
from pytz import timezone
from datetime import datetime
from models.modelo_generador import GeneradorDataModel


# Crear registro
def create_generador_data(generador_data: GeneradorDataModel, collection: Collection):
    try:
        generador_data_dict = generador_data.model_dump()

        if generador_data_dict["timestamp"] is None:
            colombia_tz = timezone('America/Bogota')
            generador_data_dict["timestamp"] = datetime.now(colombia_tz)
            generador_data_dict["timestamp"] = generador_data_dict["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        generador_data_dict["_id"] = collection.count_documents({}) + 1

        result = collection.insert_one(generador_data_dict)

        return {"message": "Registro creado exitosamente", "id": str(result.inserted_id)}

    except PyMongoError as e:
        return {"error": str(e)}


# Actualizar registro por ID
def update_generador_byID(variable_id: str, updated_data: GeneradorDataModel, collection: Collection) -> dict:
    try:
        variable_id_num = int(variable_id)

        current_data = collection.find_one({"_id": variable_id_num})
        if current_data is None:
            return {"error": f"No se encontró el registro para actualizar con el ID: {variable_id}"}

        updated_data_dict = updated_data.model_dump()
        for field in updated_data_dict:
            if updated_data_dict[field] is None:
                updated_data_dict[field] = current_data[field]

        if updated_data_dict["timestamp"] is not None:
            updated_data_dict["timestamp"] = updated_data_dict["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        result = collection.update_one({"_id": variable_id_num}, {"$set": updated_data_dict})

        if result.modified_count == 1:
            return {"message": "Registro actualizado correctamente"}
        else:
            return {"error": f"No se encontró el registro para actualizar con el ID: {variable_id}"}
    except Exception as e:
        return {"error": f"Error al intentar actualizar el registro: {str(e)}"}


# Leer registro por ID
def get_generador_byID(variable_id: str, collection: Collection):
    try:
        variable_id_num = int(variable_id)

        generador_data = collection.find_one({"_id": variable_id_num})
        if generador_data:
            for key in generador_data:
                if generador_data[key] is None:
                    generador_data[key] = 0.0
            return GeneradorDataModel(**generador_data)
        else:
            return None
    except Exception as e:
        print(e)
        return None


# Leer todos los registros
def get_all_generador_data(collection: Collection) -> List[GeneradorDataModel]:
    try:
        generador_data_list = list(collection.find())
        for generador_data in generador_data_list:
            for key in generador_data:
                if generador_data[key] is None:
                    generador_data[key] = 0.0

        return [GeneradorDataModel(**generador_data) for generador_data in generador_data_list]
    except Exception as e:
        print(e)
        return []


# Leer los últimos 20 registros
def get_last_20_generador_data(collection: Collection) -> List[GeneradorDataModel]:
    try:
        generador_data_list = list(collection.find().sort([("_id", -1)]).limit(20))
        for generador_data in generador_data_list:
            for key in generador_data:
                if generador_data[key] is None:
                    generador_data[key] = 0.0

        return [GeneradorDataModel(**generador_data) for generador_data in generador_data_list]
    except Exception as e:
        print(e)
        return []


# Leer el último registro
def get_last_generador_data(collection: Collection) -> GeneradorDataModel | Type[GeneradorDataModel]:
    try:
        generador_data = collection.find().sort([("_id", -1)]).limit(1)[0]
        for key in generador_data:
            if generador_data[key] is None:
                generador_data[key] = 0.0

        return GeneradorDataModel(**generador_data)
    except Exception as e:
        print(e)
        return GeneradorDataModel


# Eliminar registro por ID
def delete_generador_byID(variable_id: str, collection: Collection) -> dict:
    try:
        variable_id_num = int(variable_id)
        result = collection.delete_one({"_id": variable_id_num})

        if result.deleted_count == 1:
            return {"message": "Registro eliminado correctamente"}
        else:
            return {"error": "No se encontró el registro para eliminar"}
    except Exception as e:
        print(e)
        return {"error": "Error al intentar eliminar el registro"}


# Eliminar todos los registros
def delete_all_generador_data(collection: Collection) -> dict:
    try:
        result = collection.delete_many({})

        return {"message": f"Se eliminaron {result.deleted_count} registros correctamente"}
    except Exception as e:
        print(e)
        return {"error": "Error al intentar eliminar los registros"}
