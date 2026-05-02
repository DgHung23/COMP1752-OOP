from song import Song
from song_repository import SongRepository


class TrackLibrary:
    def __init__(self, repository):
        self._repository = repository
        self._library = self._repository.load()

    def list_all(self):
        self._library = self._repository.load()
        if not self._library:
            return ""

        key_width = 1
        name_width = 15
        artist_width = 11
        rating_width = 5
        duration_width = 5

        lines = []
        for key, song in self._library.items(): # to stadarlize text to table form
            key_text = str(key)[:key_width].ljust(key_width)
            name_text = song._name[:name_width].ljust(name_width)
            artist_text = song._artist[:artist_width].ljust(artist_width)
            rating_text = song.stars()[:rating_width].ljust(rating_width)
            duration_text = song.formatted_duration()[:duration_width].ljust(duration_width)

            line = (
                f"{key_text}| "
                f"{name_text} | "
                f"{artist_text} | "
                f"{rating_text} | "
                f"{duration_text}"
            )
            lines.append(line)

        return "\n".join(lines)

    def _normalize_key(self, key):
        key = str(key).strip()
        if key in self._library:
            return key
        if not key.isdigit():
            return None
        return str(int(key))

    def _get_song(self, key):
        key = self._normalize_key(key)
        if key is None:
            return None
        return self._library.get(key)

    def get_name(self, key):
        song = self._get_song(key)
        return song._name if song else None

    def get_artist(self, key):
        song = self._get_song(key)
        return song._artist if song else None

    def get_rating(self, key):
        song = self._get_song(key)
        return song._rating if song else -1

    def get_play_count(self, key):
        song = self._get_song(key)
        return song._play_count if song else -1

    def get_duration(self, key):
        song = self._get_song(key)
        return song._duration if song else -1
    
    def get_formatted_duration(self, key):
        song = self._get_song(key)
        return song.formatted_duration() if song else None

    def get_path(self, key):
        song = self._get_song(key)
        return song._path if song else None

    def get_image_path(self, key):
        song = self._get_song(key)
        return song._image_path if song else None

    def set_rating(self, key, rating):
        song = self._get_song(key)
        if not song:
            return
        song.set_rating(rating)
        self._repository.save(self._library)

    def set_image_path(self, key, image_path):
        song = self._get_song(key)
        if not song:
            return
        song._image_path = image_path
        self._repository.save(self._library)

    def increment_play_count(self, key):
        song = self._get_song(key)
        if not song:
            return
        song.increment_play_count()
        self._repository.save(self._library)

    def add_song(self, key, name, artist, rating=0, play_count=0, duration=0, path="", image_path=""):
        key = self._normalize_key(key)
        if key is None:
            raise ValueError("Track key must contain digits only.")
        if key in self._library:
            raise ValueError("Key đã tồn tại.")

        self._library[key] = Song(name, artist, rating, play_count, duration, path, image_path)
        self._repository.save(self._library)

    def remove_song(self, key):
        key = self._normalize_key(key)
        if key in self._library:
            del self._library[key]
            self._repository.save(self._library)
