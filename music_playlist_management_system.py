"""
Music Playlist Management System
This program demonstrates tuple operations through a music playlist management system.
"""

from collections import namedtuple
from datetime import datetime

def initialize_data():
    """
    Initialize the music data with predefined songs using tuples.
    
    Returns:
        tuple: A tuple containing (songs, new_releases, genres)
    """
    # Create the initial song collection
    songs = [
        ("S001", "Bohemian Rhapsody", "Queen", "rock", 354, 1975, "A Night at the Opera"),
        ("S002", "Billie Jean", "Michael Jackson", "pop", 294, 1982, "Thriller"),
        ("S003", "Take Five", "Dave Brubeck", "jazz", 324, 1959, "Time Out"),
        ("S004", "Moonlight Sonata", "Ludwig van Beethoven", "classical", 363, 1801, "Piano Sonatas"),
        ("S005", "Strobe", "Deadmau5", "electronic", 601, 2009, "For Lack of a Better Name")
    ]
    
    # Create the new releases list
    new_releases = [
        ("N001", "Blinding Lights", "The Weeknd", "pop", 200, 2020, "After Hours"),
        ("N002", "Bamboo", "J Balvin", "hip-hop", 190, 2023, "Colores")
    ]
    
    # Define valid genres
    genres = ("rock", "pop", "jazz", "classical", "electronic", "hip-hop")
    
    return songs, new_releases, genres

def create_song_record(id, title, artist, genre, duration, release_year, album):
    """
    Create an immutable song record as a tuple.
    
    Args:
        id (str): Unique identifier for the song
        title (str): Song title
        artist (str): Artist name
        genre (str): Music genre
        duration (int): Duration in seconds
        release_year (int): Year the song was released
        album (str): Album name
    
    Returns:
        tuple: A tuple containing all song information
    """
    if not isinstance(id, str) or not id:
        raise ValueError("Song ID must be a non-empty string")
    if not isinstance(title, str) or not title:
        raise ValueError("Title must be a non-empty string")
    if not isinstance(artist, str) or not artist:
        raise ValueError("Artist must be a non-empty string")
    if not isinstance(genre, str) or not genre:
        raise ValueError("Genre must be a non-empty string")
    if not isinstance(duration, int) or duration <= 0:
        raise ValueError("Duration must be a positive integer in seconds")
    if not isinstance(release_year, int):
        raise ValueError("Release year must be an integer")
    if not isinstance(album, str) or not album:
        raise ValueError("Album must be a non-empty string")
    
    # Create and return a tuple with song data
    song = (id, title, artist, genre, duration, release_year, album)
    return song

def filter_by_genre(songs, genre):
    """Filter songs by genre"""
    if not isinstance(genre, str) or not genre:
        raise ValueError("Genre must be a non-empty string")
    return [song for song in songs if song[3] == genre]

def filter_by_artist(songs, artist):
    """Filter songs by artist"""
    if not isinstance(artist, str) or not artist:
        raise ValueError("Artist must be a non-empty string") 
    return [song for song in songs if song[2] == artist]

def filter_by_duration(songs, min_duration, max_duration):
    """Filter songs by duration range"""
    if not isinstance(min_duration, int) or min_duration < 0:
        raise ValueError("Min duration must be a non-negative integer")
    if not isinstance(max_duration, int) or max_duration <= 0:
        raise ValueError("Max duration must be a positive integer")
    if min_duration > max_duration:
        raise ValueError("Min duration must be less than max duration")
    return [song for song in songs if min_duration <= song[4] <= max_duration]

def filter_by_decade(songs, decade):
    """Filter songs by release decade"""
    if not isinstance(decade, int):
        raise ValueError("Decade must be an integer")
    decade_start = decade
    decade_end = decade + 9
    return [song for song in songs if decade_start <= song[5] <= decade_end]

def format_duration(seconds):
    """
    Format duration from seconds to MM:SS.
    
    Args:
        seconds (int): Duration in seconds
    
    Returns:
        str: Formatted duration string
    """
    if not isinstance(seconds, int) or seconds < 0:
        raise ValueError("Seconds must be a non-negative integer")
    
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    formatted_duration = f"{minutes}:{remaining_seconds:02d}"
    return formatted_duration

def create_named_tuple_songs(songs):
    """
    Convert regular tuple songs to named tuples for improved readability.
    
    Args:
        songs (list): List of song tuples
    
    Returns:
        list: List of named tuple instances
    """
    if not songs:
        raise ValueError("Songs list cannot be empty")
    
    # Create a named tuple type
    Song = namedtuple('Song', ['id', 'title', 'artist', 'genre', 'duration', 'release_year', 'album'])
    
    # Convert each tuple to a named tuple
    named_songs = [Song(*song) for song in songs]
    return named_songs

def create_playlist(name, song_ids, songs):
    """
    Create an immutable playlist record with name, date, and song IDs.
    
    Args:
        name (str): Playlist name
        song_ids (list): List of song IDs to include
        songs (list): List of all available songs
    
    Returns:
        tuple: A tuple containing playlist information
    """
    if not isinstance(name, str) or not name:
        raise ValueError("Playlist name must be a non-empty string")
    if not song_ids:
        raise ValueError("Song IDs list cannot be empty")
    if not songs:
        raise ValueError("Songs list cannot be empty")
    
    # Verify all song IDs exist in the songs list
    all_ids = [song[0] for song in songs]
    invalid_ids = [id for id in song_ids if id not in all_ids]
    if invalid_ids:
        raise ValueError(f"Invalid song IDs: {', '.join(invalid_ids)}")
    
    # Get current date in YYYY-MM-DD format
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Create an immutable playlist tuple with name, date, and song IDs
    playlist = (name, current_date, tuple(song_ids))
    return playlist

def sort_songs(songs, sort_key):
    """
    Sort songs by specified attribute using tuple comparison.
    
    Args:
        songs (list): List of song tuples
        sort_key (str): Attribute to sort by ("title", "artist", "year", "duration")
    
    Returns:
        list: Sorted list of song tuples
    """
    if not songs:
        raise ValueError("Songs list cannot be empty")
    if not isinstance(sort_key, str) or not sort_key:
        raise ValueError("Sort key must be a non-empty string")
    
    # Define sorting keys based on tuple indices
    sort_keys = {
        "title": lambda x: x[1],  # Sort by title
        "artist": lambda x: x[2],  # Sort by artist
        "year": lambda x: x[5],   # Sort by release year
        "duration": lambda x: x[4],  # Sort by duration
        "genre": lambda x: x[3],  # Sort by genre
        "artist_year": lambda x: (x[2], x[5])  # Sort by artist then year
    }
    
    if sort_key not in sort_keys:
        raise ValueError(f"Invalid sort key. Must be one of {list(sort_keys.keys())}")
    
    # Sort using the appropriate key function
    sorted_songs = sorted(songs, key=sort_keys[sort_key])
    return sorted_songs

def calculate_genre_distribution(songs, genres):
    """
    Calculate the distribution of songs by genre.
    
    Args:
        songs (list): List of song tuples
        genres (tuple): Tuple of valid genres
    
    Returns:
        dict: Dictionary with genre counts
    """
    if not songs:
        raise ValueError("Songs list cannot be empty")
    if not genres:
        raise ValueError("Genres tuple cannot be empty")
    
    # Count songs in each genre using dictionary comprehension
    genre_counts = {genre: len([s for s in songs if s[3] == genre]) for genre in genres}
    return genre_counts

def integrate_new_releases(songs, new_releases):
    """
    Integrate new releases into the main song list.
    
    Args:
        songs (list): List of existing song tuples
        new_releases (list): List of new release tuples
    
    Returns:
        list: Combined list of songs
    """
    if not isinstance(songs, list):
        raise ValueError("Songs must be a list")
    if not isinstance(new_releases, list):
        raise ValueError("New releases must be a list")
    
    # Simply combine the lists
    combined_songs = songs + new_releases
    return combined_songs

def get_formatted_song(song):
    """
    Format a song tuple for display.
    
    Args:
        song (tuple): Song tuple to format
    
    Returns:
        str: Formatted song string
    """
    if not isinstance(song, tuple) or len(song) < 7:
        raise ValueError("Song must be a tuple with at least 7 elements")
    
    # Unpack the song tuple for readability
    song_id, title, artist, genre, duration, year, album = song
    
    # Format the duration from seconds to MM:SS
    formatted_duration = format_duration(duration)
    
    # Return a formatted string with all song information
    return f"{song_id} | {title} | {artist} | {genre} | {formatted_duration} | {year} | {album}"

def get_playlist_info(playlist, songs):
    """
    Format a playlist tuple for display.
    
    Args:
        playlist (tuple): Playlist tuple
        songs (list): List of song tuples
    
    Returns:
        str: Formatted playlist information
    """
    if not isinstance(playlist, tuple) or len(playlist) < 3:
        raise ValueError("Playlist must be a tuple with at least 3 elements")
    if not songs:
        raise ValueError("Songs list cannot be empty")
    
    # Unpack the playlist tuple
    name, created_date, song_ids = playlist
    
    # Create a lookup dictionary for songs by ID
    song_lookup = {song[0]: song for song in songs}
    
    # Count songs and calculate total duration
    total_duration = sum(song_lookup[song_id][4] for song_id in song_ids if song_id in song_lookup)
    
    # Format the output
    playlist_info = [
        f"Name: {name}",
        f"Created: {created_date}",
        f"Songs: {len(song_ids)}",
        f"Duration: {format_duration(total_duration)}",
        "Tracks:"
    ]
    
    # Add track information
    for i, song_id in enumerate(song_ids, 1):
        if song_id in song_lookup:
            song = song_lookup[song_id]
            playlist_info.append(f"  {i}. {song[1]} - {song[2]} ({format_duration(song[4])})")
    
    return "\n".join(playlist_info)

def calculate_total_duration(songs):
    """
    Calculate the total duration of all songs.
    
    Args:
        songs (list): List of song tuples
    
    Returns:
        tuple: A tuple containing (hours, minutes, seconds)
    """
    if not songs:
        raise ValueError("Songs list cannot be empty")
    
    # Calculate total seconds
    total_seconds = sum(song[4] for song in songs)
    
    # Convert to hours, minutes, seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return (hours, minutes, seconds)

def display_data(data, data_type="songs"):
    """
    Display formatted song data or statistics.
    
    Args:
        data: Data to display (can be list of songs, playlist, or statistics)
        data_type (str): Type of data to display
    """
    if data is None:
        raise ValueError("Data cannot be None")
    
    if data_type == "songs" or data_type == "results":
        header = "\nCurrent Song Collection:" if data_type == "songs" else "\nFiltered Results:"
        print(header)
        
        if not data:
            print("No songs to display.")
            return
            
        for song in data:
            print(get_formatted_song(song))
            
    elif data_type == "playlist":
        print("\nPlaylist Information:")
        print(data)  # Already formatted by get_playlist_info
            
    elif data_type == "distribution":
        print("\nSong Distribution:")
        for genre, count in data.items():
            print(f"{genre}: {count} songs")
            
    elif data_type == "named_songs":
        print("\nNamed Tuple Songs:")
        if not data:
            print("No songs to display.")
            return
            
        for song in data:
            duration = format_duration(song.duration)
            print(f"{song.id} | {song.title} | {song.artist} | {song.genre} | {duration} | {song.release_year} | {song.album}")
            
    else:
        print(f"\nUnknown data type: {data_type}")
        print(data)

def main():
    """Main program function."""
    # Initialize data
    songs, new_releases, genres = initialize_data()
    playlists = []  # List to store created playlists
    
    while True:
        # Calculate basic statistics
        total_songs = len(songs)
        total_hours, total_minutes, total_seconds = calculate_total_duration(songs)
        
        # Display header and statistics
        print(f"\n===== MUSIC PLAYLIST MANAGEMENT SYSTEM =====")
        print(f"Total Songs: {total_songs}")
        print(f"Total Duration: {total_hours}h {total_minutes}m {total_seconds}s")
        
        # Display menu
        print("\n1. View Songs")
        print("2. Filter Songs")
        print("3. Create Playlist")
        print("4. Convert to Named Tuples")
        print("5. Calculate Statistics")
        print("6. Integrate New Releases")
        print("0. Exit")
        
        choice = input("Enter your choice (0-6): ")
        
        if choice == "0":
            print("Thank you for using the Music Playlist Management System!")
            break
            
        elif choice == "1":
            display_data(songs, "songs")
        
        elif choice == "2":
            print("\n1. Filter by Genre")
            print("2. Filter by Artist")
            print("3. Filter by Duration Range")
            print("4. Filter by Decade")
            filter_choice = input("Select filter option (1-4): ")
            
            try:
                if filter_choice == "1":
                    print(f"Available genres: {', '.join(genres)}")
                    genre = input("Enter genre to filter by: ")
                    if genre not in genres:
                        print(f"Invalid genre. Must be one of {genres}")
                        continue
                    filtered_songs = filter_by_genre(songs, genre)
                    display_data(filtered_songs, "results")
                    
                elif filter_choice == "2":
                    artist = input("Enter artist to filter by: ")
                    filtered_songs = filter_by_artist(songs, artist)
                    display_data(filtered_songs, "results")
                    
                elif filter_choice == "3":
                    min_min = int(input("Enter minimum duration (minutes): "))
                    min_sec = int(input("Enter minimum duration (seconds): "))
                    max_min = int(input("Enter maximum duration (minutes): "))
                    max_sec = int(input("Enter maximum duration (seconds): "))
                    
                    min_duration = min_min * 60 + min_sec
                    max_duration = max_min * 60 + max_sec
                    
                    filtered_songs = filter_by_duration(songs, min_duration, max_duration)
                    display_data(filtered_songs, "results")
                    
                elif filter_choice == "4":
                    decade = int(input("Enter decade (e.g., 1970 for the 1970s): "))
                    decade_songs = filter_by_decade(songs, decade)
                    display_data(decade_songs, "results")
                    
                else:
                    print("Invalid choice.")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            try:
                # Display available songs for selection
                print("\nAvailable Songs:")
                for i, song in enumerate(songs, 1):
                    print(f"{i}. {song[0]} - {song[1]} by {song[2]}")
                
                # Get playlist information
                name = input("\nEnter playlist name: ")
                
                # Get song selections
                selections = input("Enter song numbers to add (comma-separated): ")
                indices = [int(idx.strip()) - 1 for idx in selections.split(",")]
                
                # Validate indices
                if any(idx < 0 or idx >= len(songs) for idx in indices):
                    print("Invalid song number.")
                    continue
                
                # Get song IDs from selected indices
                song_ids = [songs[idx][0] for idx in indices]
                
                # Create the playlist
                playlist = create_playlist(name, song_ids, songs)
                playlists.append(playlist)
                
                # Display the playlist
                playlist_info = get_playlist_info(playlist, songs)
                display_data(playlist_info, "playlist")
                
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            try:
                # Convert to named tuples
                named_songs = create_named_tuple_songs(songs)
                display_data(named_songs, "named_songs")
                
                # Demonstrate how to access named tuple fields
                if named_songs:
                    sample_song = named_songs[0]
                    print("\nAccessing Named Tuple Fields:")
                    print(f"ID: {sample_song.id}")
                    print(f"Title: {sample_song.title}")
                    print(f"Artist: {sample_song.artist}")
                    print(f"Genre: {sample_song.genre}")
                    print(f"Duration: {format_duration(sample_song.duration)}")
                    print(f"Year: {sample_song.release_year}")
                    print(f"Album: {sample_song.album}")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "5":
            print("\n1. Genre Distribution")
            print("2. Sort Songs")
            print("3. Artist Statistics")
            stats_choice = input("Select statistics option (1-3): ")
            
            try:
                if stats_choice == "1":
                    # Calculate and display genre distribution
                    genre_counts = calculate_genre_distribution(songs, genres)
                    display_data(genre_counts, "distribution")
                    
                elif stats_choice == "2":
                    # Sort and display songs
                    print("\nSort by: title, artist, year, duration, genre, artist_year")
                    sort_key = input("Enter sort key: ")
                    sorted_songs = sort_songs(songs, sort_key)
                    display_data(sorted_songs, "results")
                    
                elif stats_choice == "3":
                    # Create a dictionary with artist as key and song count as value
                    # Using tuples as dictionary keys (artist name)
                    artist_counts = {}
                    for song in songs:
                        artist = song[2]
                        if artist not in artist_counts:
                            artist_counts[artist] = 0
                        artist_counts[artist] += 1
                    
                    # Display artist statistics
                    print("\nArtist Statistics:")
                    for artist, count in artist_counts.items():
                        # Find an example song from this artist using tuple operations
                        example_song = next((s for s in songs if s[2] == artist), None)
                        if example_song:
                            print(f"{artist}: {count} songs (e.g., {example_song[1]})")
                        else:
                            print(f"{artist}: {count} songs")
                    
                else:
                    print("Invalid choice.")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "6":
            try:
                # Show current songs and new releases
                print("\nCurrent Songs:")
                for song in songs:
                    print(f"- {song[0]}: {song[1]} by {song[2]}")
                
                print("\nNew Releases:")
                for song in new_releases:
                    print(f"- {song[0]}: {song[1]} by {song[2]}")
                
                # Confirm integration
                confirm = input("\nIntegrate new releases? (y/n): ")
                if confirm.lower() == 'y':
                    songs = integrate_new_releases(songs, new_releases)
                    print(f"Integration complete. New total: {len(songs)} songs.")
                else:
                    print("Integration cancelled.")
            except ValueError as e:
                print(f"Error: {e}")
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()