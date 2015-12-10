#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

"""
Kodi remote controller package based on HTTP transport and JSON.
"""

from .. import rpc
from .. import echonest
from progressbar import *
import pickle
import time
import logging

# global constants

ALBUM = 'albumid'
SONG = 'songid'

# Kodi sync parameters
SONGS_SLICE_SIZE = 20
ALBUMS_SLICE_SIZE = 20

# echonest sync parameters
SONGS_EN_SLICE_SIZE = 25
EN_API_WAIT = 0.51 # max 120 api calls per minute

# global variable
logger = logging.getLogger(__name__)

def is_reachable(params):
    """Return true if the Kodi server is reachable"""
    logger.debug('call function is_reachable')
    ping_reply = rpc.jsonrpc_ping(params)
    return ping_reply

def get_friendly_name(params):
    """Return Kodi server friendly name"""
    logger.debug('call function get_friendly_name')
    assert is_reachable(params)
    friendly_name = rpc.system_friendly_name(params)
    return friendly_name

# local files

def save_songs(songs):
    """Save songs to local files"""
    logger.debug('call function save_songs')
    f = open('songs.pickle', 'wb')
    pickle.dump(songs, f)
    f.close()

def save_albums(albums):
    """Save albums to local files"""
    logger.debug('call function save_albums')
    f = open('albums.pickle', 'wb')
    pickle.dump(albums, f)
    f.close()

def set_songs_sync(params, songs, p_bar):
    """Sync library songs to local"""
    logger.debug('call function set_songs_sync')
    assert is_reachable(params)
    # get the number of songs
    limits = rpc.audiolibrary_get_songs_limits(params, 0, 1)
    nb_songs = limits['total']
    logger.debug('total number of songs: %i', nb_songs)
    # select sync type
    if len(songs) == nb_songs:
        full_scan = False
    else:
        full_scan = True
    logger.info('full scan: %s', full_scan)
    if p_bar:
        widgets = [
            'Songs: ', Percentage(),
            ' ', Bar(marker='#',left='[',right=']'),
            ' (', Counter(), ' in ' + str(nb_songs) + ') ',
            ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=nb_songs)
        pbar.start()
    # dicts for delta sync
    rating_up_songids = []
    playcount_up_songids = []
    # slicing and loop
    slice = 0
    while True:
        start = slice * SONGS_SLICE_SIZE
        end = (slice + 1) * SONGS_SLICE_SIZE
        if end > nb_songs:
            end = nb_songs
        logger.info(
            'processing slice %i (songs %i to %i in %i)',
            slice,
            start,
            end,
            nb_songs)
        if p_bar:
            pbar.update(start)
        # fetch songs slice data
        if full_scan:
            loop_songs = rpc.audiolibrary_get_songs_full(params, start, end)
        else:
            loop_songs = rpc.audiolibrary_get_songs_delta(params, start, end)
        # update songs dataset
        for loop_song in loop_songs:
            if full_scan:
                songs[loop_song['songid']] = loop_song.copy()
                del songs[loop_song['songid']]['songid']
                songs[loop_song['songid']]['rating_en'] = 0
                songs[loop_song['songid']]['playcount_en'] = 0
            else:
                if not songs[loop_song['songid']]['rating'] == loop_song['rating']:
                    songs[loop_song['songid']]['rating'] = loop_song['rating']
                    logger.info('rating updated for song: %i', loop_song['songid'])
                    rating_up_songids.append(loop_song['songid'])
                if not songs[loop_song['songid']]['playcount'] == loop_song['playcount']:
                    songs[loop_song['songid']]['playcount'] = loop_song['playcount']
                    logger.info('playcount updated for song: %i', loop_song['songid'])
                    playcount_up_songids.append(loop_song['songid'])
        if end == nb_songs:
            break
        slice += 1
    if p_bar:
        pbar.finish()
    # persist songs dataset
    save_songs(songs)
    return full_scan, rating_up_songids, playcount_up_songids

def set_albums_sync(params, albums, p_bar):
    """Sync library albums to local"""
    logger.debug('call function set_albums_sync')
    assert is_reachable(params)
    # get the number of songs
    limits = rpc.audiolibrary_get_albums_limits(params, 0, 1)
    nb_albums = limits['total']
    logger.debug('total number of albums: %i', nb_albums)
    if p_bar:
        widgets = [
            'Albums: ', Percentage(),
            ' ', Bar(marker='#',left='[',right=']'),
            ' (', Counter(), ' in ' + str(nb_albums) + ') ',
            ETA()]
        pbar = ProgressBar(widgets=widgets, maxval=nb_albums)
        pbar.start()
    # slicing and loop
    slice = 0
    while True:
        start = slice * ALBUMS_SLICE_SIZE
        end = (slice + 1) * ALBUMS_SLICE_SIZE
        if end > nb_albums:
            end = nb_albums
        logger.info(
            'processing slice %i (songs %i to %i in %i)',
            slice,
            start,
            end,
            nb_albums)
        if p_bar:
            pbar.update(start)
        # fetch songs slice data
        loop_albums = rpc.audiolibrary_get_albums(params, start, end)
        # update songs dataset
        for loop_album in loop_albums:
            albums[loop_album['albumid']] = loop_album.copy()
            del albums[loop_album['albumid']]['albumid']
        if end == nb_albums:
            break
        slice += 1
    if p_bar:
        pbar.finish()
    # persist albums dataset
    save_albums(albums)

# other

def get_albums_search(search_string, albums):
    """Search a string in albums"""
    search_result_title = []
    search_result_artist = []
    for albumid in albums.keys():
        if search_string in albums[albumid]['title'].encode('utf-8').lower():
            search_result_title.append(albumid)
        if search_string in "/".join(albums[albumid]['artist']).encode('utf-8').lower():
            search_result_artist.append(albumid)
    logger.debug('search result by title: %s', search_result_title)
    logger.debug('search result by artist: %s', search_result_artist)
    return sorted(list(set(search_result_title + search_result_artist)))

def get_songs_search(search_string, songs):
    """Search a string in songs"""
    search_result_title = []
    search_result_artist = []
    for songid in songs.keys():
        if search_string in songs[songid]['title'].encode('utf-8').lower():
            search_result_title.append(songid)
        if search_string in "/".join(songs[songid]['artist']).encode('utf-8').lower():
            search_result_artist.append(songid)
    logger.debug('search result by title: %s', search_result_title)
    logger.debug('search result by artist: %s', search_result_artist)
    return sorted(list(set(search_result_title + search_result_artist)))

def get_playlist_songids(params):
    """Fetch playlist items"""
    logger.debug('call get_playlist_songids')
    items = rpc.playlist_get_items(params)
    songids = [item['id'] for item in items]
    return songids

def get_playlist_position(params):
    """Return the current playing item in the playlist"""
    # TODO rename to player
    logger.debug('call get_playlist_position')
    properties = rpc.player_get_properties(params)
    return properties['position']

def player_properties(params):
    """Return the played time of the current song"""
    logger.debug('call player_properties')
    properties = rpc.player_get_properties(params)
    return properties

def player_item(params):
    """Return the played time of the current song"""
    logger.debug('call player_properties')
    item = rpc.player_get_item(params)
    return item

def playlist_items(params):
    """Return items playlist"""
    logger.debug('call playlist_items')
    items = rpc.playlist_get_items(params)
    return items

def get_play_item(params):
    """Return the currently played item"""
    logger.debug('call get_play_item')
    item = rpc.player_get_item(params)
    return item['id']

def playlist_add_songs(songids, params):
    """Add songids list to the playlist"""
    logger.debug('call playlist_add_songs')
    for songid in songids:
        rpc.playlist_add(SONG, songid, params)

def playlist_add_albums(albumids, params):
    """Add albumids list to the playlist"""
    logger.debug('call playlist_add_albums')
    for albumid in albumids:
        rpc.playlist_add(ALBUM, albumid, params)

def en_sync(api_key, profile_id, songs, p_bar):
    """Sync songs with echonest tasteprofile"""
    en_info = echonest.tasteprofile_profile_id(api_key, profile_id)
    if en_info['total'] == 0:
        logger.info("full sync")
        songids = songs.keys()
    else:
        logger.info("delta sync")
        songids = []
        for songid in songs:
            if not (songs[songid]['rating'] == songs[songid]['rating_en']
                    and songs[songid]['playcount'] == songs[songid]['playcount_en']):
                songids.append(songid)
        logger.debug("songs to sync: %s", songids)
    nb_songs = len(songids)
    logger.debug("numer of songs to sync: %s", nb_songs)
    if nb_songs == 0:
        logger.debug("no songs to sync")
        return songids
    if p_bar:
        widgets = [
            'Songs: ', Percentage(),
            ' ', Bar(marker='#',left='[',right=']'),
            ' (', Counter(), ' in ' + str(nb_songs) + ') ',
            ETA()
        ]
        pbar = ProgressBar(widgets=widgets, maxval=nb_songs)
        pbar.start()
    # slicing and loop
    slice = 0
    while True:
        start = slice * SONGS_EN_SLICE_SIZE
        end = (slice + 1) * SONGS_EN_SLICE_SIZE
        if end > nb_songs:
            end = nb_songs
        logger.info(
            'processing slice %i (songs %i to %i in %i)',
            slice,
            start,
            end,
            nb_songs)
        if p_bar:
            pbar.update(start)
        items = {}
        for song_index in range(start, end):
            songid = songids[song_index]
            mb_song_id = 'musicbrainz:song:' + songs[songid]['musicbrainztrackid']
            items[str(songid)] = {}
            items[str(songid)]['song_id'] = mb_song_id
            items[str(songid)]['rating'] = songs[songid]['rating']
            items[str(songid)]['play_count'] = songs[songid]['playcount']
            songs[songid]['rating_en'] = songs[songid]['rating']
            songs[songid]['playcount_en'] = songs[songid]['playcount']
        echonest.tasteprofile_update(items, api_key, profile_id)
        if end == nb_songs:
            break
        slice +=1
        time.sleep(EN_API_WAIT)
    if p_bar:
        pbar.finish()
    save_songs(songs)
    return songids

def echonest_status(ticket, api_key):
    """Check ticket status"""
    logger.debug('call echonest_status')
    echonest.tasteprofile_status(ticket, api_key)

def en_playlist(api_key, profile_id):
    """Create a static playlist"""
    logger.debug('call en_playlist')
    en_songs = echonest.playlist_static(api_key, profile_id)
    songids = []
    for en_song in en_songs:
        en_id = en_song['foreign_ids'][0]['foreign_id']
        songid = int(en_id.replace(profile_id + ':song:', ""))
        songids.append(songid)
    return songids

def en_playlist_seed(songid, api_key, profile_id):
    """Create a static playlist"""
    logger.debug('call en_playlist')
    song_id = profile_id + ':song:' + str(songid)
    en_songs = echonest.playlist_static_seed(song_id, api_key, profile_id)
    songids = []
    #TODO function to extract the songids (shared with en_playlist)
    for en_song in en_songs:
        en_id = en_song['foreign_ids'][0]['foreign_id']
        songid = int(en_id.replace(profile_id + ':song:', ""))
        songids.append(songid)
    return songids

def get_en_profile_id(api_key):
    """Get echonest profile profile ID"""
    logger.debug('call get_profile_id')
    ret = echonest.tasteprofile_profile_name(api_key)
    if not 'catalog' in ret:
        logger.info('no taste profile found, will create one')
        echonest.tasteprofile_create(api_key)
        ret = echonest.tasteprofile_profile_name(api_key)
    profile_id = ret['catalog']['id']
    logger.debug('profile id: %s', profile_id)
    return profile_id

def get_en_info(api_key, profile_id):
    """Fetch echonest taste profile info"""
    logger.debug('call get_en_info')
    en_info = echonest.tasteprofile_profile_id(api_key, profile_id)
    return en_info

def en_delete(api_key, profile_id):
    """Delete the echonest tasteprofile"""
    logger.debug('call en_delete')
    echonest.tasteprofile_delete(api_key, profile_id)

def en_display(songid, api_key, profile_id):
    """Display song detail from tasteprofile"""
    logger.debug('call en_display')
    item = echonest.tasteprofile_read(str(songid), api_key, profile_id)
    return item

def playback_start(params):
    """Start playback"""
    logger.debug('call function playback_start')
    if rpc.player_get_active(params):
        rpc.player_play_pause(params)
    else:
        logger.info('no active player, will open one')
        rpc.player_open(params)

def playback_stop(params):
    """Start playback"""
    logger.debug('call function playback_stop')
    if rpc.player_get_active(params):
        rpc.player_stop(params)

def clear_playlist(params):
    """Clear the audio playlist"""
    rpc.playlist_clear(params)

def en_favorite(api_key, profile_id, songid):
    """Toggle favorite flag in echonest"""
    logger.debug('call function en_favorite')
    echonest.tasteprofile_favorite(api_key, profile_id, str(songid))

def en_skip(api_key, profile_id, songid):
    """Toggle favorite flag in echonest"""
    logger.debug('call function en_skip')
    echonest.tasteprofile_skip(api_key, profile_id, str(songid))

def en_ban(api_key, profile_id, songid):
    """Toggle ban flag in echonest"""
    logger.debug('call function en_ban')
    echonest.tasteprofile_ban(api_key, profile_id, str(songid))

def play_next(params):
    """Move to the next song"""
    logger.debug('call function play_next')
    rpc.player_goto_next(params)

def play_party(params):
    """Trigger party mode"""
    logger.debug('call function play_party')
    rpc.player_open_party(params)

def volume_set(params, volume):
    """Set server volume"""
    logger.debug('call function volume_set')
    rpc.application_set_volume(params, volume)