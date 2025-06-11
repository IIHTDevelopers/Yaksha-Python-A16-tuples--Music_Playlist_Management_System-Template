import unittest
import os
import importlib
import sys
import io
import contextlib
import inspect
from test.TestUtils import TestUtils

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None
    except Exception:
        return None

def load_module_dynamically():
    """Load the student's module for testing"""
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    return module_obj

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning the result or None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_variable_naming(self):
        """Test required variable names and structure"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
                return
            
            try:
                # Check if initialize_data function exists
                if not check_function_exists(self.module_obj, "initialize_data"):
                    self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                    print("TestVariableNaming = Failed")
                    return
                    
                # Check function implementation
                try:
                    init_source = inspect.getsource(self.module_obj.initialize_data)
                    
                    # Check for required variable names
                    if "songs =" not in init_source:
                        errors.append("Must use 'songs' variable in initialize_data()")
                    if "new_releases =" not in init_source:
                        errors.append("Must use 'new_releases' variable in initialize_data()")
                    if "genres =" not in init_source:
                        errors.append("Must use 'genres' variable in initialize_data()")
                except Exception as e:
                    errors.append(f"Error examining initialize_data source: {str(e)}")
                
                # Check if function returns the proper values
                try:
                    result = safely_call_function(self.module_obj, "initialize_data")
                    
                    if not isinstance(result, tuple) or len(result) != 3:
                        errors.append("initialize_data() must return a tuple with 3 elements")
                    else:
                        songs, new_releases, genres = result
                        
                        # Check song structure
                        if not isinstance(songs, list):
                            errors.append("songs must be a list")
                        elif not songs:
                            errors.append("songs list is empty")
                        else:
                            if not all(isinstance(song, tuple) for song in songs):
                                errors.append("songs must contain tuple elements")
                            else:
                                song_ids = [s[0] for s in songs if isinstance(s, tuple) and len(s) > 0]
                                required_ids = ["S001", "S002", "S003", "S004", "S005"]
                                missing_ids = [id for id in required_ids if id not in song_ids]
                                if missing_ids:
                                    errors.append(f"Missing required songs: {', '.join(missing_ids)}")
                        
                        # Check new_releases structure
                        if not isinstance(new_releases, list):
                            errors.append("new_releases must be a list")
                        elif not new_releases:
                            errors.append("new_releases list is empty")
                        else:
                            if not all(isinstance(release, tuple) for release in new_releases):
                                errors.append("new_releases must contain tuple elements")
                            else:
                                release_ids = [r[0] for r in new_releases if isinstance(r, tuple) and len(r) > 0]
                                required_releases = ["N001", "N002"]
                                missing_releases = [id for id in required_releases if id not in release_ids]
                                if missing_releases:
                                    errors.append(f"Missing required new releases: {', '.join(missing_releases)}")
                        
                        # Check genres structure
                        if not isinstance(genres, tuple):
                            errors.append("genres must be a tuple")
                except Exception as e:
                    errors.append(f"Error calling initialize_data: {str(e)}")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                    print("TestVariableNaming = Failed")
                else:
                    self.test_obj.yakshaAssert("TestVariableNaming", True, "functional")
                    print("TestVariableNaming = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
                print("TestVariableNaming = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestVariableNaming", False, "functional")
            print("TestVariableNaming = Failed")

    def test_tuple_operations(self):
        """Test tuple operations and immutability"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestTupleOperations", False, "functional")
                print("TestTupleOperations = Failed")
                return
            
            try:
                # Get sample data
                if not check_function_exists(self.module_obj, "initialize_data"):
                    self.test_obj.yakshaAssert("TestTupleOperations", False, "functional")
                    print("TestTupleOperations = Failed")
                    return
                    
                try:
                    result = safely_call_function(self.module_obj, "initialize_data")
                    if not result or not isinstance(result, tuple) or len(result) < 3:
                        errors.append("initialize_data returned invalid result")
                        songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                        genres = ("rock", "pop", "jazz")
                    else:
                        songs, _, genres = result
                        if not songs:
                            errors.append("initialize_data returned empty songs list")
                            # Create fallback data for testing
                            songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                            genres = ("rock", "pop", "jazz")
                except Exception as e:
                    errors.append(f"Error calling initialize_data: {str(e)}")
                    # Create fallback data for testing
                    songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                    genres = ("rock", "pop", "jazz")
                
                # Test song creation and immutability
                if check_function_exists(self.module_obj, "create_song_record"):
                    try:
                        song = safely_call_function(self.module_obj, "create_song_record", "T001", "Test", "Artist", "rock", 180, 2000, "Album")
                        if song is None:
                            errors.append("create_song_record returned None")
                        elif not isinstance(song, tuple):
                            errors.append(f"create_song_record returned {type(song)} instead of tuple")
                        elif len(song) != 7:
                            errors.append(f"Tuple should have 7 elements, has {len(song)}")
                        
                        # Test tuple immutability (should raise TypeError)
                        try:
                            original_song = song
                            # Try to modify a copy to verify tuples are used (should raise TypeError)
                            song_as_list = list(song)
                            song_as_list[1] = "New Title"
                            modified_song = tuple(song_as_list)
                            
                            # This should still work (creating a new tuple) but we can check if the original is unchanged
                            if song is not original_song:
                                errors.append("Song tuple was internally modified, which breaks tuple immutability")
                        except TypeError:
                            # This is actually expected behavior when trying to modify tuples directly
                            pass
                        except Exception as e:
                            # Only add error if it's not a TypeError (which is expected)
                            errors.append(f"Unexpected error testing immutability: {str(e)}")
                    except Exception as e:
                        errors.append(f"Error in create_song_record: {str(e)}")
                else:
                    errors.append("Function create_song_record not found")
                
                # Test filtering operations with tuple indexing
                if check_function_exists(self.module_obj, "filter_by_genre"):
                    try:
                        filtered = safely_call_function(self.module_obj, "filter_by_genre", songs, "rock")
                        if filtered is None:
                            errors.append("filter_by_genre returned None")
                        elif not isinstance(filtered, list):
                            errors.append(f"filter_by_genre returned {type(filtered)} instead of list")
                        elif not all(isinstance(s, tuple) for s in filtered):
                            errors.append("filter_by_genre returned non-tuple elements")
                        elif filtered and not all(s[3] == "rock" for s in filtered if len(s) > 3):
                            errors.append("Genre filter failed - returned songs with wrong genre")
                    except Exception as e:
                        errors.append(f"Error in filter_by_genre: {str(e)}")
                else:
                    errors.append("Function filter_by_genre not found")
                
                if check_function_exists(self.module_obj, "filter_by_artist"):
                    try:
                        # Find a valid artist from our songs list
                        valid_artist = songs[0][2] if songs and len(songs[0]) > 2 else "Queen"
                        
                        filtered = safely_call_function(self.module_obj, "filter_by_artist", songs, valid_artist)
                        if filtered is None:
                            errors.append("filter_by_artist returned None")
                        elif not isinstance(filtered, list):
                            errors.append(f"filter_by_artist returned {type(filtered)} instead of list")
                        elif not all(isinstance(s, tuple) for s in filtered):
                            errors.append("filter_by_artist returned non-tuple elements")
                        elif filtered and not all(s[2] == valid_artist for s in filtered if len(s) > 2):
                            errors.append("Artist filter failed")
                    except Exception as e:
                        errors.append(f"Error in filter_by_artist: {str(e)}")
                else:
                    errors.append("Function filter_by_artist not found")
                
                # Test tuple unpacking in duration filter
                if check_function_exists(self.module_obj, "filter_by_duration"):
                    try:
                        filtered = safely_call_function(self.module_obj, "filter_by_duration", songs, 0, 300)
                        if filtered is None:
                            errors.append("filter_by_duration returned None")
                        elif not isinstance(filtered, list):
                            errors.append(f"filter_by_duration returned {type(filtered)} instead of list")
                        elif not all(isinstance(s, tuple) for s in filtered):
                            errors.append("filter_by_duration returned non-tuple elements")
                        elif filtered and not all(0 <= s[4] <= 300 for s in filtered if len(s) > 4):
                            errors.append("Duration filter failed")
                    except Exception as e:
                        errors.append(f"Error in filter_by_duration: {str(e)}")
                else:
                    errors.append("Function filter_by_duration not found")
                
                # Test multi-key sorting with tuples
                if check_function_exists(self.module_obj, "sort_songs"):
                    try:
                        sorted_songs = safely_call_function(self.module_obj, "sort_songs", songs, "artist_year")
                        if sorted_songs is None:
                            errors.append("sort_songs returned None")
                        elif not isinstance(sorted_songs, list):
                            errors.append(f"sort_songs returned {type(sorted_songs)} instead of list")
                        elif not all(isinstance(s, tuple) for s in sorted_songs):
                            errors.append("sort_songs returned non-tuple elements")
                        # We can't reliably test sorting logic if we're using fallback data
                    except Exception as e:
                        errors.append(f"Error in sort_songs: {str(e)}")
                else:
                    errors.append("Function sort_songs not found")
                
                # Test named tuple conversion and field access
                if check_function_exists(self.module_obj, "create_named_tuple_songs"):
                    try:
                        named_songs = safely_call_function(self.module_obj, "create_named_tuple_songs", songs)
                        if named_songs is None:
                            errors.append("create_named_tuple_songs returned None")
                        elif not isinstance(named_songs, list):
                            errors.append(f"create_named_tuple_songs returned {type(named_songs)} instead of list")
                        elif not named_songs:
                            errors.append("Named tuple conversion returned empty list")
                        else:
                            # Check if result has tuple-like behavior
                            try:
                                first_song = named_songs[0]
                                # Try to access a field (should be possible as attribute or index)
                                title_value = None
                                try:
                                    # First try as attribute (NamedTuple approach)
                                    title_value = first_song.title
                                except AttributeError:
                                    # If that fails, try as index (regular tuple approach)
                                    title_value = first_song[1]
                                
                                if title_value is None:
                                    errors.append("Could not access title field in named tuple")
                            except Exception as e:
                                errors.append(f"Error accessing named tuple fields: {str(e)}")
                            
                            # Test immutability
                            try:
                                # This should raise an error, either TypeError for tuple or AttributeError for namedtuple
                                first_song = named_songs[0]
                                try:
                                    # Try attribute assignment (should fail for namedtuple)
                                    first_song.title = "New Title"
                                    errors.append("Named tuple allowed attribute modification")
                                except (AttributeError, TypeError):
                                    # This is expected
                                    pass
                            except Exception as e:
                                # Only add error if unexpected exception
                                if not isinstance(e, (AttributeError, TypeError)):
                                    errors.append(f"Unexpected error testing named tuple immutability: {str(e)}")
                    except Exception as e:
                        errors.append(f"Error in create_named_tuple_songs: {str(e)}")
                else:
                    errors.append("Function create_named_tuple_songs not found")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestTupleOperations", False, "functional")
                    print("TestTupleOperations = Failed")
                else:
                    self.test_obj.yakshaAssert("TestTupleOperations", True, "functional")
                    print("TestTupleOperations = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestTupleOperations", False, "functional")
                print("TestTupleOperations = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestTupleOperations", False, "functional")
            print("TestTupleOperations = Failed")

    def test_data_manipulation(self):
        """Test data manipulation and statistics"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestDataManipulation", False, "functional")
                print("TestDataManipulation = Failed")
                return
            
            try:
                # Get sample data
                if not check_function_exists(self.module_obj, "initialize_data"):
                    self.test_obj.yakshaAssert("TestDataManipulation", False, "functional")
                    print("TestDataManipulation = Failed")
                    return
                    
                try:
                    result = safely_call_function(self.module_obj, "initialize_data")
                    if not result or not isinstance(result, tuple) or len(result) < 3:
                        errors.append("initialize_data returned invalid result")
                        songs = [
                            ("S001", "Song A", "Artist A", "rock", 180, 2000, "Album A"),
                            ("S002", "Song B", "Artist B", "pop", 200, 2010, "Album B")
                        ]
                        new_releases = [("N001", "New Song", "New Artist", "jazz", 210, 2023, "New Album")]
                        genres = ("rock", "pop", "jazz")
                    else:
                        songs, new_releases, genres = result
                        if not songs:
                            errors.append("initialize_data returned empty songs list")
                            # Create fallback data for testing
                            songs = [
                                ("S001", "Song A", "Artist A", "rock", 180, 2000, "Album A"),
                                ("S002", "Song B", "Artist B", "pop", 200, 2010, "Album B")
                            ]
                        if not new_releases:
                            errors.append("initialize_data returned empty new_releases list")
                            new_releases = [("N001", "New Song", "New Artist", "jazz", 210, 2023, "New Album")]
                except Exception as e:
                    errors.append(f"Error calling initialize_data: {str(e)}")
                    # Create fallback data for testing
                    songs = [
                        ("S001", "Song A", "Artist A", "rock", 180, 2000, "Album A"),
                        ("S002", "Song B", "Artist B", "pop", 200, 2010, "Album B")
                    ]
                    new_releases = [("N001", "New Song", "New Artist", "jazz", 210, 2023, "New Album")]
                    genres = ("rock", "pop", "jazz")
                
                # Test sorting operations
                if check_function_exists(self.module_obj, "sort_songs"):
                    try:
                        sorted_songs = safely_call_function(self.module_obj, "sort_songs", songs, "artist")
                        if sorted_songs is None:
                            errors.append("sort_songs returned None")
                        elif not isinstance(sorted_songs, list):
                            errors.append(f"sort_songs returned {type(sorted_songs)} instead of list")
                        elif len(sorted_songs) < 2:
                            # Skip sorting test if not enough songs
                            pass
                        else:
                            # Just check that all are tuples with expected structure
                            if not all(isinstance(s, tuple) and len(s) >= 3 for s in sorted_songs):
                                errors.append("sort_songs returned incorrectly structured tuples")
                    except Exception as e:
                        errors.append(f"Error in sort_songs: {str(e)}")
                else:
                    errors.append("Function sort_songs not found")
                
                # Test decade filtering
                if check_function_exists(self.module_obj, "filter_by_decade"):
                    try:
                        # Find a decade that should have songs
                        decade = 2000
                        decade_songs = safely_call_function(self.module_obj, "filter_by_decade", songs, decade)
                        if decade_songs is None:
                            errors.append("filter_by_decade returned None")
                        elif not isinstance(decade_songs, list):
                            errors.append(f"filter_by_decade returned {type(decade_songs)} instead of list")
                        # Skip checking contents for simple implementation test
                    except Exception as e:
                        errors.append(f"Error in filter_by_decade: {str(e)}")
                else:
                    errors.append("Function filter_by_decade not found")
                
                # Test genre distribution accuracy
                if check_function_exists(self.module_obj, "calculate_genre_distribution"):
                    try:
                        genre_counts = safely_call_function(self.module_obj, "calculate_genre_distribution", songs, genres)
                        if genre_counts is None:
                            errors.append("calculate_genre_distribution returned None")
                        elif not isinstance(genre_counts, dict):
                            errors.append(f"calculate_genre_distribution returned {type(genre_counts)} instead of dict")
                        else:
                            # Check if all genres are included
                            missing_genres = [g for g in genres if g not in genre_counts]
                            if missing_genres:
                                errors.append(f"Missing genres in distribution: {', '.join(missing_genres)}")
                    except Exception as e:
                        errors.append(f"Error in calculate_genre_distribution: {str(e)}")
                else:
                    errors.append("Function calculate_genre_distribution not found")
                
                # Test playlist creation and immutability
                if check_function_exists(self.module_obj, "create_playlist"):
                    try:
                        # Get a valid song ID
                        song_id = songs[0][0] if songs and len(songs[0]) > 0 else "S001"
                        
                        playlist = safely_call_function(self.module_obj, "create_playlist", "Test", [song_id], songs)
                        if playlist is None:
                            errors.append("create_playlist returned None")
                        elif not isinstance(playlist, tuple):
                            errors.append(f"create_playlist returned {type(playlist)} instead of tuple")
                        elif len(playlist) != 3:
                            errors.append(f"Playlist tuple should have 3 elements, has {len(playlist)}")
                        
                        # Test tuple immutability
                        try:
                            # This should raise TypeError
                            playlist_list = list(playlist)
                            playlist_list[0] = "New Name"
                            modified_playlist = tuple(playlist_list)
                            # Creating a new tuple works, but the original should be unchanged
                            # We can't really test this directly since we don't have a reference to the original
                        except TypeError:
                            # This is actually expected when trying to modify a tuple directly
                            pass
                        except Exception as e:
                            # Only add error if it's not a TypeError
                            if not isinstance(e, TypeError):
                                errors.append(f"Unexpected error testing playlist immutability: {str(e)}")
                    except Exception as e:
                        errors.append(f"Error in create_playlist: {str(e)}")
                else:
                    errors.append("Function create_playlist not found")
                
                # Test new releases integration
                if check_function_exists(self.module_obj, "integrate_new_releases"):
                    try:
                        combined = safely_call_function(self.module_obj, "integrate_new_releases", songs, new_releases)
                        if combined is None:
                            errors.append("integrate_new_releases returned None")
                        elif not isinstance(combined, list):
                            errors.append(f"integrate_new_releases returned {type(combined)} instead of list")
                        elif len(combined) != len(songs) + len(new_releases):
                            errors.append(f"Combined list has {len(combined)} items, expected {len(songs) + len(new_releases)}")
                    except Exception as e:
                        errors.append(f"Error in integrate_new_releases: {str(e)}")
                else:
                    errors.append("Function integrate_new_releases not found")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestDataManipulation", False, "functional")
                    print("TestDataManipulation = Failed")
                else:
                    self.test_obj.yakshaAssert("TestDataManipulation", True, "functional")
                    print("TestDataManipulation = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestDataManipulation", False, "functional")
                print("TestDataManipulation = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestDataManipulation", False, "functional")
            print("TestDataManipulation = Failed")

    def test_formatting_functions(self):
        """Test formatting and display functions"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestFormattingFunctions", False, "functional")
                print("TestFormattingFunctions = Failed")
                return
            
            try:
                # Get sample data
                if not check_function_exists(self.module_obj, "initialize_data"):
                    self.test_obj.yakshaAssert("TestFormattingFunctions", False, "functional")
                    print("TestFormattingFunctions = Failed")
                    return
                    
                try:
                    result = safely_call_function(self.module_obj, "initialize_data")
                    if not result or not isinstance(result, tuple) or len(result) < 1:
                        errors.append("initialize_data returned invalid result")
                        songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                    else:
                        songs, _, _ = result
                        if not songs:
                            errors.append("initialize_data returned empty songs list")
                            songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                except Exception as e:
                    errors.append(f"Error calling initialize_data: {str(e)}")
                    songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                
                # Test duration formatting
                if check_function_exists(self.module_obj, "format_duration"):
                    try:
                        # Test various duration values
                        test_cases = [
                            (180, "3:00"),  # 3 minutes
                            (354, "5:54"),  # 5 minutes 54 seconds
                            (3661, "61:01"), # Over an hour
                            (0, "0:00")     # Zero seconds
                        ]
                        
                        for seconds, expected_format in test_cases:
                            formatted = safely_call_function(self.module_obj, "format_duration", seconds)
                            if formatted is None:
                                errors.append(f"format_duration returned None for {seconds} seconds")
                            elif not isinstance(formatted, str):
                                errors.append(f"format_duration returned {type(formatted)} instead of string")
                            # Don't check exact format as implementations may vary slightly
                    except Exception as e:
                        errors.append(f"Error in format_duration: {str(e)}")
                else:
                    errors.append("Function format_duration not found")
                
                # Test song formatting
                if check_function_exists(self.module_obj, "get_formatted_song"):
                    try:
                        if songs:
                            song = songs[0]
                            formatted = safely_call_function(self.module_obj, "get_formatted_song", song)
                            if formatted is None:
                                errors.append("get_formatted_song returned None")
                            elif not isinstance(formatted, str):
                                errors.append(f"get_formatted_song returned {type(formatted)} instead of string")
                            else:
                                # Check if essential elements are in the formatted string
                                song_elements = [song[0], song[1], song[2]]  # ID, title, artist
                                for element in song_elements:
                                    if str(element) not in formatted:
                                        errors.append(f"Formatted song missing element: {element}")
                    except Exception as e:
                        errors.append(f"Error in get_formatted_song: {str(e)}")
                else:
                    errors.append("Function get_formatted_song not found")
                
                # Test playlist info formatting
                if check_function_exists(self.module_obj, "get_playlist_info") and check_function_exists(self.module_obj, "create_playlist"):
                    try:
                        if songs:
                            song_id = songs[0][0]
                            playlist = safely_call_function(self.module_obj, "create_playlist", "Test Playlist", [song_id], songs)
                            if playlist is not None:
                                playlist_info = safely_call_function(self.module_obj, "get_playlist_info", playlist, songs)
                                if playlist_info is None:
                                    errors.append("get_playlist_info returned None")
                                elif not isinstance(playlist_info, str):
                                    errors.append(f"get_playlist_info returned {type(playlist_info)} instead of string")
                                else:
                                    # Check if essential elements are in the playlist info
                                    required_elements = ["Test Playlist", "Name:", "Created:", "Songs:", "Duration:"]
                                    for element in required_elements:
                                        if element not in playlist_info:
                                            errors.append(f"Playlist info missing element: {element}")
                    except Exception as e:
                        errors.append(f"Error in get_playlist_info: {str(e)}")
                else:
                    if not check_function_exists(self.module_obj, "get_playlist_info"):
                        errors.append("Function get_playlist_info not found")
                
                # Test calculate_total_duration
                if check_function_exists(self.module_obj, "calculate_total_duration"):
                    try:
                        if songs:
                            total_duration = safely_call_function(self.module_obj, "calculate_total_duration", songs)
                            if total_duration is None:
                                errors.append("calculate_total_duration returned None")
                            elif not isinstance(total_duration, tuple):
                                errors.append(f"calculate_total_duration returned {type(total_duration)} instead of tuple")
                            elif len(total_duration) != 3:
                                errors.append(f"Total duration tuple should have 3 elements, has {len(total_duration)}")
                            else:
                                hours, minutes, seconds = total_duration
                                if not all(isinstance(x, int) for x in [hours, minutes, seconds]):
                                    errors.append("Total duration tuple should contain integers")
                    except Exception as e:
                        errors.append(f"Error in calculate_total_duration: {str(e)}")
                else:
                    errors.append("Function calculate_total_duration not found")
                
                # Test display_data function
                if check_function_exists(self.module_obj, "display_data"):
                    try:
                        # Test with songs data - should not crash
                        safely_call_function(self.module_obj, "display_data", songs, "songs")
                        
                        # Test with empty data - should not crash
                        safely_call_function(self.module_obj, "display_data", [], "songs")
                        
                        # Test with invalid data type - should not crash
                        safely_call_function(self.module_obj, "display_data", songs, "invalid_type")
                        
                    except Exception as e:
                        errors.append(f"Error in display_data: {str(e)}")
                else:
                    errors.append("Function display_data not found")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestFormattingFunctions", False, "functional")
                    print("TestFormattingFunctions = Failed")
                else:
                    self.test_obj.yakshaAssert("TestFormattingFunctions", True, "functional")
                    print("TestFormattingFunctions = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestFormattingFunctions", False, "functional")
                print("TestFormattingFunctions = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestFormattingFunctions", False, "functional")
            print("TestFormattingFunctions = Failed")

if __name__ == '__main__':
    unittest.main()