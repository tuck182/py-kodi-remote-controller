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

import pykodi as kodi
import pykodi_fd as pk_fd

import cmd
import logging
import random
import argparse
import pickle

# global constants

DISPLAY_NB_LINES = 10

logger = logging.getLogger(__name__)

# utility functions

def get_params():
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
            logger.info('Kodi controller started in verbosity mode ...')
            logger.debug('... and even in high verbosity mode!')
        else:
            args.verbosity = 0
    return args.verbosity

def is_file(fname):
    """Return true if the file does exist"""
    logger.debug('call function is_file')
    try:
        open(fname)
    except IOError:
        return False
    return True

def input_params():
    """Request the user for params input"""
    logger.debug('call function input_params')
    params = {}
    params['ip'] = raw_input("Kodi server IP: ")
    params['port'] = raw_input("Kodi server port: ")
    params['user'] = raw_input("Kodi server user: ")
    params['password'] = raw_input("Kodi server password: ")
    params['echonest_key'] = raw_input("Echonest developer key: ")
    return params

def save_params(params):
    """Save the Kodi parameters to a local file"""
    logger.debug('call function save_params')
    f = open('params.pickle', 'wb')
    pickle.dump(params, f)
    f.close()

def read_params():
    """Read the Kodi params from the local file"""
    logger.debug('call function read_params')
    f = open('params.pickle', 'rb')
    params = pickle.load(f)
    f.close()
    return params

def display_banner():
    """Display initial banner"""
    logger.debug('call function display_banner')
    print "No Kodi params file found, this is probably the first launch. Check"
    print "your Kodi parameters (IP, port, user and password) and create an"
    print "Echonest account: https://developer.echonest.com/account/register"
    print
    print "Read the API key on the Echonest account, it will be requested"
    print "later on. When you are ready, try params_create."

def get_albums_from_file(fname):
    """Load albums from pickle file"""
    logger.debug('call function get_albums_from_file')
    f = open(fname, 'rb')
    albums = pickle.load(f)
    f.close()
    return albums

def get_songs_from_file(fname):
    """Load songs from pickle file"""
    logger.debug('call function get_songs_from_file')
    f = open(fname, 'rb')
    songs = pickle.load(f)
    f.close()
    return songs

def set_friendly_name(self):
    """Set Kodi friendly name in the cmd prompt"""
    logger.debug('call function set_friendly_name')
    friendly_name = kodi.get_friendly_name(self.params)
    self.prompt = "(" + friendly_name + ") "


class KodiRemote(cmd.Cmd):
    
    def preloop(self):
        self.log_level = get_params()
        if not is_file('params.pickle'):
            logger.info('no kodi params file')
            print
            display_banner()
            print
            return
        logger.debug('kodi params file found')
        self.params = read_params()
        set_friendly_name(self)
        if not is_file('albums.pickle'):
            self.albums = {}
        else:
            self.albums = get_albums_from_file('albums.pickle')
        if not is_file('songs.pickle'):
            self.songs = {}
        else:
            self.songs = get_songs_from_file('songs.pickle')

    # albums functions

    def do_albums_display(self, line):
        """
        Display details for a given album
        Usage albums_display id
            Display all information about a given album like the artist
            or the release year.
        """
        logger.debug('call function do_albums_display')
        albumid = int(line)
        pk_fd.albums_details(albumid, self.albums)
        print

    def do_albums_page(self, line):
        """
        Display a given page of the albums library
        Usage: albums_page page
        """
        logger.debug('call function do_albums_page')
        page = int(line)
        albumids = self.albums.keys()[(page - 1) * DISPLAY_NB_LINES:page * DISPLAY_NB_LINES]
        pk_fd.albums_index(albumids, self.albums)
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
        pk_fd.albums_index(albumids, self.albums)
        print

    def do_albums_recent(self, line):
        """
        Display recently added albums
        Usage: albums_recent
        """
        logger.debug('call function do_albums_recent')
        albumids = self.albums.keys()[-1 * DISPLAY_NB_LINES:]
        pk_fd.albums_index(albumids, self.albums)
        print

    def do_albums_search(self, line):
        """
        Search into the albums
        Usage: songs_search string
            List all albums containing the string in the title or artist.
        """
        logger.debug('call function do_albums_search')
        search_string = line.lower()
        albumids = kodi.get_albums_search(search_string, self.albums)
        pk_fd.albums_index(albumids, self.albums)
        print

    def do_albums_sync(self, line):
        """
        Sync the Kodi albums library.
        Usage: album_sync
        """
        print
        kodi.set_albums_sync(self.params, self.albums, self.log_level == 0)
        print

    # echonest functions

    def do_echonest_delete(self, line):
        """
        Delete echonest taste profile.
        Usage: echonest_delete
        """
        logger.debug('call function do_echonest_delete')
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        if pk_fd.sure_delete_tasteprofile(self.params['echonest_key'], profile_id):
            kodi.en_delete(self.params['echonest_key'], profile_id)
            pk_fd.echonest_detele()
        print

    def do_echonest_display(self, line):
        """
        Display song details in tasteprofile.
        Usage: echonest_delete
        """
        logger.debug('call function do_echonest_display')
        songid = int(line)
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        song_data = kodi.en_display(songid, self.params['echonest_key'], profile_id)
        pk_fd.en_display(song_data)
        print

    def do_echonest_info(self, line):
        """
        Display info about the echonest taste profile.
        Usage: echonest_info
        """
        logger.debug('call function do_echonest_info')
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        en_info = kodi.get_en_info(self.params['echonest_key'], profile_id)
        pk_fd.echonest_info(en_info)
        print

    def do_echonest_status(self, line):
        """
        Check the status of a tasteprofile update.
        Usage: echonest_status ticket
            If there is no song in the profile, a full sync is
            performed. Otherwise, only the play counts and the
            ratings are updated.
        """
        logger.debug('call function do_echonest_sync')
        ticket = line
        kodi.echonest_status(ticket, self.params['echonest_key'])

    def do_echonest_sync(self, line):
        """
        Sync local songs with the echonest tasteprofile.
        Usage: echonest_sync
            If there is no song in the profile, a full sync is
            performed. Otherwise, only the play counts and the
            ratings are updated.
        """
        logger.debug('call function do_echonest_sync')
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        print
        en_songids = kodi.en_sync(self.params['echonest_key'], profile_id, self.songs, self.log_level == 0)
        pk_fd.en_sync(en_songids)
        print

    # Kodi params file

    def do_params_create(self, line):
        """
        Create the Kodi params file.
        Usage: params_create
        """
        logger.debug('call function do_params_create')
        print
        self.params = input_params()
        print
        save_params(self.params)
        set_friendly_name(self)

    def do_params_display(self, line):
        """
        Display the Kodi params file.
        Usage: params_display
        """
        logger.debug('call function do_params_display')
        print
        print "Kodi parameters:"
        print "\tNetwork:    %s/%s" % (
                self.params['ip'], 
                self.params['port'])
        print "\tCredential: %s (%s)" % (
                self.params['user'], 
                self.params['password'])
        print
        print "Echonest API key: %s" % self.params['echonest_key']
        print

    # player functions

    def do_play_ban(self, line):
        """
        Ban the current song and skip
        Usage: play_ban
        """
        logger.debug('call function do_play_ban')
        songid = kodi.get_play_item(self.params)
        kodi.play_next(self.params)
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        kodi.en_ban(self.params['echonest_key'], profile_id, songid)
        pk_fd.play_ban(songid, self.songs)
        print

    def do_play_favorite(self, line):
        """
        Like the current song (in your echonest tasteprofile)
        Usage: play_favorite
        """
        logger.debug('call function do_play_favorite')
        songid = kodi.get_play_item(self.params)
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        kodi.en_favorite(self.params['echonest_key'], profile_id, songid)
        pk_fd.play_favorite(songid, self.songs)
        print

    def do_play_party(self, line):
        """
        Start a big party!
        Usage: play_party
        """
        logger.debug('call function do_play_party')
        kodi.play_party(self.params)

    def do_play_pause(self, line):
        """
        Switch to play or pause
        Usage: play_pause
            Switch to pause if playing, switch to play if in pause.
        """
        logger.debug('call function do_play_pause')
        kodi.playback_start(self.params)

    def do_play_skip(self, line):
        """
        Skip the current song
        Usage: play_skip
        """
        logger.debug('call function do_play_skip')
        songid = kodi.get_play_item(self.params)
        kodi.play_next(self.params)
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        kodi.en_skip(self.params['echonest_key'], profile_id, songid)
        pk_fd.play_skip(songid, self.songs)
        print

    def do_play_stop(self, line):
        """
        Stop the music
        Usage: play_stop
            Stop the music and go home, I repeat, stop the music and go home.
        """
        logger.debug('call function do_play_stop')
        kodi.playback_stop(self.params)

    def do_play_what(self, line):
        """
        Detail status of what is currently played
        Usage: play_what
        """
        logger.debug('call function do_play_what')
        properties = kodi.player_properties(self.params)
        item = kodi.player_item(self.params)
        items = kodi.playlist_items(self.params)
        pk_fd.now_playing(item, properties)
        pk_fd.next_playing(items, properties)
        print

    # playlist functions

    def do_playlist_add_album(self, line):
        """
        Add a album to the playlist
        Usage: playlist_add_album [id]
            Add the album id to the current playlist.
            Use the albums function to find the id.
        """
        logger.debug('call function do_playlist_add_album')
        albumids = []
        albumids.append(int(line))
        kodi.playlist_add_albums(albumids, self.params)

    def do_playlist_add_song(self, line):
        """
        Add a song to the playlist
        Usage: playlist_add_song [id]
            Add the song id to the current playlist.
            Use the songs function to find the id.
        """
        logger.debug('call function do_playlist_add_song')
        songids = []
        songids.append(int(line))
        kodi.playlist_add_songs(songids, self.params)

    def do_playlist_clear(self, line):
        """
        Clear the playlist
        Usage: playlist_clear
            Remove all items from the current playlist.
        """
        logger.debug('call function do_playlist_clear')
        kodi.clear_playlist(self.params)

    def do_playlist_show(self, line):
        """
        Show the current audio playlist
        Usage: playlist_show
        """
        logger.debug('call function do_playlist_show')
        position = kodi.get_playlist_position(self.params)
        songids = kodi.get_playlist_songids(self.params)
        pk_fd.playlist_show(position, songids, self.songs)
        print

    def do_playlist_tasteprofile(self, line):
        """
        Create a playlist from echonest taste profile
        Usage: playlist_tasteprofile
            Generate and play a new playlist based on
            echonest taste profile. The current playlist
            is removed before.
        """
        logger.debug('call function do_playlist_tasteprofile')
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        songids = kodi.en_playlist(self.params['echonest_key'], profile_id)
        kodi.clear_playlist(self.params)
        kodi.playlist_add_songs(songids, self.params)
        pk_fd.songs_index(songids, self.songs)
        print

    def do_playlist_taste_seed(self, line):
        """
        Create a playlist from echonest taste profile and seeded by a song
        Usage: playlist_tasteprofile song_id
            Generate and play a new playlist based on
            echonest taste profile. The current playlist
            is removed before.
        """
        logger.debug('call function do_playlist_taste_seed')
        songid = int(line)
        profile_id = kodi.get_en_profile_id(self.params['echonest_key'])
        songids = kodi.en_playlist_seed(songid, self.params['echonest_key'], profile_id)
        kodi.clear_playlist(self.params)
        kodi.playlist_add_songs(songids, self.params)
        pk_fd.songs_index(songids, self.songs)
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
        pk_fd.songs_details(songid, self.songs)
        print

    def do_songs_info(self, line):
        """
        Display information on the songs set
        Usage: songs_info
            Display info on the songs set like the number of songs
            or the total duration.
        """
        logger.debug('call function do_songs_info')
        pk_fd.songs_info(self.songs)
        print

    def do_songs_page(self, line):
        """
        Display a given page of the songs library
        Usage: songs_page page
        """
        logger.debug('call function do_songs_page')
        page = int(line)
        songids = self.songs.keys()[(page - 1) * DISPLAY_NB_LINES:page * DISPLAY_NB_LINES]
        pk_fd.songs_index(songids, self.songs)
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
        pk_fd.songs_index(songids, self.songs)
        print

    def do_songs_search(self, line):
        """
        Search into the songs
        Usage: songs_search string
            List all songs containing the string in the title or artist.
        """
        logger.debug('call function do_songs_search')
        search_string = line.lower()
        songids = kodi.get_songs_search(search_string, self.songs)
        pk_fd.songs_index(songids, self.songs)
        print

    def do_songs_sync(self, line):
        """
        Sync the Kodi songs library.
        Usage: library_sync
        """
        print
        f_scan, ru_songids, pcu_songids = kodi.set_songs_sync(self.params, self.songs, self.log_level == 0)
        pk_fd.songs_sync(f_scan, ru_songids, pcu_songids)
        print

    def do_EOF(self, line):
        '''Override end of file'''
        logger.info('Bye!')
        print 'Bye!'
        return True

def main():
    """Where everything starts"""

    remote_controller = KodiRemote()
    remote_controller.cmdloop()

if __name__ == '__main__':
    main()
