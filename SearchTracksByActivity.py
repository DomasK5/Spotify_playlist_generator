from TrackSearcher import TrackSearcher
from SearchTracksByGenre import SearchTracksByGenre
from constants import ACTIVITY_GENRES
import random


class SearchTracksByActivity(TrackSearcher):
    """Strategy for searching tracks by activity"""

    def search_tracks(self, activity, num_tracks=20):
        """Search for tracks by activity"""
        if activity not in ACTIVITY_GENRES:
            print(f"Error: Activity '{activity}' not recognized")
            return []

        genres = ACTIVITY_GENRES[activity]
        all_tracks = []
        seen_signatures = set()

        base_tracks_per_genre = num_tracks // len(genres)
        remainder = num_tracks % len(genres)

        attempts = 0
        max_attempts = 3

        while len(all_tracks) < num_tracks and attempts < max_attempts:
            remaining_tracks = num_tracks - len(all_tracks)
            current_tracks_per_genre = remaining_tracks // len(genres)

            for genre in genres:
                target_tracks = current_tracks_per_genre + remainder + 10

                genre_searcher = SearchTracksByGenre(self.auth)
                tracks = genre_searcher.search_tracks(genre, target_tracks)

                for track in tracks:
                    signature = track.get_signature()
                    if signature not in seen_signatures:
                        all_tracks.append(track)
                        seen_signatures.add(signature)

                        if len(all_tracks) >= num_tracks:
                            break

                if len(all_tracks) >= num_tracks:
                    break

            attempts += 1

            if len(all_tracks) < num_tracks:
                print(f"Retrieved {len(all_tracks)} tracks, ")
                print("attempting to fetch more...")

        random.shuffle(all_tracks)

        return all_tracks[:num_tracks]
