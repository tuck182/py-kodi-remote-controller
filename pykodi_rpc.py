#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

'''
Module of functions for Kodi API management.
'''

import requests
import json
import logging

logger = logging.getLogger(__name__)

# API call management

def call_api(server_params, command):
    #if server_params['tcp']:
    #    ret = call_api_tcp(
    #            server_params['ip'], 
    #            server_params['port'],
    #            command)
    #else:
    #TODO: manage TCP calls
    ret = call_api_http(server_params, command)
    return ret

def call_api_http(server_params, command):
    logger.debug('call call_api_http')
    logger.info('command: %s', command)
    kodi_url = 'http://' + server_params['ip'] +  ':' + str(server_params['port']) + '/jsonrpc'
    headers = {'Content-Type': 'application/json'}
    r = requests.post(
            kodi_url,
            data=json.dumps(command),
            headers=headers,
            auth=(server_params['user'], server_params['password']))
    ret = r.json()
    logger.debug('url: %s', r.url)
    logger.debug('status code: %s', r.status_code)
    logger.debug('text: %s', r.text)
    return ret

def call_api_tcp(ip, port, command):
    '''Send the command using TCP'''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    logger.debug('command: %s', command)
    s.send(json.dumps(command))
    data = ''
    while True:
        filler = s.recv(BUFFER_SIZE)
        logger.debug('data received: %s', filler)
        logger.debug('length of the filler: %i', len(filler))
        data += filler
        nb_open_brackets = data.count('{') - data.count('}')
        logger.debug('number of open brackets: %i', nb_open_brackets)
        if nb_open_brackets == 0:
            break
        else:
            logger.info('api reception incomplete')
    s.close()
    logger.debug('data length: %i', len(data))
    ret = json.loads(data)
    logger.debug('return: %s', ret)

def display_result(ret):
    '''Display command result for simple methods'''
    logger.debug('call display_result')
    if 'error' in ret:
        logger.error('too bad, something went wrong!')
        logger.error('error message: %s', ret['error']['message'])
    else:
        logger.info('command processed successfully')

# audiolibrary

def audiolibrary_get_albums_limits(server_params, songid_start, songid_end):
    """Retrieve all albums whithin limits"""
    command = {"jsonrpc": "2.0",
            "method": "AudioLibrary.GetAlbums",
            "params": {
                "limits": {
                    "start": songid_start,
                    "end": songid_end }
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']['limits']

def audiolibrary_get_albums(server_params, albumid_start, albumid_end):
    """Retrieve all albums whithin limits"""
    command = {"jsonrpc": "2.0",
            "method": "AudioLibrary.GetAlbums",
            "params": {
                "properties":
                    [
                        "title",
                        "artist",
                        "year",
                        "rating",
                        "musicbrainzalbumid",
                    ],
                "limits": {
                    "start": albumid_start,
                    "end": albumid_end }
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']['albums']

def audiolibrary_get_songs_full(server_params, songid_start, songid_end):
    """Retrieve all songs whithin limits"""
    command = {"jsonrpc": "2.0",
            "method": "AudioLibrary.GetSongs",
            "params": {
                "properties":
                    [
                        "title",
                        "artist",
                        "year",
                        "duration",
                        "rating",
                        "playcount",
                        "musicbrainztrackid",
                        "genre"
                    ],
                "limits": {
                    "start": songid_start,
                    "end": songid_end }
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']['songs']

def audiolibrary_get_songs_delta(server_params, songid_start, songid_end):
    """Retrieve all songs whithin limits"""
    command = {"jsonrpc": "2.0",
            "method": "AudioLibrary.GetSongs",
            "params": {
                "properties":
                    [
                        "rating",
                        "playcount",
                    ],
                "limits": {
                    "start": songid_start,
                    "end": songid_end }
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']['songs']

def audiolibrary_get_songs_limits(server_params, songid_start, songid_end):
    """Retrieve all songs whithin limits"""
    command = {"jsonrpc": "2.0",
            "method": "AudioLibrary.GetSongs",
            "params": {
                "limits": {
                    "start": songid_start,
                    "end": songid_end }
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']['limits']

# playlist

def playlist_add(item_type, item_id, server_params):
    """Add an item to the audio playlist"""
    logger.debug('call function playlist_add')
    command = {"jsonrpc": "2.0",
            "method": "Playlist.Add",
            "params": {
                "playlistid": 0,
                "item": {
                    item_type: item_id } },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)

def playlist_clear(server_params):
    """Clear the audio playlist"""
    logger.debug('call function playlist_clear')
    command = {"jsonrpc": "2.0",
            "method": "Playlist.Clear",
            "params": {
                "playlistid": 0 },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)

def playlist_get_items(server_params):
    """Get all songids from the audio playlist"""
    logger.debug('call playlist_get_items')
    command = {"jsonrpc": "2.0",
            "method": "Playlist.GetItems",
            "params": {
                "playlistid": 0,
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result'].get('items', [])

# player

def player_get_active(server_params):
    """Returns active audio players (boolean)"""
    logger.debug('call function player_get_active')
    command = {
        'jsonrpc': '2.0',
        'method': 'Player.GetActivePlayers',
        'id': 1,
    }
    ret = call_api(server_params, command)
    display_result(ret)
    return not len(ret['result']) == 0

def player_get_item(server_params):
    '''Get the current played item'''
    #TODO: change to return item id only
    logger.debug('call function get_item')
    command = {"jsonrpc": "2.0",
            "method": "Player.GetItem",
            "params": {
                "playerid": 0,
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    if 'result' in ret:
        return ret['result']['item']['id']
    else:
        return None

def player_get_properties(server_params):
    """Get properties of the played item"""
    logger.debug('call function player_get_properties')
    command = {"jsonrpc": "2.0",
            "method": "Player.GetProperties",
            "params": {
                "playerid": 0,
                "properties": [
                    "time",
                    "totaltime",
                    "percentage",
                    "position" ] },
                "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']

def player_goto(server_params):
    '''Go to the next item'''
    logger.debug('call function player_goto')
    command = {"jsonrpc": "2.0",
            "method": "Player.GoTo",
            "params":{
                "playerid": 0,
                "to": 'next'},
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)

def player_open(server_params):
    """Open the audio playlist"""
    logger.debug('call function player_open')
    command = {
        'jsonrpc': '2.0',
        'method': 'Player.Open',
        'params': {
            'item': {
                'playlistid': 0
            },
        },
        'id': 1
    }
    ret = call_api(server_params, command)
    display_result(ret)

def player_open_party(server_params):
    '''Open the audio player in partymode'''
    logger.debug('call function player_open_party')
    command = {"jsonrpc": "2.0",
            "method": "Player.Open",
            "params": {
                "item": {
                    "partymode": "music" }
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)

def player_play_pause(server_params):
    """Pauses or unpause playback"""
    logger.debug('call function player_play_pause')
    command = {"jsonrpc": "2.0",
            "method": "Player.PlayPause",
            "params": {
                "playerid": 0,
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)

def player_stop(server_params):
    """Stop playback"""
    logger.debug('call function player_stop')
    command = {"jsonrpc": "2.0",
            "method": "Player.Stop",
            "params": {
                "playerid": 0 },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)

# application

def player_volume(server_params,volume):
    '''Volume'''
    logger.debug('call function player_volume')
    command = {"jsonrpc": "2.0",
            "method": "Application.SetVolume",
            "params": {
                "volume": volume,
                },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    
# system

def system_friendly_name(server_params):
    '''Get the system name and hostname'''
    command = {"jsonrpc": "2.0",
            "method": "XBMC.GetInfoLabels",
            "params": {
                "labels": ["System.FriendlyName"] },
            "id": 1}
    ret = call_api(server_params, command)
    display_result(ret)
    return ret['result']['System.FriendlyName']

def jsonrpc_ping(server_params):
    '''Ping the server'''
    logger.debug('call function jsonrpc_ping')
    command = {"jsonrpc": "2.0",
            "method": "JSONRPC.Ping",
            "id": 1}
    try:
        ret = call_api(server_params, command)
        display_result(ret)
        return True
    except requests.exceptions.ConnectionError:
        return False
