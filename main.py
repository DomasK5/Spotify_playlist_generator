from SpotifyPlaylistGenerator import SpotifyPlaylistGenerator
from AppUI import AppUI


if __name__ == "__main__":
    generator = SpotifyPlaylistGenerator()
    app = AppUI(generator)
    app.run()
