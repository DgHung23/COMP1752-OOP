import csv
import os
from song import Song


class SongRepository:
    def __init__(self, file_path):
        self._file_path = file_path

    def load(self):
        songs = {}

        if not os.path.exists(self._file_path):
            return songs

        with open(self._file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                key = row["id"]   # id dùng làm key của library
                song = Song.from_dict(row)
                songs[key] = song

        return songs

    def save(self, songs):
        with open(self._file_path, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["id","name","artist","rating","play_count","duration","path","image_path"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for key, song in songs.items():
                row = {"id": key}
                row.update(song.to_dict())
                writer.writerow(row)
