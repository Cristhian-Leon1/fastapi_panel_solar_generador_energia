from pymongo import MongoClient
from pymongo.server_api import ServerApi


def establecer_conexion():
    try:
        uri = ("mongodb+srv://vergarakevin857:melocaramelo@cluster0.dhljdl3.mongodb.net/?retryWrites=true&w=majority"
               "&appName=Cluster0")
        client = MongoClient(uri, server_api=ServerApi('1'))

        # Acceder a la base de datos específica
        db = client.Generador
        variables_collection = db.Variables
        client.admin.command('ping')
        print("Ping completado. Conexión establecida correctamente a MongoDB!")
        return variables_collection
    except Exception as e:
        print(e)

