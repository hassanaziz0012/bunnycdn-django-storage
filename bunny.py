from django.core.files import File
from django.core.files.storage import Storage
from products.utils.Exceptions import BunnyStorageException
import requests


class BunnyStorage(Storage):
    """
    Implementation of Django's storage module using Bunny.net. 
    """

    def __init__(self, LIBRARY_ID: str = "LIBRARY ID GOES HERE", API_KEY: str = "API KEY GOES HERE"):
        self.LIBRARY_ID = LIBRARY_ID
        self.API_KEY = API_KEY
        
        self.headers = {
            'AccessKey': self.API_KEY
        }
    def _full_path(self, name):
        if name == '/':
            name = ''
        return (f"https://video.bunnycdn.com/play/{self.LIBRARY_ID}/" + str(name)).replace('\\', '/')
    
    def _save(self, name, content):
        url = f"http://video.bunnycdn.com/library/{self.LIBRARY_ID}/videos"

        payload = {"title": f'{name}'}
        headers = {
            "Content-Type": "application/*+json",
            "AccessKey": self.API_KEY
        }

        response = requests.request("POST", url, json=payload, headers=headers)

        video_id = response.json()['guid']
        
        url = f"http://video.bunnycdn.com/library/{self.LIBRARY_ID}/videos/{video_id}"

        response = requests.request("PUT", url, data=content, headers=headers)

        return video_id


    def _open(self, name, mode='rb'):
        resp = requests.get(self.base_url + name, headers=self.headers)

        if resp.status_code == 404:
            raise ValueError('File not found.')

        return File(resp.content)

    def delete(self, name):
        url = f"http://video.bunnycdn.com/library/{self.LIBRARY_ID}/videos/{name}"
        headers = {"AccessKey": self.API_KEY}

        response = requests.request("DELETE", url, headers=headers)

        return name

    def exists(self, name):
        # BunnyCDN does not care about duplicate file names. Also, we are using Video IDs to interact with videos. 
        # So, for naming the file, we don't care if the file exists or not.
        return False

    def get_thumbnail(self, video_id):
        url = f"http://video.bunnycdn.com/library/{self.LIBRARY_ID}/videos/{video_id}"

        response = requests.request("GET", url, headers=self.headers)
        
        if response.status_code != 200:
            raise BunnyStorageException(f'An error occurred in getting the thumbnail of the requested video!')

        return response.json()['thumbnailFileName']
    
    def url(self, name):
        return self._full_path(f'{name}')
