#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

"""
Kodi remote controller in command lines based on (cmd). Integrated with
the echonest API for smart playlists generation.
More info on the echonest API: http://developer.echonest.com/docs/v4
"""

import pykodi as pk
import pykodi.display as pkd

import cmd
import logging
import random
import argparse
import pickle

# global constants

DISPLAY_NB_LINES = 10

logger = logging.getLogger(__name__)

# simple utility functions

def display_banner():
    """Display initial banner"""
    logger.debug('call function display_banner')
    print
    print "No Kodi params file found, this is probably the first launch. Check"
    print "your Kodi parameters (IP, port, user and password) and create an"
    print "Echonest account: https://developer.echonest.com/account/register"
    print
    print "Read the API key on the Echonest account, it will be requested"
    print "later on. When you are ready, try params_create."

def set_friendly_name(self):
    """Set Kodi friendly name in the cmd prompt"""
    logger.debug('call function set_friendly_name')
    friendly_name = pk.get_friendly_name(self.params)
    self.prompt = "(" + friendly_name + ") "

# params utility functions

def params_display(params):
    """Fancy display of PyKodi params"""
    print
    print "Kodi parameters:"
    print "   Network:        {}/{}".format(
        params['ip'],
        params['port']
    )
    print "   Credential:     {} ({})".format(
        params['user'],
        params['password']
    )
    print
    print "Echonest API key:  {}".format(params['echonest_key'])

def params_get():
    """Get the run parameters"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity",
            action="count",
            help='Increase output verbosity')
    args = parser.parse_args()
    if args.verbosity == 2:
        logging.basicConfig(level=logging.DEBUG)
    else:
        if args.verbosity == 1:
            logging.basicConfig(level=logging.INFO)
        else:
            args.verbosity = 0
    logger.info('Kodi controller started in verbosity mode ...')
    logger.debug('... and even in high verbosity mode!')
    return args.verbosity

def params_inputs():
    """Request the user for params input"""
    logger.debug('call function input_params')
    params = {}
    params['ip'] = raw_input("Kodi server IP: ")
    params['port'] = raw_input("Kodi server port: ")
    params['user'] = raw_input("Kodi server user: ")
    params['password'] = raw_input("Kodi server password: ")
    params['echonest_key'] = raw_input("Echonest developer key: ")
    return params

def params_read():
    """Read the Kodi params from the local file"""
    logger.debug('call function read_params')
    f = open('params.pickle', 'rb')
    params = pickle.load(f)
    f.close()
    return params

def params_save(params):
    """Save the Kodi parameters to a local file"""
    logger.debug('call function save_params')
    f = open('params.pickle', 'wb')
    pickle.dump(params, f)
    f.close()


class KodiRemote(cmd.Cmd):
    
    def preloop(self):
        self.log_level = params_get()
        if not pk.is_file('params.pickle'):
            logger.info('no kodi params file')
            display_banner()
            print
            return
        logger.debug('kodi params file found')
        self.params = params_read()
        set_friendly_name(self)
        if not pk.is_local_albums():
            self.albums = {}
            self.genres = {}
        else:
            self.albums = pk.albums_read_from_file()
            self.genres = pk.genres_read_from_file()
        if not pk.is_local_songs():
            self.songs = {}
        else:
            self.songs = pk.songs_read_from_file()

    # albums functions

    def do_albums_display(self, line):
        """
        Display details for a given album
        Usage: albums_display id
            Display all information about a given album like the artist
            or the release year.
        """
        logger.debug('call function do_albums_display')
        albumid = int(line)
        pkd.albums_details(albumid, self.albums)
        print

    def do_albums_page(self, line):
        """
        Display a given page of the albums library
        Usage: albums_page page
        """
        logger.debug('call function do_albums_page')
        page = int(line)
        albumids = self.albums.keys()[(page - 1) * DISPLAY_NB_LINES:page * DISPLAY_NB_LINES]
        pkd.albums_index(albumids, self.albums)
        print

    def do_albums_random(self, line):
        """
        Display a set of random albums
        Usage: albums_random
            Select random albums and display them.
        """
        logger.debug('call function do_albums_random')
        indexes = random.sample(xrange(len(self.albums)), DISPLAY_NB_LINES)
        albumids = [self.albums.keys()[index] for index in indexes]
        pkd.albums_index(albumids, self.albums)
        print

    def do_albums_recent(self, line):
        """
        Display recently added albums
        Usage: albums_recent
        """
        logger.debug('call function do_albums_recent')
        albumids = self.albums.keys()[-1 * DISPLAY_NB_LINES:]
        pkd.albums_index(albumids, self.albums)
        print

    def do_albums_search(self, line):
        """
        Search into the albums
        Usage: songs_search string
            List all albums containing the string in the title or artist.
        """
        logger.debug('call function do_albums_search')
        search_string = line.lower()
        albumids = pk.albums_search(self.albums, search_string)
        pkd.albums_index(albumids, self.albums)
        print

    def do_albums_sync(self, line):
        """
        Sync the Kodi albums library.
        Usage: album_sync
        """
        print
        pk.albums_sync(self.params, self.albums, self.log_level == 0)
        pk.genres_extract(self.albums, self.genres)
        print

    # genres function

    def do_genres_info(self, line):
        """
        Display information on the genres
        Usage: genres_info
        """
        logger.debug('call function do_genres_info')
        pkd.genres_info(self.genres)
        print

    def do_genres_search(self, line):
        """
        Search into the genres
        Usage: genres_search string
            List all genres containing the string in the description.
        """
        logger.debug('call function do_genres_search')
        search_string = line.lower()
        genreids = pk.genres_search(self.genres, search_string)
        pkd.genres_index(genreids, self.genres)
        print

    # echonest functions

    def do_echonest_delete(self, line):
        """
        Delete echonest taste profile.
        Usage: echonest_delete
            All information stored in the profile will be lost.
        """
        logger.debug('call function do_echonest_delete')
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        if pkd.en_sure_delete_tasteprofile(self.params['echonest_key'], profile_id):
            pk.en_delete(self.params['echonest_key'], profile_id)
            pkd.en_delete()
        print

    def do_echonest_display(self, line):
        """
        Display song details in tasteprofile
        Usage: echonest_display id
        """
        logger.debug('call function do_echonest_display')
        songid = int(line)
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        song_data = pk.en_display(self.params['echonest_key'], profile_id, songid)
        pkd.en_display(song_data)
        print

    def do_echonest_info(self, line):
        """
        Display info about the echonest taste profile.
        Usage: en_info
        """
        logger.debug('call function do_echonest_info')
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        en_info = pk.en_info(self.params['echonest_key'], profile_id)
        pkd.en_info(en_info)
        print

    def do_echonest_status(self, line):
        """
        Check the status of a tasteprofile update
        Usage: en_status ticket
            Detail status of the update tickets.
        """
        logger.debug('call function do_echonest_sync')
        ticket = line
        pk.en_status(self.params['echonest_key'], ticket)

    def do_echonest_sync(self, line):
        """
        Sync local songs with the echonest tasteprofile
        Usage: echonest_sync
            If there is no song in the profile, a full sync is
            performed. Otherwise, only the play counts and the
            ratings are updated.
        """
        logger.debug('call function do_echonest_sync')
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        print
        en_songids = pk.en_sync(self.params['echonest_key'], profile_id, self.songs, self.log_level == 0)
        pkd.en_sync(en_songids)
        print

    # Kodi params file

    def do_params_create(self, line):
        """
        Create the Kodi params file.
        Usage: params_create
        """
        logger.debug('call function do_params_create')
        print
        self.params = params_inputs()
        print
        params_save(self.params)
        set_friendly_name(self)

    def do_params_display(self, line):
        """
        Display the Kodi params file.
        Usage: params_display
        """
        logger.debug('call function do_params_display')
        params_display(self.params)
        print

    # player functions

    def do_play_albums(self, line):
        """
        Play a given album
        Usage: play_albums id
        """
        logger.debug('call function do_play_songs')
        albumids = []
        albumids.append(int(line))
        pk.playback_stop(self.params)
        pk.playlist_clear(self.params)
        pk.playlist_add_albums(self.params, albumids)
        pk.playback_start(self.params)

    def do_play_ban(self, line):
        """
        Ban the current song (in your echonest tasteprofile) and skip
        Usage: play_ban
            The echonest integration should be activated.
        """
        logger.debug('call function do_play_ban')
        songid = pk.player_songid(self.params)
        pk.player_next(self.params)
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        pk.en_ban(self.params['echonest_key'], profile_id, songid)
        pkd.play_ban(songid, self.songs)
        print

    def do_play_favorite(self, line):
        """
        Like the current song (in your echonest tasteprofile)
        Usage: play_favorite
            The echonest integration should be activated.
        """
        logger.debug('call function do_play_favorite')
        songid = pk.player_songid(self.params)
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        pk.en_favorite(self.params['echonest_key'], profile_id, songid)
        pkd.play_favorite(songid, self.songs)
        print

    def do_play_genres(self, line):
        """
        Play a given genre
        Usage: play_genres id
        """
        logger.debug('call function do_play_genres')
        genreids = []
        genreids.append(int(line))
        pk.playback_stop(self.params)
        pk.playlist_clear(self.params)
        pk.playlist_add_albums(self.params, genreids)
        pk.playback_start(self.params)

    def do_play_party(self, line):
        """
        Start a big party!
        Usage: player_party
        """
        logger.debug('call function do_play_party')
        pk.player_party(self.params)

    def do_play_pause(self, line):
        """
        Switch to play or pause
        Usage: play_pause
            Switch to pause if playing, switch to play if in pause.
        """
        logger.debug('call function do_play_pause')
        pk.playback_start(self.params)

    def do_play_skip(self, line):
        """
        Skip the current song (also in your echonest tasteprofile)
        Usage: play_skip
        """
        logger.debug('call function do_play_skip')
        songid = pk.player_songid(self.params)
        pk.player_next(self.params)
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        pk.en_skip(self.params['echonest_key'], profile_id, songid)
        pkd.play_skip(songid, self.songs)
        print

    def do_play_songs(self, line):
        """
        Play a given song
        Usage: play_songs id
        """
        logger.debug('call function do_play_songs')
        songids = []
        songids.append(int(line))
        pk.playback_stop(self.params)
        pk.playlist_clear(self.params)
        pk.playlist_add_songs(self.params, songids)
        pk.playback_start(self.params)

    def do_play_stop(self, line):
        """
        Stop the music
        Usage: play_stop
            Stop the music and go home, I repeat, stop the music and go home.
        """
        logger.debug('call function do_play_stop')
        pk.playback_stop(self.params)

    def do_play_what(self, line):
        """
        Detail status of what is currently being played
        Usage: play_what
        """
        logger.debug('call function do_play_what')
        properties = pk.player_properties(self.params)
        item = pk.player_item(self.params)
        items = pk.playlist_items(self.params)
        pkd.playlist_now_playing(item, properties)
        pkd.playlist_next_playing(items, properties)
        print

    # playlist functions

    def do_playlist_add_albums(self, line):
        """
        Add an album to the playlist
        Usage: playlist_add_albums id
            Add the album id to the current playlist. Use the
            albums function to find the id.
        """
        logger.debug('call function do_playlist_add_albums')
        albumids = []
        albumids.append(int(line))
        pk.playlist_add_albums(self.params, albumids)

    def do_playlist_add_genres(self, line):
        """
        Add a genre to the playlist
        Usage: playlist_add_genres id
            Add the genre id to the current playlist. Use the
            genres function to find the id.
        """
        logger.debug('call function do_playlist_add_genres')
        genreids = []
        genreids.append(int(line))
        pk.playlist_add_genres(self.params, genreids)

    def do_playlist_add_songs(self, line):
        """
        Add a song to the playlist
        Usage: playlist_add_songs id
            Add the song id to the current playlist. Use the
            songs function to find the id.
        """
        logger.debug('call function do_playlist_add_song')
        songids = []
        songids.append(int(line))
        pk.playlist_add_songs(self.params, songids)

    def do_playlist_clear(self, line):
        """
        Clear the playlist
        Usage: playlist_clear
            Remove all items from the current playlist.
        """
        logger.debug('call function do_playlist_clear')
        pk.playlist_clear(self.params)

    def do_playlist_show(self, line):
        """
        Show the current audio playlist
        Usage: playlist_show
        """
        logger.debug('call function do_playlist_show')
        position = pk.player_position(self.params)
        songids = pk.playlist_songids(self.params)
        pkd.playlist_show(position, songids, self.songs)
        print

    def do_playlist_tasteprofile(self, line):
        """
        Create a playlist from echonest taste profile
        Usage: playlist_tasteprofile
            Generate a new playlist based on echonest taste
            profile. The current playlist is removed before.
        """
        logger.debug('call function do_playlist_tasteprofile')
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        songids = pk.en_playlist(self.params['echonest_key'], profile_id)
        pk.playlist_clear(self.params)
        pk.playlist_add_songs(self.params, songids)
        pkd.songs_index(songids, self.songs)
        print

    def do_playlist_taste_seed(self, line):
        """
        Create a playlist from echonest taste profile seeded by a song
        Usage: playlist_taste_seed songid
            Generate a new playlist based on your echonest taste,
            profile seeded by a song. The current playlist is
            removed before.
        """
        logger.debug('call function do_playlist_taste_seed')
        songid = int(line)
        profile_id = pk.en_profile_id(self.params['echonest_key'])
        songids = pk.en_playlist_seed(self.params['echonest_key'], profile_id, songid)
        pk.playlist_clear(self.params)
        pk.playlist_add_songs(self.params, songids)
        pkd.songs_index(songids, self.songs)
        print

    # songs functions

    def do_songs_display(self, line):
        """
        Display details for a given song
        Usage songs_display id
            Display all information about a given song like the playcount
            or the rating.
        """
        logger.debug('call function do_songs_display')
        songid = int(line)
        pkd.songs_details(songid, self.songs)
        print

    def do_songs_info(self, line):
        """
        Display information on the songs library
        Usage: songs_info
            Display info on the songs set like the number of songs
            or the total duration.
        """
        logger.debug('call function do_songs_info')
        pkd.songs_info(self.songs)
        print

    def do_songs_page(self, line):
        """
        Display a given page of the songs library
        Usage: songs_page page
        """
        logger.debug('call function do_songs_page')
        page = int(line)
        songids = self.songs.keys()[(page - 1) * DISPLAY_NB_LINES:page * DISPLAY_NB_LINES]
        pkd.songs_index(songids, self.songs)
        print

    def do_songs_random(self, line):
        """
        Display a set of random songs
        Usage: songs_random
            Select random songs and display them.
        """
        logger.debug('call function do_songs_random')
        indexes = random.sample(xrange(len(self.songs)), DISPLAY_NB_LINES)
        songids = [self.songs.keys()[index] for index in indexes]
        pkd.songs_index(songids, self.songs)
        print

    def do_songs_search(self, line):
        """
        Search into the songs
        Usage: songs_search string
            List all songs containing the string in the title or artist.
        """
        logger.debug('call function do_songs_search')
        search_string = line.lower()
        songids = pk.songs_search(self.songs, search_string)
        pkd.songs_index(songids, self.songs)
        print

    def do_songs_sync(self, line):
        """
        Sync the Kodi songs library.
        Usage: library_sync
        """
        print
        f_scan, ru_songids, pcu_songids = pk.songs_sync(self.params, self.songs, self.log_level == 0)
        pkd.songs_sync(f_scan, ru_songids, pcu_songids)
        print

    # volume functions

    def do_volume_set(self, line):
        """
        Set Kodi volume
        Usage: volume_set n
            The value should be between 0 and 100.
        """
        logger.debug('call function do_volume_set')
        volume = int(line)
        pk.volume_set(self.params, volume)

    def do_EOF(self, line):
        """Override end of file"""
        logger.info('Bye!')
        print 'Bye!'
        return True

def main():
    """Where everything starts"""

    remote_controller = KodiRemote()
    remote_controller.cmdloop()

if __name__ == '__main__':
    main()
