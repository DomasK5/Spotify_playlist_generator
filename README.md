# Spotify Playlist Generator

## Introduction

### What is this application?
The Spotify Playlist Generator is a Python desktop application that creates customized Spotify playlists based on either music genres or activities. It features:
- Login with Spotify authentication
- Two playlist generation modes:
  - Generate by Genre: Create playlists for any music genre
  - Generate by Activity: Create playlists for specific activities like Workout, Study, Party, etc.
- Customizable number of tracks (10-100 songs)
- Automatic playlist creation in your Spotify account
- Modern user interface with Spotify's signature colors

### How to run the program

#### Prerequisites
1. Python 3.8 or higher
2. Required Python packages:
   ```bash
   pip install requests customtkinter
   ```

#### Configuration
1. Set up Spotify API credentials:
   - Create a Spotify Developer account at [Spotify Developer Dashboard](https://developer.spotify.com)
   - Create a new application in the dashboard
   - Copy your Client ID and Client Secret
   - Rename `secret1.template.py` to `secret1.py`
   - Add your credentials:
     ```python
     CLIENT_ID = "your_spotify_client_id"
     CLIENT_SECRET = "your_spotify_client_secret"
     REDIRECT_URI = "http://localhost:8000/callback"
     ```

#### Running the Application
```bash
python main.py
```

### How to use the program

1. **Login**
   - Launch the application
   - Click "Login with Spotify"
   - Complete authentication in your web browser

2. **Generate Playlist**
   - Choose your generation method:
     - **By Genre**: Enter any music genre (e.g., "rock", "jazz")
     - **By Activity**: Select from predefined activities (e.g., "Workout", "Study")
   - Select number of tracks (10-100)
   - Click "Generate Playlist"

3. **Create in Spotify**
   - Review the generated tracks
   - Click "Add to Spotify"
   - The playlist will appear in your Spotify library

# Implementation Analysis

## Object-Oriented Programming Pillars

### 1. Encapsulation
The `SpotifyAuth` class demonstrates proper encapsulation by protecting sensitive credentials with private attributes and controlled access through properties:

```python
class SpotifyAuth:
    def __init__(self):
        self.__client_id = ""        # Private attribute
        self.__client_secret = ""    # Private attribute
        
    @property
    def client_id(self):
        return self.__client_id
    
    @client_id.setter
    def client_id(self, value):
        self.__client_id = value
```

This ensures sensitive authentication data can only be accessed and modified through defined getter and setter methods, preventing unauthorized direct access and maintaining data integrity.

### 2. Inheritance
The track searching functionality demonstrates inheritance through an abstract base class:

```python
class TrackSearcher(ABC):
    def __init__(self, auth):
        self.auth = auth

    @abstractmethod
    def search_tracks(self, query, num_tracks=20):
        pass
```

Child classes inherit and implement the abstract method, allowing for specialized search strategies while maintaining a consistent interface. This promotes code reuse and extensibility - new search strategies can be added without modifying existing code.

### 3. Polymorphism
Different search strategies can be used interchangeably through a common interface:

```python
class SpotifyPlaylistGenerator:
    def set_strategy(self, strategy_type):
        """Set the search strategy"""
        if strategy_type == "genre":
            self.search_strategy = SearchTracksByGenre(self.auth)
        elif strategy_type == "activity":
            self.search_strategy = SearchTracksByActivity(self.auth)

    def generate_playlist(self, query, num_tracks=20, playlist_name=None):
         """Generate a playlist using the current strategy"""
         tracks = self.search_strategy.search_tracks(query, num_tracks)
```

The generator works with any search strategy that inherits from `TrackSearcher`. This demonstrates polymorphism as we can swap different search implementations at runtime while maintaining the same interface. The calling code doesn't need to know which specific strategy is being used.

### 4. Abstraction
The `TrackSearcher` class provides abstraction by defining an interface while hiding implementation details:

```python
class TrackSearcher(ABC):
    @abstractmethod
    def search_tracks(self, query, num_tracks=20):
        pass

class SearchTracksByGenre(TrackSearcher):
    def search_tracks(self, genre, num_tracks=20):
        # Complex implementation hidden from users
        tracks = self._search_tracks_by_genre(genre, num_tracks)
        return tracks
```

This abstracts away the complexity of Spotify API interactions and track searching logic. Users only need to know about the simple `search_tracks` interface, not the underlying implementation details.

## Design Pattern: Strategy Pattern
The application uses the Strategy Pattern to define interchangeable playlist generation algorithms. This pattern enables dynamic switching between different search strategies while maintaining a consistent interface. Strategy is selected through user interface.

```python
# Context
class SpotifyPlaylistGenerator:
    def __init__(self):
        self.search_strategy = None
        
    def set_strategy(self, strategy_type):
        if strategy_type == "genre":
            self.search_strategy = SearchTracksByGenre(self.auth)
        elif strategy_type == "activity":
            self.search_strategy = SearchTracksByActivity(self.auth)

# Usage
generator = SpotifyPlaylistGenerator()
generator.set_strategy("genre")
playlist = generator.generate_playlist("rock", 20)
```

## API Integration

### Authentication Flow
The application implements OAuth2 authentication with Spotify:

```python
def process_auth_code(self):
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": self.auth_code,
        "redirect_uri": self.redirect_uri
    }
    response = post(url, data=payload)
```

This handles the complex token exchange process, managing access tokens and refresh tokens automatically.

### User Profile Access
Demonstrates API integration for fetching user data:

```python
def get_user_profile(self):
    headers = {"Authorization": f"Bearer {self.access_token}"}
    response = get("https://api.spotify.com/v1/me", headers=headers)
```

### Track Search API
Complex search functionality abstracted into simple method calls:

```python
def _search_tracks_by_genre(self, genre, limit=20):
    url = "https://api.spotify.com/v1/search"
    query = f"q=genre:{genre}&type=track&limit={limit}"
    result = get(url, headers=self.auth.get_auth_header())
```

## Unit Testing

The application includes comprehensive unit tests using the unittest framework:

```python
class TestSearchTracksByActivity(unittest.TestCase):
    def setUp(self):
        self.mock_auth = Mock()
        self.searcher = SearchTracksByActivity(self.mock_auth)

    @patch('TrackSearcher.get')
    def test_valid_activity(self, mock_get):
        mock_get.return_value.content = json.dumps({
            "tracks": {"items": [{"id": "1", "name": "Test"}]}
        })
        result = self.searcher.search_tracks("Workout")
        self.assertGreater(len(result), 0)
```

These tests ensure reliability and maintainability of the codebase by verifying functionality and catching potential issues early.

# Results and Summary

## Implementation Results

* Developed a Spotify playlist generator implementing the Strategy pattern which allows switching between genre-based and activity-based playlist creation through a user interface.

* Implemented secure OAuth2 authentication with the Spotify API, effectively managing user sessions and token handling:
```python
def get_auth_header(self):
    """Return authorization header for API requests"""
    return {"Authorization": f"Bearer {self.access_token}"}
```

* Overcame Spotify API rate limiting challenges by implementing efficient batch processing for track operations:
```python
def add_tracks_to_playlist(self, playlist_id, track_uris):
    """Add tracks in batches to handle API limits"""
    for i in range(0, len(track_uris), 100):
        batch = track_uris[i:i+100]
        self._add_batch_to_playlist(playlist_id, batch)
```

* Discovered a secret Spotify API bias, which can be seen specifically when generating playlist by genre on selected genre: "hip hop". Generated playlist consists of songs mostly created by the same artist which was also hard to overcome by playing with offset settings. 

* Overcame challenge of eliminating same songs with different song ids. This made generating playlist with non-repeating songs difficult since the same song can be published as a single and in an album which gives it two different ids. This was eliminated by creating unique song signatures consisting from both the title and artist name.

* One of the functionalities was not implemented since Spotify API audio-feature endpoint was deprecated not long ago. Functionality was supposed to be in generating by genre strategy. Audio-features endpoint would have let me use different info about selected songs (like energy, danceability and more) which would have resulted in more complex and interesting generating algorithm
## Conclusions

### Key Achievements

* **Core Functionality**
  - Multiple playlist generation strategies (genre/activity)
  - Secure Spotify API integration
  - User-friendly interface
  - Code uses OOP principles

* **Technical Implementation**
  - Clean architecture using Strategy pattern
  - PEP8 compliant codebase
  - Efficient batch processing

### Project Outcomes

* Created a fully functional playlist generator that:
  - Integrates seamlessly with Spotify
  - Provides multiple generation methods
  - Handles API limitations smoothly
  - Maintains code quality and extensibility

## Future Extensions

### New Features

1. **Additional Search Strategies**
   - Mood-based playlist generation
   - Artist similarity-based playlists
   - Era/decade-based playlists
   - BPM/tempo-based playlists
  * many of points above will be implemented provided I find a replacement for audio-features endpoint.

2. **Enhanced Functionality**
   - Playlist artwork customization
   - Collaborative playlist creation
   - Social sharing capabilities
   - Playlist name and description customization

### Technical Improvements

1. **Performance Optimization**
   - Implement async/await for API calls
   - Add caching for frequent queries
   - Optimize batch processing
   - Improve error recovery

2. **User Experience**
   - Playlist analytics
   - Advanced search filters
   - Sliders in UI windows (now to use the UI it is recommended that is is open in fullscreen so that every button is visible)
