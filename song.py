class Song:
    def __init__(self, name, artist, rating=0, play_count=0, duration=0, path="", image_path=""):
        self._name = name
        self._artist = artist
        self._rating = int(rating)
        self._play_count = int(play_count)
        self._duration = int(duration)
        self._path = path
        self._image_path = image_path

    def info(self):
        return f"{self._name} - {self._artist} {self.stars()}"

    def stars(self):
        return "*" * self._rating

    def set_rating(self, rating):
        rating = int(rating)
        if 0 <= rating <= 5:
            self._rating = rating
        else:
            raise ValueError("Rating must be between 0 and 5.")

    def increment_play_count(self):
        self._play_count += 1

    def formatted_duration(self):
        minutes = self._duration // 60
        seconds = self._duration % 60
        return f"{minutes}:{seconds:02d}"

    def to_dict(self):
        return {
            "name": self._name,
            "artist": self._artist,
            "rating": self._rating,
            "play_count": self._play_count,
            "duration": self._duration,
            "path": self._path,
            "image_path": self._image_path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            artist=data["artist"],
            rating=data.get("rating", 0),
            play_count=data.get("play_count", 0),
            duration=data.get("duration", 0),
            path=data.get("path", ""),
            image_path=data.get("image_path", "")
        )
