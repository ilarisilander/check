import json

class JsonFile:
    
    def read(file_path: str) -> dict:
        """ Read a json file and return the data as a dict

        :param file_path: str
            Path to the json file
        :return: dict
            The json data in dict format 
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write(file_path: str, new_data: dict) -> None:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, indent=4)
    