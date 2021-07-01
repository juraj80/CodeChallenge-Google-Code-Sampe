"""A video player class."""

from src.video import Video
from .video_library import VideoLibrary
from .video_playlist import Playlist 
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.currentVideo = { "item": None, "status": None}                        
        self.playlists = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")


    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        list_of_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        for video in list_of_videos:
            tags=" ".join(str(tag) for tag in video.tags)
            print(video.title, f"({video.video_id})", f"[{tags}]")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
            return 

        if self.currentVideo["item"] is not None:
            print("Stopping video:", self.currentVideo["item"].title)
            self.currentVideo["status"] = "STOPPED"
            print("Playing video:",video.title)
            self.currentVideo["item"] = video
            self.currentVideo["status"] = "PLAYING"

        else:
            print("Playing video:",video.title)
            self.currentVideo["item"] = video
            self.currentVideo["status"] = "PLAYING"
       

    def stop_video(self):
        """Stops the current video."""
        if self.currentVideo["item"] is not None:
            print("Stopping video:", self.currentVideo["item"].title)
            self.currentVideo["status"] = "STOPPED"
            self.currentVideo["item"] = None
        else:
            print("Cannot stop video: No video is currently playing")


    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()
        if len(videos) == 0:
            print("No videos available")
        else:
            video = random.choice(videos)
            if self.currentVideo["item"] is not None:
                print("Stopping video:", self.currentVideo["item"].title)
                self.currentVideo["item"] = video
                print("Playing video:",video.title)
            else:
                print("Playing video:",video.title)
                self.currentVideo["item"] = video
                self.currentVideo["status"] = "PLAYING"


    def pause_video(self):
        """Pauses the current video."""
        if self.currentVideo["status"] == "PAUSED":
            print("Video already paused:", self.currentVideo["item"].title)
            return 
        if self.currentVideo["item"] is not None:
            print("Pausing video:",self.currentVideo["item"].title)
            self.currentVideo["status"] = "PAUSED"
        else:
            print("Cannot pause video: No video is currently playing")
        

    def continue_video(self):
        """Resumes playing the current video."""
        if self.currentVideo["item"] == None:
            print("Cannot continue video: No video is currently playing")

        elif self.currentVideo["status"] != "PAUSED":
            print("Cannot continue video: Video is not paused")
        
        else:
            print("Continuing video:", self.currentVideo["item"].title)
            self.currentVideo["status"] = "PLAYING"


    def show_playing(self):
        """Displays video currently playing."""
        video = self.currentVideo["item"] 
        status = self.currentVideo["status"] 
        if video is None:
            print("No video is currently playing")
        else:
            tags=" ".join(str(tag) for tag in video.tags)
            if status  == "PAUSED":
                print("Currently playing:", video.title, f"({video.video_id})", f"[{tags}] - {status}")
            else:
                print("Currently playing:", video.title, f"({video.video_id})", f"[{tags}]")


    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """       
        for p in self.playlists:
            if p.name.lower() == playlist_name.lower():
                print("Cannot create playlist: A playlist with the same name already exists")
                return
        
        playlist = Playlist(playlist_name)
        
        print("Successfully created new playlist:", playlist_name)
        self.playlists.append(playlist)
      

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """ 
        video = self._video_library.get_video(video_id)

        playlist = None 

        for p in self.playlists:
            if p.name.lower() == playlist_name.lower():
                playlist = p

        if playlist is None:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return   
        
        if video is None:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return 


        for v in playlist.videos:
            if v.video_id == video_id:
                print(f"Cannot add video to {playlist_name}: Video already added")
                return 
                
        playlist.videos.append(video)
        print(f"Added video to {playlist_name}: {video.title}")
    


    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlists)==0:
            print("No playlists exist yet")
            return 
        
        print("Showing all playlists:")
        list_of_playlists = sorted(self.playlists, key=lambda x: x.name)
        for p in list_of_playlists:
            print(p.name)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        for playlist in self.playlists:
            if playlist_name.lower() == playlist.name.lower():
                print("Showing playlist:", playlist_name)
                if len(playlist.videos)==0:
                    print("No videos here yet")
                else:
                    for video in playlist.videos:
                        tags=" ".join(str(tag) for tag in video.tags)
                        print(video.title, f"({video.video_id})", f"[{tags}]")
                return
        print(f'Cannot show playlist {playlist_name}: Playlist does not exist')   
                    


    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        playlist = None
        for p in self.playlists:
            if p.name.lower()==playlist_name.lower():
                playlist = p

        if playlist is None:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
        else:
            video = self._video_library.get_video(video_id)
            if video is None:
               print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                video_in = None
                for v in playlist.videos:
                    if v.video_id==video_id:
                        video_in = v
                if video_in is None:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
                else:
                    playlist.videos.remove(video_in)
                    print(f'Removed video from {playlist_name}: {video_in.title}')


    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = None
        for p in self.playlists:
            if p.name==playlist_name.lower():
                p.videos = []
                print(f"Successfully removed all videos from {playlist_name}")
                playlist = p
        if playlist is None:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")


    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        playlist = None
        for p in self.playlists:
            if p.name==playlist_name.lower():
                playlist = p

        if playlist is None:
            print(f'Cannot delete playlist {playlist_name}: Playlist does not exist')
        else:
            self.playlists.remove(playlist)
            print("Deleted playlist:", playlist.name)


    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        list_of_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)

        matches = []
        for video in list_of_videos:
            video_title = video.title.lower()   
            index = video_title.find(search_term.lower())
            if index > 0:
                matches.append(video)
        
        if len(matches) == 0:
            print(f'No search results for {search_term}')
        else:
            print(f'Here are the results for {search_term}:')
            i=1
            for v in matches:
                tags=" ".join(str(tag) for tag in v.tags)
                print(f'{i}) {v.title} ({v.video_id}) [{tags}]')
                i+=1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            
            try:
                user_input=int(input())
                if user_input>0 and user_input<=len(matches):
                    self.play_video(matches[user_input-1].video_id)
                    return 
            except ValueError:
                return 



    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        list_of_videos = sorted(self._video_library.get_all_videos(), key=lambda x: x.title)
        matches = []
        for video in list_of_videos:
           for tag in video.tags:
               if video_tag.lower() in tag.lower():
                   matches.append(video)
        if len(matches) == 0:
            print(f'No search results for {video_tag}')
        else:
            print(f'Here are the results for {video_tag}:')
            i=1
            for v in matches:
                tags=" ".join(str(tag) for tag in v.tags)
                print(f'{i}) {v.title} ({v.video_id}) [{tags}]')
                i+=1
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            
            try:
                user_input=int(input())
                if user_input>0 and user_input<=len(matches):
                    self.play_video(matches[user_input-1].video_id)
                    return 
            except ValueError:
                return 



    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """  
        print("flag_video needs implementation")


    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")
