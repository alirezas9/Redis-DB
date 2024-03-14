from Cli.actions.utils.encrypt import AESCipher
import json
import redis
from datetime import datetime


client = redis.Redis(host='localhost', port=6379, db=0)

class Actions():
    CREATE = 'create'
    READ = 'read'
    UPDATE = 'update'
    LIST = 'list'
    DELETE = 'delete'
    REMAIN = 'rem'

    def __str__(self):
        return self.value.lower()
    
class Action():
    def __init__(self) -> None:
        self._cipher = AESCipher()
    
    def create(self, name, description, key, exp):
        """
        encrypt the given key
        create a Password object
        store the json format of object in redis
        print the encrypted key
        """
        if client.exists(name):
            print(f"The key '{name}' already exists.")
        else:
            encrypted_key = self._cipher.encrypt(key)

            value = {"name" : name,
                     "description": description,
                     "key": encrypted_key,
                     "exp": exp}
            password = json.dumps(value)

            client.set(name, password)
            client.expire(name, exp)

            print(encrypted_key)


    def read(self, name):
        """
        retreives the password from redis
        prints the password info
        """
        value = client.get(name)    
        if value:
            for key, value in json.loads(value).items():
                print(f"{key}: {value}")
        else :
            print(f"The key '{name}' does not exist.")
    
    def update(self, name, new_key):
        """
        encrypts new key
        saves the password with updated attributes
        prints new value for encrypted key
        """
        
        if client.exists(name):
            key = self._cipher.encrypt(new_key)
            client.set(name, key)
            print(f"The key '{name}' has been successfully updated.")
            print(f"updated key {key}")
        else : 
            print(f"The key '{name}' does not exist.")


    def delete(self, name):
        """
        deletes the password from redis
        prints a success message
        """
        if client.exists(name):
            client.delete(name)
            if not client.exists(name):
                print(f"The key '{name}' has been successfully deleted.")
            else:
                print(f"Failed to delete the key '{name}'.")
        else:
            print(f"The key '{name}' does not exist.")
            
        

    def list(self):
        """
        gets all the saved passwords from redis
        prints each password info
        """
        keys = client.keys()
        values = client.mget(keys)
        
        if not values:
            print("No passwords found.")
        else :    
            print("List of all key and values ")
            print("=======================================")
            for value in values:
                for key, val in json.loads(value).items():
                    print(f"{key}: {val}")
                print("=======================================")


    def get_remaining_time(self, name):
        """
        retreives the remaining time of password existance on redis
        prints the remaining time
        """
        print(client.ttl(name))
