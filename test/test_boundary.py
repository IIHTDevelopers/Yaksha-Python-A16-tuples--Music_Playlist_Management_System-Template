import pytest
from test.TestUtils import TestUtils
from music_playlist_management_system import *

@pytest.fixture
def test_obj():
    return TestUtils()

def test_boundary_scenarios(test_obj):
    """Test boundary cases for tuple operations"""
    try:
        # Test with empty data
        empty_songs = []
        
        # Test filtering empty data
        assert filter_by_genre(empty_songs, "rock") == []
        assert filter_by_artist(empty_songs, "Queen") == []
        assert filter_by_duration(empty_songs, 0, 300) == []
        assert filter_by_decade(empty_songs, 1970) == []
        
        # Test with single song
        single_song = ("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")
        single_list = [single_song]
        
        # Test single song filtering
        assert len(filter_by_genre(single_list, "rock")) == 1
        assert len(filter_by_genre(single_list, "pop")) == 0
        
        # Test duration boundaries
        assert len(filter_by_duration(single_list, 179, 181)) == 1
        assert len(filter_by_duration(single_list, 181, 190)) == 0
        
        # Test decade boundaries
        assert len(filter_by_decade(single_list, 2000)) == 1
        assert len(filter_by_decade(single_list, 1990)) == 0
        
        # Test named tuple conversion
        named_songs = create_named_tuple_songs(single_list)
        assert len(named_songs) == 1
        assert hasattr(named_songs[0], 'title')
        
        # Test empty playlist creation
        with pytest.raises(ValueError):
            create_playlist("Empty", [], single_list)
        
        # Test genre distribution with single song
        genres = ("rock", "pop")
        distribution = calculate_genre_distribution(single_list, genres)
        assert distribution["rock"] == 1
        assert distribution["pop"] == 0
        
        test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
        pytest.fail(f"Boundary scenarios test failed: {str(e)}")

def test_extreme_values(test_obj):
    """Test extreme value cases"""
    try:
        songs, _, _ = initialize_data()
        
        # Test extremely short and long durations
        very_short = 1
        very_long = 100000
        
        short_filtered = filter_by_duration(songs, very_short, very_short)
        assert len(short_filtered) == 0
        
        long_filtered = filter_by_duration(songs, very_long, very_long)
        assert len(long_filtered) == 0
        
        # Test extreme years
        very_old = 1000
        future = 3000
        
        old_songs = filter_by_decade(songs, very_old)
        assert len(old_songs) == 0
        
        future_songs = filter_by_decade(songs, future)
        assert len(future_songs) == 0
        
        test_obj.yakshaAssert("TestExtremeValues", True, "boundary")
    except Exception as e:
        test_obj.yakshaAssert("TestExtremeValues", False, "boundary")
        pytest.fail(f"Extreme values test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])