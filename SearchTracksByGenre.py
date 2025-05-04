from TrackSearcher import TrackSearcher
import random


class SearchTracksByGenre(TrackSearcher):
    """Strategy for searching tracks by genre"""

    def search_tracks(self, genre, num_tracks=20):
        """Search for tracks by genre"""
        all_tracks = []
        seen_signatures = set()
        cycle = 0
        limit = 50

        while len(all_tracks) < num_tracks and cycle < 10:
            remaining_tracks = num_tracks - len(all_tracks)
            offset = cycle * limit

            tracks = self._search_tracks_by_genre(
                genre, limit=limit, offset=offset)

            if not tracks:
                break

            for track in tracks:
                signature = track.get_signature()
                if signature not in seen_signatures:
                    all_tracks.append(track)
                    seen_signatures.add(signature)

                    if len(all_tracks) >= num_tracks:
                        break

            cycle += 1

        if len(all_tracks) > num_tracks:
            return random.sample(all_tracks, num_tracks)

        return all_tracks
