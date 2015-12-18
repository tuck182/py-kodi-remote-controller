#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

"""
Module of display functions for PyKodi.
"""

import datetime
import logging

# global variable
logger = logging.getLogger(__name__)

# albums

def albums_details(albumid, albums):
    """Display album details from albumid"""
    logger.debug('call function albums_details')
    print
    print "\"{}\" by {} ({})".format(
        albums[albumid]['title'],
        "/".join(albums[albumid]['artist']),
        albums[albumid]['year']
    )
    print
    print "   Rating:          {}".format(albums[albumid]['rating'])
    print "   MusicBrainz ID:  {}".format(albums[albumid]['musicbrainzalbumid'])

def albums_index(albumids, albums):
    """Display albums list from internal index"""
    logger.debug('call function disp_albums_index')
    print
    for albumid in albumids:
        print "   \"{}\" by {} ({}) [{}]".format(
            albums[albumid]['title'].encode('UTF-8'),
            "/".join(albums[albumid]['artist']).encode('UTF-8'),
            albums[albumid]['year'],
            albumid
        )

def albums_info(albums):
    """Display albums information"""
    logger.debug('call function albums_info')
    print
    print "   Total number of albums: {}".format(len(albums))

# genres

def genres_index(genreids, genres):
    """Display genres list from internal index"""
    logger.debug('call function genres_index')
    print
    for genreid in genreids:
        print "   {} [{}]".format(
            genres[genreid].encode('UTF-8'),
            genreid
        )

def genres_info(genres):
    """Display genres information"""
    logger.debug('call function genres_info')
    print
    print "   Total number of genres: {}".format(len(genres))

# songs

def songs_index(songids, songs):
    """Display songs list from internal index"""
    logger.debug('call function songs_index')
    print
    for songid in songids:
        print "   \"{}\" by {} ({}) [{}]".format(
            songs[songid]['title'].encode('UTF-8'),
            "/".join(songs[songid]['artist']).encode('UTF-8'),
            songs[songid]['year'],
            songid
        )

def songs_details(songid, songs):
    """Display song details from song id"""
    logger.debug('call function songs_details')
    print
    print "\"{}\" by {} ({})".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8'),
        songs[songid]['year']
    )
    print
    print "   Duration:        {}".format(
        str(datetime.timedelta(seconds=songs[songid]['duration']))
    )
    print "   Playcount:       {} ({})".format(
        songs[songid]['playcount'],
        songs[songid]['playcount_en']
    )
    print "   Rating:          {} ({})".format(
        songs[songid]['rating'],
        songs[songid]['rating_en']
    )
    print "   MusicBrainz ID:  {}".format(
        songs[songid]['musicbrainztrackid']
    )

def songs_info(songs):
    """Display songs information"""
    logger.debug('call function songs_info')
    print
    print "   Total number of songs: {}".format(len(songs))
    total_duration = 0
    for songid in songs:
        total_duration += songs[songid]['duration']
    duration_str = str(datetime.timedelta(seconds=total_duration))
    print "   Total duration: {}".format(duration_str)

def songs_sync(f_scan, ru_songsids, pcu_songids):
    """Display result of the songs sync process"""
    logger.debug('call function songs_sync')
    print
    if f_scan:
        print "   A full scan has been performed."
    else:
        print "A delta scan has been performed, {} song(s) with a rating " \
              "update and {} song(s) with a play count update.".format(
                len(ru_songsids), len(pcu_songids)
        )

# playlist

def playlist_show(position, songids, songs):
    """Display playlist"""
    logger.debug('call function playlist_show')
    print
    if songids:
        for i, songid in enumerate(songids):
            if i == position:
                print ">> ",
            else:
                print "   ",
            print "{}. \"{}\" by {} ({}) [{}]".format(
                str(i+1).zfill(2),
                songs[songid]['title'].encode('utf-8'),
                "/".join(songs[songid]['artist']).encode('utf-8'),
                songs[songid]['year'],
                songid
            )
    else:
        print "   [playlist empty]"

def playlist_now_playing(item, properties):
    """Display the now playing part of play_what"""
    logger.debug('call function playlist_now_playing')
    print
    if not item:
        print "   [not playing anything]"
        return
    # build rating display
    disp_rating = '*' * int(item['rating']) + '.' * (5 - int(item['rating']))
    # build time variables
    play_time = datetime.timedelta(
        hours=properties['time']['hours'],
        minutes=properties['time']['minutes'],
        seconds=properties['time']['seconds']
    )
    play_totaltime = datetime.timedelta(
        hours=properties['totaltime']['hours'],
        minutes=properties['totaltime']['minutes'],
        seconds=properties['totaltime']['seconds']
    )
    print "Now Playing:"
    print
    print "{} - {} ({})".format(
        "/".join(item['artist']).encode('UTF-8'),
        item['album'].encode('UTF-8'),
        item['year']
    )
    print "   {} - [{}]".format(item['label'].encode('UTF-8'), disp_rating)
    print "   {} / {} - {} %".format(
        play_time,
        play_totaltime,
        int(properties['percentage'])
    )

def playlist_next_playing(items, properties):
    """Display the next playing part of display_what"""
    logger.debug('call function playlist_show')
    if not properties:
        return
    print
    print "({} / {}) - Next: {} - {}".format(
        properties['position'] + 1,
        len(items),
        "/".join(items[properties['position'] + 1]['artist']).encode('UTF-8'),
        items[properties['position'] + 1]['label'].encode('UTF-8')
    )

# player

def play_album(albumid, albums):
    """Confirm play album"""
    logger.debug('call function play_album')
    print "   Let's play the album \"%s\" by %s [%i].".format(
        albums[albumid]['title'].encode('UTF-8'),
        "/".join(albums[albumid]['artist']).encode('UTF-8'),
        albumid
    )

def play_ban(songid, songs):
    """Confirm ban"""
    logger.debug('call function play_ban')
    print
    print "   The song \"{}\" by {} [{}] has been banned forever.".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8)'),
        songid
    )

def play_favorite(songid, songs):
    """Confirm favorite"""
    logger.debug('call function play_favorite')
    print
    print "   The song \"{}\" by {} [{}] is now a favorite.".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8)'),
        songid
    )

def play_skip(songid, songs):
    """Confirm skip"""
    logger.debug('call function play_skip')
    print
    print "   You just have skipped the song \"{}\" by {} [{}].".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8'),
        songid
    )

# echonest

def en_sync(songids):
    """Display echonest sync results"""
    logger.debug('call function en_sync')
    if len(songids) == 0:
        print "   Echonest tasteprofile up to date."
    else:
        print
        print "   {} song(s) have been updated.".format(len(songids))

def en_display(song):
    """Display echonest song data"""
    logger.debug('call function en_display')
    print
    print "\"{}\" by {}".format(
        song['song_name'].encode('UTF-8'),
        song['artist_name'].encode('UTF-8')
    )
    print
    print "   Echonest ID:         {}".format(song['song_id'])
    print "   Foreign ID:          {}".format(song['foreign_id'])
    print "   MusicBrainz ID:      {}".format(song['request']['song_id'])
    print
    print "   Date added: {} - Last modified: {}".format(
        song['date_added'], song['last_modified'])
    print
    print "   This song has been played {} time(s) and skipped {} time(s)".format(
        song.get('play_count', 0), song.get('skip_count', 0)
    )
    print "   Rating: {} - Favorite: {} - Banned: {}".format(
        song.get('rating', 0),
        song.get('favorite', False),
        song.get('banned', False)
    )
    print
    print "   Song type(s):        {}".format(", ".join(song['song_type']))
    print
    print "   Song currency:       {}".format(song['song_currency'])
    print "   Song hotttnesss:     {}".format(song['song_hotttnesss'])
    print
    print "   Artist familiarity:  {}".format(song['artist_familiarity'])
    print "   Artist hotttnesss:   {}".format(song['artist_hotttnesss'])
    print "   Artist discovery:    {}".format(song['artist_discovery'])

def en_info(catalog):
    """Display echnonest tasteprofile info"""
    logger.debug('call function en_info')
    print
    print "   Songs resolved/total: {} / {}".format(catalog['resolved'], catalog['total'])
    print "   ID:                   {}".format(catalog['id'])
    print "   Date created:         {}".format(catalog['created'])
    print "   Pending tickets:      {}".format(" / ".join(
        [pending_ticket['ticket_id'] for pending_ticket in catalog['pending_tickets']])
    )

def en_sure_delete_tasteprofile(api_key, profile_id):
    """Warning before taste profile deletion."""
    logger.debug('call function sure_delete_tasteprofile')
    print
    print "WARNING: you are about to delete your taste profile. All your"
    print "favorite, ban and skip data will be lost. playcount and rating"
    print "data are safe in your Kodi library."
    print
    rep = raw_input("Are you sure (Y/c)? ")
    return rep == 'Y'

def en_delete():
    """Print delete output"""
    logger.debug('call function en_delete')
    print
    print "   Your echonest profile has been deleted."