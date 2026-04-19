class Song:
    def __init__(self, name, artist, rating=0, play_count=0, duration=0, path=""):
        self.name = name
        self.artist = artist
        self.rating = int(rating)
        self.play_count = int(play_count)
        self.duration = int(duration)
        self.path = path

    def info(self):
        return f"{self.name} - {self.artist} {self.stars()}"

    def stars(self):
        return "*" * self.rating

    def set_rating(self, rating):
        rating = int(rating)
        if 0 <= rating <= 5:
            self.rating = rating
        else:
            raise ValueError("Rating must be between 0 and 5.")

    def increment_play_count(self):
        self.play_count += 1

    def formatted_duration(self):
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

    def to_dict(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "rating": self.rating,
            "play_count": self.play_count,
            "duration": self.duration,
            "path": self.path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            artist=data["artist"],
            rating=data.get("rating", 0),
            play_count=data.get("play_count", 0),
            duration=data.get("duration", 0),
            path=data.get("path", "")
        )