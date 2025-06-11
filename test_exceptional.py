import unittest
import os
import importlib
import sys
import io
import contextlib
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

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = func(*args)
            # If function returns None, it might be unimplemented (has pass statement)
            if result is None:
                return False  # Consider this as "function doesn't raise exception properly"
            return False
    except expected_exception:
        return True
    except Exception:
        return False

def is_function_implemented(module, function_name, test_args):
    """Check if a function is implemented (doesn't just return None)."""
    if not check_function_exists(module, function_name):
        return False
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = getattr(module, function_name)(*test_args)
            # If result is None, function might have 'pass' statement
            return result is not None
    except Exception:
        # If it raises an exception, it's at least trying to do something
        return True

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_comprehensive_exception_handling(self):
        """Comprehensive test for all exception handling scenarios"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            # Check for initialize_data function
            if not check_function_exists(self.module_obj, "initialize_data"):
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
                return
            
            try:
                # Get sample data
                try:
                    result = safely_call_function(self.module_obj, "initialize_data")
                    if result is None or not isinstance(result, tuple) or len(result) != 3:
                        errors.append("initialize_data returned invalid data format")
                        # Create fallback data
                        songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                        new_releases = [("N001", "New Song", "New Artist", "pop", 200, 2023, "New Album")]
                        genres = ("rock", "pop", "jazz")
                    else:
                        songs, new_releases, genres = result
                        if not songs:
                            # Create fallback data for testing
                            songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                        if not new_releases:
                            new_releases = [("N001", "New Song", "New Artist", "pop", 200, 2023, "New Album")]
                        if not genres:
                            genres = ("rock", "pop", "jazz")
                except Exception as e:
                    errors.append(f"Error calling initialize_data: {str(e)}")
                    # Create fallback data
                    songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                    new_releases = [("N001", "New Song", "New Artist", "pop", 200, 2023, "New Album")]
                    genres = ("rock", "pop", "jazz")
                
                # =================================================================
                # SECTION 1: SONG RECORD CREATION VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "create_song_record"):
                    test_cases = [
                        (["", "Title", "Artist", "rock", 180, 2000, "Album"], "Empty ID"),
                        (["S001", "", "Artist", "rock", 180, 2000, "Album"], "Empty title"),
                        (["S001", "Title", "", "rock", 180, 2000, "Album"], "Empty artist"),
                        (["S001", "Title", "Artist", "", 180, 2000, "Album"], "Empty genre"),
                        (["S001", "Title", "Artist", "rock", -1, 2000, "Album"], "Negative duration"),
                        (["S001", "Title", "Artist", "rock", 0, 2000, "Album"], "Zero duration"),
                        (["S001", "Title", "Artist", "rock", 180, 2000, ""], "Empty album"),
                        ([None, "Title", "Artist", "rock", 180, 2000, "Album"], "None ID"),
                        (["S001", None, "Artist", "rock", 180, 2000, "Album"], "None title"),
                        (["S001", "Title", "Artist", "rock", "not_int", 2000, "Album"], "Non-integer duration"),
                        (["S001", "Title", "Artist", "rock", 180, "not_int", "Album"], "Non-integer year")
                    ]
                    
                    for args, test_desc in test_cases:
                        try:
                            result = check_raises(getattr(self.module_obj, "create_song_record"), args, ValueError)
                            if not result:
                                # Check if function is unimplemented
                                if not is_function_implemented(self.module_obj, "create_song_record", ["S001", "Title", "Artist", "rock", 180, 2000, "Album"]):
                                    errors.append(f"create_song_record returned None with {test_desc} - function may not be implemented yet")
                                else:
                                    errors.append(f"create_song_record does not raise ValueError with {test_desc}")
                        except Exception as e:
                            errors.append(f"Error testing create_song_record with {test_desc}: {str(e)}")
                else:
                    errors.append("Function create_song_record not found")
                
                # =================================================================
                # SECTION 2: FILTER FUNCTION VALIDATION
                # =================================================================
                
                filter_test_cases = [
                    ("filter_by_genre", [songs, ""], "empty genre"),
                    ("filter_by_genre", [songs, None], "None genre"),
                    ("filter_by_artist", [songs, ""], "empty artist"),
                    ("filter_by_artist", [songs, None], "None artist"),
                    ("filter_by_duration", [songs, -1, 100], "negative min duration"),
                    ("filter_by_duration", [songs, 200, 100], "min > max duration"),
                    ("filter_by_duration", [songs, 100, -1], "negative max duration"),
                    ("filter_by_decade", [songs, None], "None decade"),
                    ("filter_by_decade", [songs, "not_int"], "non-integer decade")
                ]
                
                for func_name, args, test_desc in filter_test_cases:
                    if check_function_exists(self.module_obj, func_name):
                        try:
                            func = getattr(self.module_obj, func_name)
                            result = check_raises(func, args, ValueError)
                            if not result:
                                # Check if function is unimplemented
                                if not is_function_implemented(self.module_obj, func_name, [songs, "rock"] if "genre" in func_name else [songs, "Queen"] if "artist" in func_name else [songs, 100, 200] if "duration" in func_name else [songs, 2000]):
                                    errors.append(f"{func_name} returned None with {test_desc} - function may not be implemented yet")
                                else:
                                    errors.append(f"{func_name} does not raise ValueError with {test_desc}")
                        except Exception as e:
                            errors.append(f"Error testing {func_name} with {test_desc}: {str(e)}")
                    else:
                        errors.append(f"Function {func_name} not found")
                
                # =================================================================
                # SECTION 3: PLAYLIST CREATION VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "create_playlist"):
                    playlist_test_cases = [
                        (["", ["S001"], songs], "empty playlist name"),
                        ([None, ["S001"], songs], "None playlist name"),
                        (["Playlist", [], songs], "empty song IDs list"),
                        (["Playlist", None, songs], "None song IDs"),
                        (["Playlist", ["INVALID_ID"], songs], "invalid song ID"),
                        (["Playlist", ["S001"], []], "empty songs list"),
                        (["Playlist", ["S001"], None], "None songs list")
                    ]
                    
                    for args, test_desc in playlist_test_cases:
                        try:
                            func = getattr(self.module_obj, "create_playlist")
                            result = check_raises(func, args, ValueError)
                            if not result:
                                # Check if function is unimplemented
                                if not is_function_implemented(self.module_obj, "create_playlist", ["Test", ["S001"], songs]):
                                    errors.append(f"create_playlist returned None with {test_desc} - function may not be implemented yet")
                                else:
                                    errors.append(f"create_playlist does not raise ValueError with {test_desc}")
                        except Exception as e:
                            errors.append(f"Error testing create_playlist with {test_desc}: {str(e)}")
                else:
                    errors.append("Function create_playlist not found")
                
                # =================================================================
                # SECTION 4: NAMED TUPLE CONVERSION VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "create_named_tuple_songs"):
                    try:
                        result = check_raises(getattr(self.module_obj, "create_named_tuple_songs"), [[]], ValueError)
                        if not result:
                            # Check if function is unimplemented
                            if not is_function_implemented(self.module_obj, "create_named_tuple_songs", [songs]):
                                errors.append("create_named_tuple_songs returned None with empty list - function may not be implemented yet")
                            else:
                                errors.append("create_named_tuple_songs does not raise ValueError with empty list")
                    except Exception as e:
                        errors.append(f"Error testing create_named_tuple_songs with empty list: {str(e)}")
                else:
                    errors.append("Function create_named_tuple_songs not found")
                
                # =================================================================
                # SECTION 5: SORTING VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "sort_songs"):
                    sort_test_cases = [
                        ([[], "title"], "empty songs list"),
                        ([songs, ""], "empty sort key"),
                        ([songs, None], "None sort key"),
                        ([songs, "invalid_key"], "invalid sort key")
                    ]
                    
                    for args, test_desc in sort_test_cases:
                        try:
                            result = check_raises(getattr(self.module_obj, "sort_songs"), args, ValueError)
                            if not result:
                                # Check if function is unimplemented
                                if not is_function_implemented(self.module_obj, "sort_songs", [songs, "title"]):
                                    errors.append(f"sort_songs returned None with {test_desc} - function may not be implemented yet")
                                else:
                                    errors.append(f"sort_songs does not raise ValueError with {test_desc}")
                        except Exception as e:
                            errors.append(f"Error testing sort_songs with {test_desc}: {str(e)}")
                else:
                    errors.append("Function sort_songs not found")
                
                # =================================================================
                # SECTION 6: DURATION FORMATTING VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "format_duration"):
                    duration_test_cases = [
                        ([-1], "negative duration"),
                        ([None], "None duration"),
                        (["not_int"], "non-integer duration")
                    ]
                    
                    for args, test_desc in duration_test_cases:
                        try:
                            result = check_raises(getattr(self.module_obj, "format_duration"), args, ValueError)
                            if not result:
                                # Check if function is unimplemented
                                if not is_function_implemented(self.module_obj, "format_duration", [180]):
                                    errors.append(f"format_duration returned None with {test_desc} - function may not be implemented yet")
                                else:
                                    errors.append(f"format_duration does not raise ValueError with {test_desc}")
                        except Exception as e:
                            errors.append(f"Error testing format_duration with {test_desc}: {str(e)}")
                else:
                    errors.append("Function format_duration not found")
                
                # =================================================================
                # SECTION 7: DATA INTEGRITY TESTS
                # =================================================================
                
                # Test tuple immutability
                original_songs = songs.copy()
                
                # Test filtering operations - data should not be modified
                if check_function_exists(self.module_obj, "filter_by_genre"):
                    try:
                        filtered_songs = safely_call_function(self.module_obj, "filter_by_genre", songs, "rock")
                        if songs != original_songs:
                            errors.append("Original songs list was modified by filter_by_genre")
                    except Exception as e:
                        errors.append(f"Error testing data integrity in filter_by_genre: {str(e)}")
                
                # Test sorting operations - data should not be modified
                if check_function_exists(self.module_obj, "sort_songs"):
                    try:
                        sorted_songs = safely_call_function(self.module_obj, "sort_songs", songs, "title")
                        if songs != original_songs:
                            errors.append("Original songs list was modified by sort_songs")
                    except Exception as e:
                        errors.append(f"Error testing data integrity in sort_songs: {str(e)}")
                
                # Test new releases integration - data should not be modified
                if check_function_exists(self.module_obj, "integrate_new_releases"):
                    try:
                        combined = safely_call_function(self.module_obj, "integrate_new_releases", songs, new_releases)
                        if songs != original_songs:
                            errors.append("Original songs list was modified by integrate_new_releases")
                        
                        if combined is not None:
                            if not isinstance(combined, list):
                                errors.append(f"integrate_new_releases returned {type(combined)} instead of list")
                            elif len(combined) != len(songs) + len(new_releases):
                                errors.append(f"Combined list length {len(combined)} does not match expected {len(songs) + len(new_releases)}")
                    except Exception as e:
                        errors.append(f"Error testing data integrity in integrate_new_releases: {str(e)}")
                
                # =================================================================
                # SECTION 8: EDGE CASE HANDLING TESTS
                # =================================================================
                
                # Test with non-existent values
                edge_case_tests = [
                    ("filter_by_genre", [songs, "non_existent_genre"], "non-existent genre"),
                    ("filter_by_artist", [songs, "non_existent_artist"], "non-existent artist"),
                    ("filter_by_decade", [songs, 1500], "very old decade"),
                    ("filter_by_decade", [songs, 3000], "future decade")
                ]
                
                for func_name, args, test_desc in edge_case_tests:
                    if check_function_exists(self.module_obj, func_name):
                        try:
                            result = safely_call_function(self.module_obj, func_name, *args)
                            if result is None:
                                if not is_function_implemented(self.module_obj, func_name, [songs, args[1]]):
                                    errors.append(f"{func_name} returned None for {test_desc} - function may not be implemented yet")
                                else:
                                    errors.append(f"{func_name} returned None for {test_desc}")
                            elif not isinstance(result, list):
                                errors.append(f"{func_name} returned {type(result)} instead of list")
                            elif result != []:
                                errors.append(f"Should return empty list for {test_desc}")
                        except Exception as e:
                            errors.append(f"Error in {func_name} with {test_desc}: {str(e)}")
                
                # =================================================================
                # SECTION 9: GENRE DISTRIBUTION VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "calculate_genre_distribution"):
                    try:
                        # Test with empty songs list - should raise ValueError according to solution
                        result = check_raises(getattr(self.module_obj, "calculate_genre_distribution"), [[], genres], ValueError)
                        if not result:
                            if not is_function_implemented(self.module_obj, "calculate_genre_distribution", [songs, genres]):
                                errors.append("calculate_genre_distribution returned None with empty songs - function may not be implemented yet")
                            else:
                                errors.append("calculate_genre_distribution does not raise ValueError with empty songs")
                        
                        # Test with None genres
                        result2 = check_raises(getattr(self.module_obj, "calculate_genre_distribution"), [songs, None], ValueError)
                        if not result2:
                            if not is_function_implemented(self.module_obj, "calculate_genre_distribution", [songs, genres]):
                                errors.append("calculate_genre_distribution returned None with None genres - function may not be implemented yet")
                            else:
                                errors.append("calculate_genre_distribution does not raise ValueError with None genres")
                        
                        # Test with empty genres
                        result3 = check_raises(getattr(self.module_obj, "calculate_genre_distribution"), [songs, ()], ValueError)
                        if not result3:
                            if not is_function_implemented(self.module_obj, "calculate_genre_distribution", [songs, genres]):
                                errors.append("calculate_genre_distribution returned None with empty genres - function may not be implemented yet")
                            else:
                                errors.append("calculate_genre_distribution does not raise ValueError with empty genres")
                        
                    except Exception as e:
                        errors.append(f"Error testing calculate_genre_distribution: {str(e)}")
                else:
                    errors.append("Function calculate_genre_distribution not found")
                
                # =================================================================
                # SECTION 10: TOTAL DURATION CALCULATION VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "calculate_total_duration"):
                    try:
                        # Test with empty songs list
                        result = check_raises(getattr(self.module_obj, "calculate_total_duration"), [[]], ValueError)
                        if not result:
                            # Check if function is unimplemented
                            if not is_function_implemented(self.module_obj, "calculate_total_duration", [songs]):
                                errors.append("calculate_total_duration returned None with empty list - function may not be implemented yet")
                            else:
                                errors.append("calculate_total_duration does not raise ValueError with empty list")
                    except Exception as e:
                        errors.append(f"Error testing calculate_total_duration with empty list: {str(e)}")
                else:
                    errors.append("Function calculate_total_duration not found")
                
                # =================================================================
                # SECTION 11: DISPLAY FUNCTION VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "display_data"):
                    try:
                        # Test with None data (should raise exception)
                        result = check_raises(getattr(self.module_obj, "display_data"), [None], ValueError)
                        if not result:
                            if not is_function_implemented(self.module_obj, "display_data", [songs, "songs"]):
                                errors.append("display_data returned None with None data - function may not be implemented yet")
                            else:
                                errors.append("display_data does not raise ValueError with None data")
                        
                        # Test with invalid data type (should handle gracefully - no exception expected)
                        try:
                            safely_call_function(self.module_obj, "display_data", songs, "invalid_type")
                            # This should not raise an exception, just print "Unknown data type"
                        except Exception as e:
                            errors.append(f"display_data crashes with invalid data_type: {str(e)}")
                    except Exception as e:
                        errors.append(f"Error testing display_data: {str(e)}")
                else:
                    errors.append("Function display_data not found")
                
                # =================================================================
                # SECTION 12: INTEGRATION AND NEW RELEASES VALIDATION
                # =================================================================
                
                if check_function_exists(self.module_obj, "integrate_new_releases"):
                    try:
                        # Test with None songs list
                        result = check_raises(getattr(self.module_obj, "integrate_new_releases"), [None, new_releases], ValueError)
                        if not result:
                            if not is_function_implemented(self.module_obj, "integrate_new_releases", [songs, new_releases]):
                                errors.append("integrate_new_releases returned None with None songs - function may not be implemented yet")
                            else:
                                errors.append("integrate_new_releases does not raise ValueError with None songs")
                        
                        # Test with None new_releases
                        result2 = check_raises(getattr(self.module_obj, "integrate_new_releases"), [songs, None], ValueError)
                        if not result2:
                            if not is_function_implemented(self.module_obj, "integrate_new_releases", [songs, new_releases]):
                                errors.append("integrate_new_releases returned None with None new_releases - function may not be implemented yet")
                            else:
                                errors.append("integrate_new_releases does not raise ValueError with None new_releases")
                                
                    except Exception as e:
                        errors.append(f"Error testing integrate_new_releases: {str(e)}")
                
                # =================================================================
                # SECTION 13: FRAMEWORK ROBUSTNESS TEST
                # =================================================================
                
                # Test that the test framework is robust even with incomplete implementation
                class MockModule:
                    def initialize_data(self):
                        return ([], [], ())
                
                try:
                    mock_module = MockModule()
                    
                    # Test with minimal implementation
                    if check_function_exists(mock_module, "initialize_data"):
                        try:
                            mock_result = safely_call_function(mock_module, "initialize_data")
                            if not isinstance(mock_result, tuple) or len(mock_result) != 3:
                                errors.append("Mock initialize_data should return tuple with 3 elements")
                        except Exception as e:
                            errors.append(f"Error calling mock initialize_data: {str(e)}")
                    
                    # Test with missing function
                    if check_function_exists(mock_module, "filter_by_genre"):
                        errors.append("check_function_exists incorrectly identified missing function as existing")
                    
                    # Test safely_call_function with missing function
                    result = safely_call_function(mock_module, "non_existent_function", [])
                    if result is not None:
                        errors.append("safely_call_function should return None for missing function")
                except Exception as e:
                    errors.append(f"Framework robustness test failed: {str(e)}")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                    print("TestComprehensiveExceptionHandling = Failed")
                else:
                    self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", True, "exception")
                    print("TestComprehensiveExceptionHandling = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
                print("TestComprehensiveExceptionHandling = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestComprehensiveExceptionHandling", False, "exception")
            print("TestComprehensiveExceptionHandling = Failed")

if __name__ == '__main__':
    unittest.main()