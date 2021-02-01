import os
import json
import requests

DATABASE_LINK_NAME="Databases.json"

def update(path):
    if not os.path.exists(path) :
        os.makedirs(path)
    link_path = os.path.join(path,DATABASE_LINK_NAME)
    request = requests.get('http://164.132.96.221/databases/'+DATABASE_LINK_NAME)
    if request.status_code == 200 :
        database_list = request.json()
        with open(link_path, 'w') as linkfile:
            json.dump(database_list, linkfile, indent=4)
        for database in database_list :
            if database["Name"]:
                new_req = requests.get('http://164.132.96.221/databases/'+database["Name"])
                if new_req.status_code == 200 :
                    database_path = os.path.join(path,database["Name"])
                    with open(database_path, 'w') as databasefile:
                        json.dump(new_req.json(), databasefile)


if __name__ == "__main__":
    update("./databases/")
