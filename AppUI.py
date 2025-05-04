from SearchTracksByActivity import SearchTracksByActivity
from constants import SPOTIFY_GREEN, SPOTIFY_BLACK, ACTIVITY_GENRES
import webbrowser
import customtkinter as ctk
import threading


class AppUI:
    """Class for the application UI"""

    def __init__(self, generator):
        self.generator = generator
        self.activities = list(ACTIVITY_GENRES.keys())
        self.playlist_url = None

        self.root = ctk.CTk()
        self.root.title("Spotify Playlist Generator")
        self.root.geometry("600x400")
        self.root.configure(fg_color=SPOTIFY_BLACK)

        self.main_frame = ctk.CTkFrame(self.root, fg_color=SPOTIFY_BLACK)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.create_login_screen()

    def create_login_screen(self):
        """Create the login screen UI"""

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        logo_label = ctk.CTkLabel(
            self.main_frame,
            text="Spotify Playlist Generator",
            font=("Helvetica", 24, "bold"),
            text_color=SPOTIFY_GREEN
        )
        logo_label.pack(pady=40)

        login_button = ctk.CTkButton(
            self.main_frame,
            text="Login with Spotify",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=self.login_with_spotify
        )
        login_button.pack(pady=20)

    def login_with_spotify(self):
        """Handle Spotify login"""

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        loading_label = ctk.CTkLabel(
            self.main_frame,
            text="Connecting to Spotify...\nPlease complete authentication in your browser.",
            font=("Helvetica", 16),
            text_color=SPOTIFY_GREEN
        )
        loading_label.pack(pady=40)

        auth_thread = threading.Thread(target=self.perform_auth)
        auth_thread.daemon = True
        auth_thread.start()

    def perform_auth(self):
        """Perform authentication in a separate thread"""

        self.generator.auth.open_auth_page()

        auth_completed = self.generator.auth.wait_for_auth_completion(timeout=120)

        if auth_completed:
            self.root.after(100, self.auth_success)
        else:
            self.root.after(100, self.auth_timeout)

    def auth_success(self):
        """Handle successful authentication"""

        if self.generator.auth.access_token and self.generator.auth.user_id:

            for widget in self.main_frame.winfo_children():
                widget.destroy()

            success_label = ctk.CTkLabel(
                self.main_frame,
                text="Authentication successful!",
                font=("Helvetica", 16),
                text_color=SPOTIFY_GREEN
            )
            success_label.pack(pady=20)

            self.root.after(1500, self.create_main_menu)
        else:
            self.auth_failed()

    def auth_timeout(self):
        """Handle authentication timeout"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        timeout_label = ctk.CTkLabel(
            self.main_frame,
            text="Authentication timed out. Please try again.",
            font=("Helvetica", 16),
            text_color="red"
        )
        timeout_label.pack(pady=40)

        retry_button = ctk.CTkButton(
            self.main_frame,
            text="Try Again",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=self.create_login_screen
        )
        retry_button.pack(pady=20)

    def auth_failed(self):
        """Handle authentication failure"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        error_label = ctk.CTkLabel(
            self.main_frame,
            text="Authentication failed. Please try again.",
            font=("Helvetica", 16),
            text_color="red"
        )
        error_label.pack(pady=40)

        retry_button = ctk.CTkButton(
            self.main_frame,
            text="Try Again",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=self.create_login_screen
        )
        retry_button.pack(pady=20)

    def auth_callback(self):
        """Callback function for when auth is complete"""
        self.root.after(100, self.handle_auth_completion)

    def handle_auth_completion(self):
        """Handle the completion of the authorization process"""
        if self.generator.auth.access_token and self.generator.auth.user_id:

            self.create_main_menu()
        else:
            for widget in self.main_frame.winfo_children():
                widget.destroy()

            error_label = ctk.CTkLabel(
                self.main_frame,
                text="Spotify authentication failed. Please try again.",
                font=("Helvetica", 14),
                text_color="red"
            )
            error_label.pack(pady=40)

            retry_button = ctk.CTkButton(
                self.main_frame,
                text="Retry Login",
                font=("Helvetica", 16),
                fg_color=SPOTIFY_GREEN,
                hover_color="#1aa34a",
                command=self.create_login_screen
            )
            retry_button.pack(pady=20)

    def create_main_menu(self):
        """Create the main menu UI"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        heading = ctk.CTkLabel(
            self.main_frame,
            text="How would you like to generate your playlist?",
            font=("Helvetica", 18, "bold"),
            text_color=SPOTIFY_GREEN
        )
        heading.pack(pady=30)

        genre_button = ctk.CTkButton(
            self.main_frame,
            text="Generate by Genre",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=lambda: self.show_genre_selection()
        )
        genre_button.pack(pady=10)

        activity_button = ctk.CTkButton(
            self.main_frame,
            text="Generate by Activity",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=lambda: self.show_activity_selection()
        )
        activity_button.pack(pady=10)

    def show_genre_selection(self):
        """Show the genre selection UI"""
        self.generator.set_strategy("genre")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        heading = ctk.CTkLabel(
            self.main_frame,
            text="Enter a genre",
            font=("Helvetica", 18, "bold"),
            text_color=SPOTIFY_GREEN
        )
        heading.pack(pady=20)

        genre_label = ctk.CTkLabel(
            self.main_frame,
            text="Genre:",
            font=("Helvetica", 14)
        )
        genre_label.pack(pady=(20, 5))

        genre_entry = ctk.CTkEntry(
            self.main_frame,
            width=300,
            font=("Helvetica", 14)
        )
        genre_entry.pack(pady=(0, 10))

        track_label = ctk.CTkLabel(
            self.main_frame,
            text="Number of tracks:",
            font=("Helvetica", 14)
        )
        track_label.pack(pady=(10, 5))

        track_count = ctk.CTkSlider(
            self.main_frame,
            from_=10,
            to=100,
            number_of_steps=9
        )
        track_count.set(50)
        track_count.pack(pady=(0, 5))

        track_count_label = ctk.CTkLabel(
            self.main_frame,
            text="50 tracks"
        )
        track_count_label.pack(pady=(0, 10))

        def update_track_label(value):
            track_count_label.configure(text=f"{int(value)} tracks")

        track_count.configure(command=update_track_label)

        generate_button = ctk.CTkButton(
            self.main_frame,
            text="Generate Playlist",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=lambda: self.generate_playlist(
                genre_entry.get(), int(track_count.get()))
        )
        generate_button.pack(pady=20)

        back_button = ctk.CTkButton(
            self.main_frame,
            text="Back",
            font=("Helvetica", 12),
            fg_color="#555555",
            hover_color="#444444",
            command=self.create_main_menu
        )
        back_button.pack(pady=10)

    def show_activity_selection(self):
        """Show the activity selection UI"""
        self.generator.set_strategy("activity")

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        heading = ctk.CTkLabel(
            self.main_frame,
            text="Select an activity",
            font=("Helvetica", 18, "bold"),
            text_color=SPOTIFY_GREEN
        )
        heading.pack(pady=20)

        activity_frame = ctk.CTkFrame(self.main_frame, fg_color=SPOTIFY_BLACK)
        activity_frame.pack(pady=10, fill="both", expand=True)

        selected_activity = ctk.StringVar()
        selected_activity.set(self.activities[0])

        for activity in self.activities:
            activity_radio = ctk.CTkRadioButton(
                activity_frame,
                text=activity,
                variable=selected_activity,
                value=activity,
                font=("Helvetica", 14),
                fg_color=SPOTIFY_GREEN,
                hover_color="#1aa34a"
            )
            activity_radio.pack(anchor="w", padx=20, pady=5)

        track_label = ctk.CTkLabel(
            self.main_frame,
            text="Number of tracks:",
            font=("Helvetica", 14)
        )
        track_label.pack(pady=(10, 5))

        track_count = ctk.CTkSlider(
            self.main_frame,
            from_=10,
            to=100,
            number_of_steps=9
        )
        track_count.set(50)
        track_count.pack(pady=(0, 5))

        track_count_label = ctk.CTkLabel(
            self.main_frame,
            text="50 tracks"
        )
        track_count_label.pack(pady=(0, 10))

        def update_track_label(value):
            track_count_label.configure(text=f"{int(value)} tracks")

        track_count.configure(command=update_track_label)

        generate_button = ctk.CTkButton(
            self.main_frame,
            text="Generate Playlist",
            font=("Helvetica", 16),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=lambda: self.generate_playlist(
                selected_activity.get(), int(track_count.get()))
        )
        generate_button.pack(pady=20)

        back_button = ctk.CTkButton(
            self.main_frame,
            text="Back",
            font=("Helvetica", 12),
            fg_color="#555555",
            hover_color="#444444",
            command=self.create_main_menu
        )
        back_button.pack(pady=10)

    def generate_playlist(self, query, num_tracks):
        """Generate the playlist and show results"""
        playlist = self.generator.generate_playlist(query, num_tracks)

        self.show_playlist_results(playlist, query)

    def show_playlist_results(self, playlist, query):
        """Show the playlist results UI"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        heading = ctk.CTkLabel(
            self.main_frame,
            text=f"Playlist: {query}",
            font=("Helvetica", 18, "bold"),
            text_color=SPOTIFY_GREEN
        )
        heading.pack(pady=(20, 10))

        tracks_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=500,
            height=200,
            fg_color="#333333"
        )
        tracks_frame.pack(pady=10, padx=20, fill="both", expand=True)

        for i, track in enumerate(playlist.tracks):
            track_label = ctk.CTkLabel(
                tracks_frame,
                text=f"{i+1}. {track}",
                font=("Helvetica", 12),
                anchor="w"
            )
            track_label.pack(pady=2, padx=10, anchor="w", fill="x")

        button_frame = ctk.CTkFrame(self.main_frame, fg_color=SPOTIFY_BLACK)
        button_frame.pack(pady=20, fill="x")

        add_button = ctk.CTkButton(
            button_frame,
            text="Add to Spotify",
            font=("Helvetica", 14),
            fg_color=SPOTIFY_GREEN,
            hover_color="#1aa34a",
            command=self.add_to_spotify
        )
        add_button.pack(side="left", padx=10, expand=True)

        new_button = ctk.CTkButton(
            button_frame,
            text="Generate New Playlist",
            font=("Helvetica", 14),
            fg_color="#555555",
            hover_color="#444444",
            command=self.create_main_menu
        )
        new_button.pack(side="right", padx=10, expand=True)

    def add_to_spotify(self):
        """Add the playlist to Spotify"""
        if not self.generator.auth.access_token or not self.generator.auth.user_id:
            auth_message = ctk.CTkLabel(
                self.main_frame,
                text="Authentication required. Please restart the app.",
                font=("Helvetica", 12),
                text_color="red"
            )
            auth_message.pack(pady=10)
            return

        loading_label = ctk.CTkLabel(
            self.main_frame,
            text="Creating playlist in Spotify...",
            font=("Helvetica", 12),
            text_color=SPOTIFY_GREEN
        )
        loading_label.pack(pady=10)

        def create_playlist_thread():
            playlist_id = self.generator.create_spotify_playlist(
                self.generator.auth.user_id,
                self.generator.auth.access_token
            )

            self.root.after(100, lambda: self.playlist_created(
                playlist_id, loading_label))

        thread = threading.Thread(target=create_playlist_thread)
        thread.daemon = True
        thread.start()

    def playlist_created(self, playlist_id, loading_label):
        """Handle playlist creation completion"""
        loading_label.destroy()

        if playlist_id:
            success_label = ctk.CTkLabel(
                self.main_frame,
                text="Playlist created successfully!",
                font=("Helvetica", 12),
                text_color=SPOTIFY_GREEN
            )
            success_label.pack(pady=10)

            playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"

            view_button = ctk.CTkButton(
                self.main_frame,
                text="View in Spotify",
                font=("Helvetica", 14),
                fg_color=SPOTIFY_GREEN,
                hover_color="#1aa34a",
                command=lambda: webbrowser.open(playlist_url)
            )
            view_button.pack(pady=10)
        else:
            error_label = ctk.CTkLabel(
                self.main_frame,
                text="Failed to create playlist. Please try again.",
                font=("Helvetica", 12),
                text_color="red"
            )
            error_label.pack(pady=10)

    def run(self):
        """Run the application"""
        self.root.mainloop()
