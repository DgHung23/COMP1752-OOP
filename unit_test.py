# ===================Test cases for the TrackLibrary class using pytest===================
# ================================to run, execute: py -m pytest ==========================
import pytest

from song import Song
from track_library import TrackLibrary


class FakeSongRepository:
    # Create a fake repository so tests do not read from or write to the real CSV file.
    def __init__(self, songs):
        self._songs = songs
        self.save_count = 0
        self.saved_songs = None

    # Simulate loading song data from the repository.
    def load(self):
        return dict(self._songs)

    # Simulate saving song data and count how many times save is called.
    def save(self, songs):
        self.save_count += 1
        self.saved_songs = dict(songs)


# Create a TrackLibrary with sample data shared by the tests.
def make_library():
    repository = FakeSongRepository(
        {
            "1": Song("The Nights", "Avicii", rating=5, play_count=99, duration=220),
            "4": Song("Mockingbird", "Eminem", rating=2, play_count=15, duration=253),
        }
    )

    return TrackLibrary(repository), repository


# Check that song details can be returned using a valid key.
def test_get_song_with_valid_key_returns_song_details():
    library, _ = make_library()

    assert library.get_name("1") == "The Nights"
    assert library.get_artist("1") == "Avicii"
    assert library.get_rating("1") == 5


# Check that a zero-padded key like "04" is accepted as key "4".
def test_zero_padded_key_is_accepted():
    library, _ = make_library()

    assert library.get_name("04") == "Mockingbird"
    assert library.get_duration("04") == 253


# Check that a text key like "four" does not crash the program.
def test_text_key_returns_default_values():
    library, _ = make_library()

    assert library.get_name("four") is None
    assert library.get_rating("four") == -1
    assert library.get_formatted_duration("four") is None


# Check that a new song cannot be added when the key is not numeric.
def test_add_song_with_text_key_raises_value_error():
    library, repository = make_library()

    with pytest.raises(ValueError, match="digits"):
        library.add_song("four", "New Song", "New Artist")

    assert repository.save_count == 0
    assert library.get_name("four") is None


# Check that a text rating like "four" is rejected and not saved.
def test_set_rating_with_text_value_raises_value_error():
    library, repository = make_library()

    with pytest.raises(ValueError):
        library.set_rating("1", "four")

    assert library.get_rating("1") == 5
    assert repository.save_count == 0


# Check that a duplicate key cannot be used when adding a new song.
def test_add_song_with_duplicate_key_raises_value_error():
    library, repository = make_library()

    with pytest.raises(ValueError):
        library.add_song("1", "Duplicate Song", "Duplicate Artist")

    assert library.get_name("1") == "The Nights"
    assert repository.save_count == 0


# Check that a valid rating update changes the rating and saves the library.
def test_set_rating_with_valid_value_updates_and_saves():
    library, repository = make_library()

    library.set_rating("1", 3)

    assert library.get_rating("1") == 3
    assert repository.save_count == 1


# Check that a rating above 5 is rejected and does not save the library.
def test_set_rating_above_five_raises_value_error():
    library, repository = make_library()

    with pytest.raises(ValueError, match="between 0 and 5"):
        library.set_rating("1", 6)

    assert library.get_rating("1") == 5
    assert repository.save_count == 0


# Check that incrementing play count increases the value and saves the library.
def test_increment_play_count_updates_and_saves():
    library, repository = make_library()

    library.increment_play_count("1")

    assert library.get_play_count("1") == 100
    assert repository.save_count == 1


# Check that removing an existing song deletes it and saves the library.
def test_remove_existing_song_deletes_and_saves():
    library, repository = make_library()

    library.remove_song("4")

    assert library.get_name("4") is None
    assert repository.save_count == 1
