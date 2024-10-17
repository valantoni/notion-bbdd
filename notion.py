import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

class NotionDatabase:
    def __init__(self, token, database_id):
        self.token = token
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.base_url = "https://api.notion.com/v1"

    def write(self, tarea, date, status):
        """Crea una nueva página en la base de datos de Notion      
        
        Args:
            title (str): Título de la página
            description (str): Descripción de la página
            date (str): Fecha en formato ISO 8601 (e.g., "2023-09-19T19:54:01Z")
            status (str): Estado de la página (debe coincidir con uno de los estados definidos en Notion)
        
        Referencia:
            https://developers.notion.com/reference/post-page
        """
        url = f"{self.base_url}/pages"
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "tarea": {
                    "title": [
                        {
                            "text": {
                                "content": tarea
                            }
                        }
                    ]
                },
                "fecha": {
                    "date": {
                        "start": date,
                        "end": None
                    }
                },
                "Status": {
                    "status": {
                        "name": status
                    }
                }
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        if response.status_code in [200, 201]:
            print("Página creada exitosamente")
        else:
            print(f"Error al crear página: {response.status_code}, {response.text}")

    def read(self, filter_conditions=None, sorts=None):
        """
        Lee la base de datos de Notion con opciones de filtrado y ordenamiento.
        Devuelve la respuesta JSON de la consulta.
        Args:
            filter_conditions (dict, optional): Condiciones de filtrado según la API de Notion.
            sorts (list, optional): Lista de criterios de ordenamiento.
            filter example: filter_conditions = {
        "property": "Status",
        "status": {
            "equals": "Not started"
            }
        }
        sorts = [{"property": "Date", "direction": "ascending"}]
        Returns:
            dict: Respuesta JSON de la consulta o None en caso de error.
        """
        url = f"{self.base_url}/databases/{self.database_id}/query"
        data = {}
        if filter_conditions:
            data["filter"] = filter_conditions
        if sorts:
            data["sorts"] = sorts
        response = requests.post(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            #obtener todos los ids y guardarlos en un array
            ids = []
            for i in response.json()["results"]:
                ids.append(i["id"])
            return response.json(), response.json()["results"][0]["id"] 
        else:
            print(f"Error al leer la base de datos: {response.status_code}, {response.text}")
            return None

    def update(self, page_id, tarea=None, status=None, date=None):
        """
        Actualiza las propiedades de una página existente en la base de datos de Notion.

        Args:
            page_id (str): ID de la página a actualizar.
            title (str, optional): Nuevo título de la página.
            description (str, optional): Nueva descripción de la página.
            status (str, optional): Nuevo estado de la página.
            date (str, optional): Nueva fecha en formato ISO 8601.
        """
        url = f"{self.base_url}/pages/{page_id}"
        properties = {}
        
        if tarea:
            properties["tarea"] = {
                "title": [
                    {
                        "text": {
                            "content": tarea
                        }
                    }
                ]
            }
        if status:
            properties["Status"] = {
                "status": {
                    "name": status
                }
            }
        if date:
            properties["fecha"] = {
                "date": {
                    "start": date,
                    "end": None
                }
            }
        data = {"properties": properties}
        response = requests.patch(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Página actualizada exitosamente")
        else:
            print(f"Error al actualizar página: {response.status_code}, {response.text}")


    def delete(self, page_id):
        """
        Archiva (elimina) una página en la base de datos de Notion.

        Args:
            page_id (str): ID de la página a archivar.
        """
        url = f"{self.base_url}/pages/{page_id}"
        data = {"archived": True}
        response = requests.patch(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            print("Página eliminada exitosamente")
        else:
            print(f"Error al eliminar página: {response.status_code}, {response.text}")

# Ejemplo de uso
if __name__ == "__main__":
    load_dotenv()
    
    NOTION_TOKEN = os.getenv('notion_token')
    DATABASE_ID = os.getenv('table_id')
 
    notion = NotionDatabase(NOTION_TOKEN, DATABASE_ID)
    
    #acceder al id de la primera tarea
    response, id = notion.read()

    notion.delete(id)

   
