from song import Song
from song_repository import SongRepository


class TrackLibrary:
    def __init__(self, repository):
        self.repository = repository
        self.library = self.repository.load()

    def list_all(self):
        output = ""
        for key, song in self.library.items():
            output += f"{key} {song.info()} ({song.formatted_duration()})\n"
        return output.strip()

    def get_song(self, key):
        return self.library.get(str(key))

    def get_name(self, key):
        song = self.get_song(key)
        return song.name if song else None

    def get_artist(self, key):
        song = self.get_song(key)
        return song.artist if song else None

    def get_rating(self, key):
        song = self.get_song(key)
        return song.rating if song else -1

    def get_play_count(self, key):
        song = self.get_song(key)
        return song.play_count if song else -1

    def get_duration(self, key):
        song = self.get_song(key)
        return song.duration if song else -1
    
    def get_formatted_duration(self, key):
        song = self.get_song(key)
        return song.formatted_duration() if song else None

    def get_path(self, key):
        song = self.get_song(key)
        return song.path if song else None

    def set_rating(self, key, rating):
        song = self.get_song(key)
        if not song:
            return
        song.set_rating(rating)
        self.repository.save(self.library)

    def increment_play_count(self, key):
        song = self.get_song(key)
        if not song:
            return
        song.increment_play_count()
        self.repository.save(self.library)

    def add_song(self, key, name, artist, rating=0, play_count=0, duration=0, path=""):
        key = str(key)
        if key in self.library:
            raise ValueError("Key đã tồn tại.")

        self.library[key] = Song(name, artist, rating, play_count, duration, path)
        self.repository.save(self.library)

    def remove_song(self, key):
        key = str(key)
        if key in self.library:
            del self.library[key]
            self.repository.save(self.library)