import pytest
import inspect
import importlib
from test.TestUtils import TestUtils
from music_playlist_management_system import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_variable_naming(test_obj):
    """Test required variable names and structure"""
    try:
        module = importlib.import_module("music_playlist_management_system")
        
        init_source = inspect.getsource(module.initialize_data)
        assert "songs =" in init_source, "Must use 'songs' variable"
        assert "new_releases =" in init_source, "Must use 'new_releases' variable"
        assert "genres =" in init_source, "Must use 'genres' variable"
        
        songs, _, _ = initialize_data()
        song_ids = [s[0] for s in songs]
        required_ids = ["S001", "S002", "S003", "S004", "S005"]
        assert all(id in song_ids for id in required_ids), "Missing required songs"
        
        _, new_releases, _ = initialize_data()
        release_ids = [r[0] for r in new_releases]
        required_releases = ["N001", "N002"]
        assert all(id in release_ids for id in required_releases), "Missing required new releases"
        
        test_obj.yakshaAssert("TestVariableNaming", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestVariableNaming", False, "functional")
        pytest.fail(f"Variable naming test failed: {str(e)}")

def test_tuple_operations(test_obj):
    """Test tuple operations and immutability"""
    try:
        songs, _, genres = initialize_data()
        
        # Test song creation and immutability
        song = create_song_record("T001", "Test", "Artist", "rock", 180, 2000, "Album")
        assert isinstance(song, tuple), "Must return tuple"
        assert len(song) == 7, "Tuple must have 7 elements"
        with pytest.raises(TypeError):
            song[1] = "New Title"
        
        # Test filtering operations with tuple indexing
        filtered = filter_by_genre(songs, "rock")
        assert all(s[3] == "rock" for s in filtered), "Genre filter failed"
        
        filtered = filter_by_artist(songs, "Queen")
        assert all(s[2] == "Queen" for s in filtered), "Artist filter failed"
        
        # Test tuple unpacking in duration filter
        filtered = filter_by_duration(songs, 0, 300)
        if filtered:
            _, _, _, _, duration, _, _ = filtered[0]
            assert duration <= 300, "Duration tuple unpacking failed"
        
        # Test multi-key sorting with tuples
        sorted_songs = sort_songs(songs, "artist_year")
        if len(sorted_songs) > 1:
            assert sorted_songs[0][2] <= sorted_songs[1][2], "Artist+year sort failed"
        
        # Test named tuple conversion and field access
        named_songs = create_named_tuple_songs(songs)
        assert all(hasattr(s, 'title') for s in named_songs), "Named tuple fields missing"
        assert named_songs[0].title == songs[0][1], "Named tuple field access failed"
        with pytest.raises(AttributeError):
            named_songs[0].title = "New Title"
        
        test_obj.yakshaAssert("TestTupleOperations", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestTupleOperations", False, "functional")
        pytest.fail(f"Tuple operations test failed: {str(e)}")

def test_data_manipulation(test_obj):
    """Test data manipulation and statistics"""
    try:
        songs, new_releases, genres = initialize_data()
        
        # Test sorting operations
        sorted_songs = sort_songs(songs, "artist")
        assert all(sorted_songs[i][2] <= sorted_songs[i+1][2] 
                  for i in range(len(sorted_songs)-1)), "Artist sort failed"
        
        # Test decade filtering
        decade_songs = filter_by_decade(songs, 1970)
        assert all(1970 <= s[5] <= 1979 for s in decade_songs), "Decade filter failed"
        
        # Test genre distribution accuracy
        genre_counts = calculate_genre_distribution(songs, genres)
        for genre in genres:
            expected = len([s for s in songs if s[3] == genre])
            assert genre_counts[genre] == expected, f"Wrong count for {genre}"
        
        # Test playlist creation and immutability
        playlist = create_playlist("Test", [songs[0][0]], songs)
        assert isinstance(playlist, tuple), "Playlist must be tuple"
        assert len(playlist) == 3, "Playlist must have 3 elements"
        with pytest.raises(TypeError):
            playlist[0] = "New Name"
        
        # Test new releases integration
        combined = integrate_new_releases(songs, new_releases)
        assert len(combined) == len(songs) + len(new_releases), "Integration failed"
        assert all(s in combined for s in songs), "Missing original songs"
        assert all(r in combined for r in new_releases), "Missing new releases"
        
        test_obj.yakshaAssert("TestDataManipulation", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestDataManipulation", False, "functional")
        pytest.fail(f"Data manipulation test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])