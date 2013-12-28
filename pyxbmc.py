#!/usr/bin/env python
#
# Copyright 2013 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-xbmc-remote-controller/blob/master/LICENSE.

'''
XBMC remote controller based on TCP transport, JSON and using the (cmd) interface.
'''

import socket
import json
import cmd
import logging
import argparse

# global constants
BUFFER_SIZE = 1024
DISPLAY_NB_LINES = 20

# utilities functions

def get_xbmc_params():
    '''Get XBMC sever IP and port'''
    parser = argparse.ArgumentParser()
    parser.add_argument("ip",
            help='IP of your XBMC server')
    parser.add_argument("-p", "--port",
            type=int,
            default=9090,
            help='TCP port of the XBMC server')
    parser.add_argument("-v", "--verbosity",
            action="store_true",
            help='Increase output verbosity')
    args = parser.parse_args()
    return args.ip, args.port, args.verbosity

def call_api(ip, port, command):
    '''Send the command using TCP'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.send(json.dumps(command))
    data = s.recv(BUFFER_SIZE)
    s.close()
    return json.loads(data)

def display_result(ret):
    '''Display command result for simple methods'''
    logging.debug('call display_result')
    if 'result' in ret:
        if ret['result'] == 'OK':
            print 'Command processed successfully'
        else:
            print 'Too bad, something went wrong'
    else:
        print "Weird, can't read the result"

def display_albums(albums):
    '''Nice looking albums display'''
    logging.debug('call display_albums')
    print 'Recently added albums:'
    print
    for i, album in enumerate(albums):
        print ('%i. %s by %s (%s) - id: %i') % (
                i,
                album['title'],
                album['artist'][0],
                album['year'],
                album['albumid'])
    print

# parsers

def parse_get_int(line):
    '''Parse line for an integer'''
    if len(line) == 0:
        ret_val = 0
    else:
        ret_val = int(line)
    return ret_val

def parse_get_limits(line):
    '''Parse line and return start/end limits'''
    if len(line) == 0:
        start = 0
    else:
        start = int(line)
    end = start + DISPLAY_NB_LINES
    return (start, end)

def parse_get_string(line):
    '''Parse line and return the first string (without space)'''
    args = str.split(line)
    return args[0]

# process return messages

class XBMCRemote(cmd.Cmd):
        
    '''Subclass of the cmd class'''
    
    def preloop(self):
        '''Override and used for class variable'''
        (self.xbmc_ip, self.xbmc_port, verbosity) = get_xbmc_params()
        if verbosity:
            logging.basicConfig(level=logging.DEBUG)
        logging.info('XBMC controller started in verbosity mode')

    def do_audio_library(self, line):
        '''
        Set of namespace AudioLibrary methods.
        '''
        logging.debug('call do_audio_library')
        print 'Try help audio_library'

    def do_audio_library_clean(self, line):
        '''
        Cleans the audio library from non-existent items.
        Usage: audio_library_clean
        '''
        logging.debug('call do_audio_library_clean')
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.Clean",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_audio_library_export(self, line):
        '''
        Exports all items from the audio library
        Usage: audio_library_export
        '''
        logging.debug('call do_audio_library_export')
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.Export",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_audio_library_get_album_details(self, line):
        '''
        Retrieve details about a specific album.
        Usage: audio_library_get_album_degtails album_id
        '''
        logging.debug('call do_audio_library_get_albums')
        album_id = int(line)
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.GetAlbumDetails",
                "params": { "albumid": album_id},
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)

    def do_audio_library_get_albums(self, line):
        '''
        Retrieve all albums with criteria.
        Usage: audio_library_get_albums [start]
        '''
        logging.debug('call do_audio_library_get_albums')
        (start, end) = parse_get_limits(line)
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.GetAlbums",
                "params": {
                    "limits": { "start": start, "end": end } },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        albums = ret['result']['albums']
        display_albums(albums)

    def do_audio_library_get_recently_albums(self, line):
        '''
        Retrieve recently added albums (10 last entries).
        Usage: audio_library_get_recently_albums
        '''
        logging.debug('call do_audio_library_get_recently_albums')
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.GetRecentlyAddedAlbums",
                "params": {
                    "properties": ["title", "artist", "year"],
                    "limits": { "start": 0, "end": 9 } },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        albums = ret['result']['albums']
        display_albums(albums)

    def do_audio_library_get_songs(self, line):
        '''
        Retrieve all songs from specified album, artist or genre
        Usage: audio_library_get_songs start
        '''
        logging.debug('call do_audio_library_get_songs')
        (start, end) = parse_get_limits(line)
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.GetSongs",
                "params": { "limits": { "start": 0, "end": 10 } },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)

    def do_audio_library_scan(self, line):
        '''
        Scan the audio library.
        Usage: audio_library_scan
        '''
        logging.debug('call do_audio_library_scan')
        command = {"jsonrpc": "2.0",
                "method": "AudioLibrary.Scan",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_input(self, line):
        '''
        Set of namespace Input methods.
        '''
        logging.debug('call do_input')
        print 'Try help input'

    def do_input_context_menu(self, line):
        '''
        Display context menu.
        Usage: input_context_menu
        '''
        logging.debug('call do_input_context_menu')
        command = {"jsonrpc": "2.0",
                "method": "Input.ContextMenu",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)
    
    def do_input_home(self, line):
        '''
        Go to home screnn.
        Usage: input_home
        '''
        logging.debug('call do_input_home')
        command = {"jsonrpc": "2.0",
                "method": "Input.Home",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_gui(self, line):
        '''
        Set of namespace GUI methods.
        '''
        logging.debug('call do_gui')
        print 'Try help gui'

    def do_gui_show_notification(self, line):
        '''
        Show a GUI notification with the text 'message' in the low right corner.
        Usage: gui_show_notification message
        '''
        logging.debug('call do_gui_show_notification')
        command = {"jsonrpc": "2.0",
                "method": "GUI.ShowNotification",
                "params": {"title": "PyController", "message": line},
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)
        
    def do_json(self, line):
        '''
        Set of namespace JSONRPC methods.
        '''
        logging.debug('call do_json')
        print 'Try help json'

    def do_json_introspect(self, line):
        '''
        Enumerates all actions and descriptions
        Usage: json_introspect method
        '''
        #TODO: add a pretty print for readability
        logging.debug('call do_json_introspect')
        method = parse_get_string(line)
        command = {"jsonrpc": "2.0",
                "method": "JSONRPC.Introspect",
                "params": {
                    "filter": {
                        "id": method, "type": "method" } },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_json_version(self, line):
        '''
        Get the JSON-RPC protocol version.
        Usage: json_version
        '''
        logging.debug('call do_json_version')
        command = {"jsonrpc": "2.0",
                "method": "JSONRPC.Version",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        print ('JSON-RPC protocol version: %i.%i patch %i' %
                (ret['result']['version']['major'],
                ret['result']['version']['minor'],
                ret['result']['version']['patch']))

    def do_player(self, line):
        '''
        Set of namespace Player methods.
        '''
        logging.debug('call do_player')
        print 'Try help player'

    def do_player_open(self, line):
        '''
        Start playback of either the playlist with the given ID, a slideshow with the pictures from the given directory or a single file or an item from the database.
        Usage: player_open
        '''
        logging.debug('call do_player_open')
        command = {"jsonrpc": "2.0",
                "method": "Player.Open",
                "params": {"item": {"playlistid": 0 } },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_player_playpause(self, line):
        '''
        Pauses or unpause playback and returns the new state.
        Usage: player_open
        '''
        logging.debug('call do_player_playpause')
        command = {"jsonrpc": "2.0",
                "method": "Player.PlayPause",
                "params": {"playerid": 0 },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_player_set_partymode(self, line):
        '''
        Turn partymode on or off
        Usage: player_set_partymode
        '''
        logging.debug('call do_player_set_party_mode')
        command = {"jsonrpc": "2.0",
                "method": "Player.SetPartymode",
                "params": {
                    "playerid": 0,
                    "partymode": True },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)
        
    def do_player_get_actives(self, line):
        '''
        Get the active players.
        Usage: player_get_active
        '''
        logging.debug('call do_player_get_actives')
        command = {"jsonrpc": "2.0",
                "method": "Player.GetActivePlayers",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        if len(ret['result']) == 0:
            print 'Currently no active player'
        else:
            if len(ret['result']) == 1:
                print 'One active player: ' + ret['result'][0]['type']
            else:
                # if two player, it can only be audio and picture
                print 'Two active players: audio and picture'

    def do_player_get_item(self, line):
        '''
        Retrieves the currently played item
        Usage: player_get_item
        '''
        logging.debug('call do_player_get_item')
        command = {"jsonrpc": "2.0",
                "method": "Player.GetItem",
                "params": { "playerid": 0 },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)
        
    def do_player_get_properties(self, line):
        '''
        Retrieves the values of the given properties.
        Usage: player_get_properties
        '''
        logging.debug('call do_player_get_properties')
        command = {"jsonrpc": "2.0",
                "method": "Player.GetProperties",
                "params": {
                    "playerid": 0,
                    "properties": ["time", "totaltime"] },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)
        
    def do_player_stop(self, line):
        '''
        Stops playback.
        Usage: player_set_partymode
        '''
        logging.debug('call do_player_stop')
        command = {"jsonrpc": "2.0",
                "method": "Player.Stop",
                "params": { "playerid": 0 },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)
        
    def do_playlist(self, line):
        '''
        Set of namespace Playlist  methods.
        '''
        logging.debug('call do_playlist')
        print 'Try help playlist'

    def do_playlist_add(self, line):
        '''
        Add item(s) to playlist.
        Usage: playlist_add id
        '''
        logging.debug('call playlist_add')
        playlist_id = parse_get_int(line)
        command = {"jsonrpc": "2.0",
                "method": "Playlist.Add",
                "params": {
                    "playlistid": 0,
                    "item": {"songid": 14934 } },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_playlist_clear(self, line):
        '''
        Clear playlist.
        Usage: playlist_clear id
        '''
        logging.debug('call playlist_clear')
        playlist_id = parse_get_int(line)
        command = {"jsonrpc": "2.0",
                "method": "Playlist.Clear",
                "params": {"playlistid": 0 },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_playlist_get_items(self, line):
        '''
        Get all items from playlist.
        Usage: playlist_get_items id
        '''
        logging.debug('call playlist_get_items')
        playlist_id = parse_get_int(line)
        command = {"jsonrpc": "2.0",
                "method": "Playlist.GetItems",
                "params": {"playlistid": playlist_id},
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)

    def do_playlist_get_playlists(self, line):
        '''
        Get the existing playlist.
        Usage: playlist_get_playlists
        '''
        logging.debug('call playlist_get_playlists')
        command = {"jsonrpc": "2.0",
                "method": "Playlist.GetPlaylists",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)

    def do_playlist_get_properties(self, line):
        '''
        Get the values of the given properties.
        Usage: playlist_get_properties id
        '''
        logging.debug('call playlist_get_properties')
        playlist_id = parse_get_int(line)
        command = {"jsonrpc": "2.0",
                "method": "Playlist.GetProperties",
                "params": {"playlistid": playlist_id, "properties": {} },
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)

    def do_system(self, line):
        '''
        Set of namespace System methods.
        '''
        logging.debug('call do_system')
        print 'Try help system'

    def do_system_reboot(self, line):
        '''
        Reboot the XBMC server.
        Usage: system_reboot
        '''
        logging.debug('call do_system_reboot')
        command = {"jsonrpc": "2.0",
                "method": "System.Reboot",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_video_library(self, line):
        '''
        Set of namespace VideoLibrary methods.
        '''
        logging.debug('call do_video_library')
        print 'Try help audio_library'

    def do_video_library_clean(self, line):
        '''
        Clean the video library.
        Usage: video_library_clean
        '''
        logging.debug('call do_video_library_clean')
        command = {"jsonrpc": "2.0",
                "method": "VideoLibrary.Clean",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_video_library_scan(self, line):
        '''
        Scan the video library.
        Usage: video_library_scan
        '''
        logging.debug('call do_video_library_scan')
        command = {"jsonrpc": "2.0",
                "method": "VideoLibrary.Scan",
                "id": 1}
        logging.debug('command: %s', command)
        ret = call_api(self.xbmc_ip, self.xbmc_port, command)
        logging.debug('return: %s', ret)
        display_result(ret)

    def do_EOF(self, line):
        '''Override end of file'''
        logging.debug('Bye!')
        print 'Bye!'
        return True

def main():
    '''Where everything starts'''

    remote_controller = XBMCRemote()
    remote_controller.cmdloop()

if __name__ == '__main__':
    main()
