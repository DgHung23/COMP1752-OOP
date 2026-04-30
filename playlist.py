class Playlist:
    def __init__(self, name, tracks=None, path=""):
        self.name = name
        self.tracks = self._parse_tracks(tracks)
        self.path = path

    def _parse_tracks(self, tracks):
        if tracks is None:
            return []
        if isinstance(tracks, str):
            return [track.strip() for track in tracks.split("|") if track.strip()]
        return [str(track).strip() for track in tracks if str(track).strip()]

    def track_list(self):
        return "|".join(self.tracks)

    def to_dict(self):
        return {
            "name": self.name,
            "tracks": self.track_list(),
            "path": self.path
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            tracks=data.get("tracks", ""),
            path=data.get("path", "")
        )
