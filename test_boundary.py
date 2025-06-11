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

class TestAssignment(unittest.TestCase):
    def setUp(self):
        """Standard setup for all test methods"""
        self.test_obj = TestUtils()
        self.module_obj = load_module_dynamically()

    def test_boundary_scenarios(self):
        """Test boundary cases for tuple operations"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
                return
            
            try:
                # Test with empty data
                empty_songs = []
                
                # Check for initialize_data function
                if not check_function_exists(self.module_obj, "initialize_data"):
                    self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                    print("TestBoundaryScenarios = Failed")
                    return
                
                # Get real data for later tests
                try:
                    result = safely_call_function(self.module_obj, "initialize_data")
                    if result is None:
                        errors.append("initialize_data returned None - function may not be implemented")
                        # Create fallback data
                        songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                        new_releases = [("N001", "New Song", "New Artist", "pop", 200, 2023, "New Album")]
                        genres = ("rock", "pop", "jazz")
                    elif not isinstance(result, tuple) or len(result) != 3:
                        errors.append("initialize_data must return tuple with 3 elements (songs, new_releases, genres)")
                        # Create fallback data
                        songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                        new_releases = [("N001", "New Song", "New Artist", "pop", 200, 2023, "New Album")]
                        genres = ("rock", "pop", "jazz")
                    else:
                        songs, new_releases, genres = result
                        if not songs:
                            errors.append("initialize_data returned empty songs list")
                            songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                except Exception as e:
                    errors.append(f"Error calling initialize_data: {str(e)}")
                    # Create fallback data
                    songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                    new_releases = [("N001", "New Song", "New Artist", "pop", 200, 2023, "New Album")]
                    genres = ("rock", "pop", "jazz")
                
                # Test all required functions with empty lists
                functions_to_test = [
                    ("filter_by_genre", [empty_songs, "rock"]),
                    ("filter_by_artist", [empty_songs, "Queen"]),
                    ("filter_by_duration", [empty_songs, 0, 300]),
                    ("filter_by_decade", [empty_songs, 1970])
                ]
                
                for func_name, args in functions_to_test:
                    if check_function_exists(self.module_obj, func_name):
                        try:
                            result = safely_call_function(self.module_obj, func_name, *args)
                            if result is None:
                                errors.append(f"{func_name} returned None for empty list - function may not be implemented")
                            elif not isinstance(result, list):
                                errors.append(f"{func_name} returned {type(result)} instead of list for empty input")
                            elif result != []:
                                errors.append(f"{func_name} on empty list should return empty list, got {result}")
                        except Exception as e:
                            errors.append(f"Error in {func_name} with empty list: {str(e)}")
                    else:
                        errors.append(f"Function {func_name} not found")
                
                # Test with single song if create_song_record function exists
                if check_function_exists(self.module_obj, "create_song_record"):
                    try:
                        single_song = safely_call_function(self.module_obj, "create_song_record", 
                                                          "S001", "Test Song", "Test Artist", 
                                                          "rock", 180, 2000, "Test Album")
                        if single_song is None:
                            errors.append("create_song_record returned None - function may not be implemented")
                            # Create a fallback single song for further tests
                            single_song = ("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")
                        elif not isinstance(single_song, tuple):
                            errors.append(f"create_song_record returned {type(single_song)} instead of tuple")
                            single_song = ("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")
                        elif len(single_song) != 7:
                            errors.append(f"Song tuple should have 7 elements, has {len(single_song)}")
                    except Exception as e:
                        errors.append(f"Error creating single song: {str(e)}")
                        # Create a fallback single song for further tests
                        single_song = ("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")
                else:
                    errors.append("Function create_song_record not found")
                    # Create a fallback single song for further tests
                    single_song = ("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")
                
                single_list = [single_song]
                
                # Test single song filtering
                if check_function_exists(self.module_obj, "filter_by_genre"):
                    try:
                        rock_filtered = safely_call_function(self.module_obj, "filter_by_genre", single_list, "rock")
                        if rock_filtered is None:
                            errors.append("filter_by_genre returned None for rock genre - function may not be implemented")
                        elif not isinstance(rock_filtered, list):
                            errors.append(f"filter_by_genre returned {type(rock_filtered)} instead of list")
                        elif len(rock_filtered) != 1:
                            errors.append(f"Should find 1 rock song, found {len(rock_filtered)}")
                        
                        pop_filtered = safely_call_function(self.module_obj, "filter_by_genre", single_list, "pop")
                        if pop_filtered is None:
                            errors.append("filter_by_genre returned None for pop genre - function may not be implemented")
                        elif not isinstance(pop_filtered, list):
                            errors.append(f"filter_by_genre returned {type(pop_filtered)} instead of list")
                        elif len(pop_filtered) != 0:
                            errors.append(f"Should find 0 pop songs, found {len(pop_filtered)}")
                    except Exception as e:
                        errors.append(f"Error in filter_by_genre with single song: {str(e)}")
                
                # Test duration boundaries
                if check_function_exists(self.module_obj, "filter_by_duration"):
                    try:
                        within_duration = safely_call_function(self.module_obj, "filter_by_duration", single_list, 179, 181)
                        if within_duration is None:
                            errors.append("filter_by_duration returned None for boundary case - function may not be implemented")
                        elif not isinstance(within_duration, list):
                            errors.append(f"filter_by_duration returned {type(within_duration)} instead of list")
                        elif len(within_duration) != 1:
                            errors.append(f"Should find 1 song within duration, found {len(within_duration)}")
                        
                        outside_duration = safely_call_function(self.module_obj, "filter_by_duration", single_list, 181, 190)
                        if outside_duration is None:
                            errors.append("filter_by_duration returned None for outside boundary case - function may not be implemented")
                        elif not isinstance(outside_duration, list):
                            errors.append(f"filter_by_duration returned {type(outside_duration)} instead of list")
                        elif len(outside_duration) != 0:
                            errors.append(f"Should find 0 songs outside duration, found {len(outside_duration)}")
                    except Exception as e:
                        errors.append(f"Error in filter_by_duration with single song: {str(e)}")
                
                # Test decade boundaries
                if check_function_exists(self.module_obj, "filter_by_decade"):
                    try:
                        within_decade = safely_call_function(self.module_obj, "filter_by_decade", single_list, 2000)
                        if within_decade is None:
                            errors.append("filter_by_decade returned None for matching decade - function may not be implemented")
                        elif not isinstance(within_decade, list):
                            errors.append(f"filter_by_decade returned {type(within_decade)} instead of list")
                        elif len(within_decade) != 1:
                            errors.append(f"Should find 1 song in decade, found {len(within_decade)}")
                        
                        outside_decade = safely_call_function(self.module_obj, "filter_by_decade", single_list, 1990)
                        if outside_decade is None:
                            errors.append("filter_by_decade returned None for non-matching decade - function may not be implemented")
                        elif not isinstance(outside_decade, list):
                            errors.append(f"filter_by_decade returned {type(outside_decade)} instead of list")
                        elif len(outside_decade) != 0:
                            errors.append(f"Should find 0 songs outside decade, found {len(outside_decade)}")
                    except Exception as e:
                        errors.append(f"Error in filter_by_decade with single song: {str(e)}")
                
                # Test named tuple conversion
                if check_function_exists(self.module_obj, "create_named_tuple_songs"):
                    try:
                        named_songs = safely_call_function(self.module_obj, "create_named_tuple_songs", single_list)
                        if named_songs is None:
                            errors.append("create_named_tuple_songs returned None - function may not be implemented")
                        elif not isinstance(named_songs, list):
                            errors.append(f"create_named_tuple_songs returned {type(named_songs)} instead of list")
                        elif len(named_songs) != 1:
                            errors.append(f"Should convert 1 song, got {len(named_songs)}")
                        # Cannot reliably check for attributes as named tuple implementation may vary
                    except Exception as e:
                        errors.append(f"Error in create_named_tuple_songs: {str(e)}")
                
                # Test empty playlist creation (should fail gracefully)
                if check_function_exists(self.module_obj, "create_playlist"):
                    try:
                        # This should fail gracefully and be caught by our testing framework
                        result = safely_call_function(self.module_obj, "create_playlist", "Empty", [], single_list)
                        if result is not None:
                            errors.append("create_playlist should not succeed with empty song IDs")
                    except Exception:
                        # Expected exception, do nothing
                        pass
                
                # Test genre distribution with single song
                if check_function_exists(self.module_obj, "calculate_genre_distribution"):
                    try:
                        distribution = safely_call_function(self.module_obj, "calculate_genre_distribution", single_list, genres)
                        if distribution is None:
                            errors.append("calculate_genre_distribution returned None - function may not be implemented")
                        elif not isinstance(distribution, dict):
                            errors.append(f"calculate_genre_distribution returned {type(distribution)} instead of dict")
                        elif len(distribution) != len(genres):
                            errors.append(f"Genre distribution should have {len(genres)} keys, has {len(distribution)}")
                        else:
                            # Check if rock genre has count 1 and others have count 0
                            if distribution.get("rock") != 1:
                                errors.append(f"Rock genre should have 1 song, has {distribution.get('rock')}")
                            other_genres = [g for g in genres if g != "rock"]
                            for genre in other_genres:
                                if distribution.get(genre) != 0:
                                    errors.append(f"{genre} genre should have 0 songs, has {distribution.get(genre)}")
                    except Exception as e:
                        errors.append(f"Error in calculate_genre_distribution: {str(e)}")
                
                # Test duration formatting
                if check_function_exists(self.module_obj, "format_duration"):
                    try:
                        formatted = safely_call_function(self.module_obj, "format_duration", 180)
                        if formatted is None:
                            errors.append("format_duration returned None - function may not be implemented")
                        elif not isinstance(formatted, str):
                            errors.append(f"format_duration returned {type(formatted)} instead of string")
                        # Don't check exact format as implementations may vary
                    except Exception as e:
                        errors.append(f"Error in format_duration: {str(e)}")
                
                # Test sorting with single song
                if check_function_exists(self.module_obj, "sort_songs"):
                    try:
                        sorted_songs = safely_call_function(self.module_obj, "sort_songs", single_list, "title")
                        if sorted_songs is None:
                            errors.append("sort_songs returned None - function may not be implemented")
                        elif not isinstance(sorted_songs, list):
                            errors.append(f"sort_songs returned {type(sorted_songs)} instead of list")
                        elif len(sorted_songs) != 1:
                            errors.append(f"Should sort 1 song, got {len(sorted_songs)}")
                    except Exception as e:
                        errors.append(f"Error in sort_songs: {str(e)}")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                    print("TestBoundaryScenarios = Failed")
                else:
                    self.test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
                    print("TestBoundaryScenarios = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
                print("TestBoundaryScenarios = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            print("TestBoundaryScenarios = Failed")

    def test_extreme_values(self):
        """Test extreme value cases"""
        try:
            errors = []
            
            # Check if module can be imported
            if self.module_obj is None:
                self.test_obj.yakshaAssert("TestExtremeValues", False, "boundary")
                print("TestExtremeValues = Failed")
                return
            
            try:
                # Get sample data
                if check_function_exists(self.module_obj, "initialize_data"):
                    try:
                        result = safely_call_function(self.module_obj, "initialize_data")
                        if result is None or not isinstance(result, tuple) or len(result) != 3:
                            errors.append("initialize_data returned invalid data")
                            # Create fallback song list for testing
                            songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                        else:
                            songs, _, _ = result
                            if not songs:
                                errors.append("initialize_data returned empty songs list")
                                # Create fallback song list for testing
                                songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                    except Exception as e:
                        errors.append(f"Error calling initialize_data: {str(e)}")
                        # Create fallback song list for testing
                        songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                else:
                    errors.append("Function initialize_data not found")
                    # Create fallback song list for testing
                    songs = [("S001", "Test Song", "Test Artist", "rock", 180, 2000, "Test Album")]
                
                # Test extremely short and long durations
                if check_function_exists(self.module_obj, "filter_by_duration"):
                    try:
                        very_short = 1
                        very_long = 100000
                        
                        short_filtered = safely_call_function(self.module_obj, "filter_by_duration", songs, very_short, very_short)
                        if short_filtered is None:
                            errors.append("filter_by_duration returned None for very short duration - function may not be implemented")
                        elif not isinstance(short_filtered, list):
                            errors.append(f"filter_by_duration returned {type(short_filtered)} instead of list")
                        
                        long_filtered = safely_call_function(self.module_obj, "filter_by_duration", songs, very_long, very_long)
                        if long_filtered is None:
                            errors.append("filter_by_duration returned None for very long duration - function may not be implemented")
                        elif not isinstance(long_filtered, list):
                            errors.append(f"filter_by_duration returned {type(long_filtered)} instead of list")
                    except Exception as e:
                        errors.append(f"Error in filter_by_duration with extreme values: {str(e)}")
                
                # Test extreme years
                if check_function_exists(self.module_obj, "filter_by_decade"):
                    try:
                        very_old = 1000
                        future = 3000
                        
                        old_songs = safely_call_function(self.module_obj, "filter_by_decade", songs, very_old)
                        if old_songs is None:
                            errors.append("filter_by_decade returned None for very old decade - function may not be implemented")
                        elif not isinstance(old_songs, list):
                            errors.append(f"filter_by_decade returned {type(old_songs)} instead of list")
                        
                        future_songs = safely_call_function(self.module_obj, "filter_by_decade", songs, future)
                        if future_songs is None:
                            errors.append("filter_by_decade returned None for future decade - function may not be implemented")
                        elif not isinstance(future_songs, list):
                            errors.append(f"filter_by_decade returned {type(future_songs)} instead of list")
                    except Exception as e:
                        errors.append(f"Error in filter_by_decade with extreme values: {str(e)}")
                
                # Test extreme duration formatting
                if check_function_exists(self.module_obj, "format_duration"):
                    try:
                        zero_duration = safely_call_function(self.module_obj, "format_duration", 0)
                        if zero_duration is None:
                            errors.append("format_duration returned None for zero duration - function may not be implemented")
                        elif not isinstance(zero_duration, str):
                            errors.append(f"format_duration returned {type(zero_duration)} instead of string")
                        
                        long_duration = safely_call_function(self.module_obj, "format_duration", 3661)  # 1 hour 1 minute 1 second
                        if long_duration is None:
                            errors.append("format_duration returned None for long duration - function may not be implemented")
                        elif not isinstance(long_duration, str):
                            errors.append(f"format_duration returned {type(long_duration)} instead of string")
                    except Exception as e:
                        errors.append(f"Error in format_duration with extreme values: {str(e)}")
                
                # Final assertion
                if errors:
                    self.test_obj.yakshaAssert("TestExtremeValues", False, "boundary")
                    print("TestExtremeValues = Failed")
                else:
                    self.test_obj.yakshaAssert("TestExtremeValues", True, "boundary")
                    print("TestExtremeValues = Passed")
            except Exception as e:
                self.test_obj.yakshaAssert("TestExtremeValues", False, "boundary")
                print("TestExtremeValues = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestExtremeValues", False, "boundary")
            print("TestExtremeValues = Failed")

if __name__ == '__main__':
    unittest.main()