class PlaylistLibrary:
    def __init__(self, repository):
        self.repository = repository
        self.library = self.repository.load()

    def list_all(self):
        self.library = self.repository.load()
        if not self.library:
            return ""

        key_width = 2
        name_width = 20
        tracks_width = 20

        lines = []
        for key, playlist in self.library.items():
            key_text = str(key)[:key_width].ljust(key_width)
            name_text = playlist.name[:name_width].ljust(name_width)
            tracks_text = playlist.track_list()[:tracks_width].ljust(tracks_width)

            line = (
                f"{key_text}| "
                f"{name_text} | "
                f"{tracks_text}"
            )
            lines.append(line)

        return "\n".join(lines)

    def get_playlist(self, key):
        return self.library.get(str(key))

    def get_name(self, key):
        playlist = self.get_playlist(key)
        return playlist.name if playlist else None

    def get_tracks(self, key):
        playlist = self.get_playlist(key)
        return playlist.tracks if playlist else []

    def get_path(self, key):
        playlist = self.get_playlist(key)
        return playlist.path if playlist else None
