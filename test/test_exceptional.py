import pytest
from test.TestUtils import TestUtils
from music_playlist_management_system import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_input_validation(test_obj):
    """Test input validation and error handling"""
    try:
        # Test song record creation with invalid inputs
        with pytest.raises(ValueError):
            create_song_record("", "Title", "Artist", "rock", 180, 2000, "Album")  # Empty ID
        
        with pytest.raises(ValueError):
            create_song_record("S001", "", "Artist", "rock", 180, 2000, "Album")  # Empty title
            
        with pytest.raises(ValueError):
            create_song_record("S001", "Title", "Artist", "rock", -1, 2000, "Album")  # Negative duration
            
        # Test invalid filter parameters
        songs, _, _ = initialize_data()
        
        with pytest.raises(ValueError):
            filter_by_genre(songs, "")  # Empty genre
            
        with pytest.raises(ValueError):
            filter_by_artist(songs, "")  # Empty artist
            
        with pytest.raises(ValueError):
            filter_by_duration(songs, -1, 100)  # Negative duration
            
        with pytest.raises(ValueError):
            filter_by_duration(songs, 200, 100)  # Min > Max duration
            
        # Test invalid playlist creation
        with pytest.raises(ValueError):
            create_playlist("", ["S001"], songs)  # Empty name
            
        with pytest.raises(ValueError):
            create_playlist("Playlist", ["INVALID_ID"], songs)  # Invalid song ID
            
        # Test named tuple conversion with invalid data
        with pytest.raises(ValueError):
            create_named_tuple_songs([])  # Empty list
            
        # Test sorting with invalid key
        with pytest.raises(ValueError):
            sort_songs(songs, "invalid_key")
            
        test_obj.yakshaAssert("TestInputValidation", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputValidation", False, "exception")
        pytest.fail(f"Input validation test failed: {str(e)}")

def test_data_integrity(test_obj):
    """Test data integrity and immutability"""
    try:
        # Test tuple immutability
        songs, new_releases, genres = initialize_data()
        original_songs = songs.copy()
        
        # Attempt modifications should create new lists/tuples
        filtered_songs = filter_by_genre(songs, "rock")
        assert songs == original_songs, "Original songs list should not be modified"
        
        sorted_songs = sort_songs(songs, "title")
        assert songs == original_songs, "Original songs list should not be modified"
        
        # Test new releases integration
        combined = integrate_new_releases(songs, new_releases)
        assert songs == original_songs, "Original songs list should not be modified"
        assert len(combined) == len(songs) + len(new_releases)
        
        # Test playlist immutability
        playlist = create_playlist("Test", [songs[0][0]], songs)
        assert isinstance(playlist, tuple), "Playlist should be an immutable tuple"
        
        test_obj.yakshaAssert("TestDataIntegrity", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestDataIntegrity", False, "exception")
        pytest.fail(f"Data integrity test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])