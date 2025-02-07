from os import path
from configparser import ConfigParser
from pyrogram import Client
from shazamio import Shazam, serialize_track, serialize_artist

shazam = Shazam()


class bot(Client):
    def __init__(self, name):
        config_file = f"{name}.ini"
        config = ConfigParser()
        config.read(config_file)
        name = name.lower()
        plugins = {'root': path.join(__package__, 'plugins')}
        api_id = config.get('pyrogram', 'api_id')
        api_hash = config.get('pyrogram', 'api_hash')
        super().__init__(
            name,
            api_id=api_id,
            api_hash=api_hash,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
        )

    async def start(self):
        await super().start()
        print("bot started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("bot stopped. Bye.")

    async def recognize(self):
        return await shazam.recognize_song(path)

    async def related(self, track_id):
        try:
            return (await shazam.related_tracks(track_id=track_id, limit=50, start_from=2))['tracks']
        except exceptions.FailedDecodeJson:
            return None
    
    async def get_artist(self, query: str):
        artists = await shazam.search_artist(query=query, limit=50)
        hits = []
        for artist in artists['artists']['hits']:
            serialized = serialize_artist(data=artist)
            print(serialized)
        
    async def get_artist_tracks(self, artist_id: int):
        tracks = []
        artist_id = 41663839
        tem = await shazam.artist_top_tracks(artist_id=artist_id, limit=50)['tracks']
        for track in tem['tracks']:
            serialized_track = serialize_track(data=track)
            print(serialized_track)
