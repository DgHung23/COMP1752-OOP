import csv
import os
from playlist import Playlist


class PlaylistRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        playlists = {}

        if not os.path.exists(self.file_path):
            return playlists

        with open(self.file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                key = row["id"]
                playlist = Playlist.from_dict(row)
                playlists[key] = playlist

        return playlists

    def save(self, playlists):
        with open(self.file_path, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "name", "tracks", "path"]

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for key, playlist in playlists.items():
                row = {"id": key}
                row.update(playlist.to_dict())
                writer.writerow(row)
