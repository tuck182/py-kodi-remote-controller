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

def albums_index(albumids, albums):
    """Display albums list from internal index"""
    logger.debug('call disp_albums_index')
    print
    for albumid in albumids:
        print "   \"{}\" by {} ({}) [{}]".format(
                albums[albumid]['title'].encode('UTF-8'),
                "/".join(albums[albumid]['artist']).encode('UTF-8'),
                albums[albumid]['year'],
                albumid
        )

def albums_details(albumid, albums):
    """Display album details from albumid"""
    logger.debug('call albums_details')
    print
    print "\"{}\" by {} ({})".format(
        albums[albumid]['title'],
        "/".join(albums[albumid]['artist']),
        albums[albumid]['year']
    )
    print
    print "   Rating:          {}".format(albums[albumid]['rating'])
    print "   MusicBrainz ID:  {}".format(albums[albumid]['musicbrainzalbumid'])

# songs

def songs_index(songids, songs):
    """Display songs list from internal index"""
    logger.debug('call songs_index')
    print
    for i, songid in enumerate(songids):
        print ("%02i. \"%s\" by %s (%s) [%i]") % (
                i + 1,
                songs[songid]['title'],
                 "/".join(songs[songid]['artist']),
                songs[songid]['year'],
                songid )

def songs_details(songid, songs):
    """Display song details from song id"""
    logger.debug('call songs_details')
    print
    print ('"%s" by %s (%s)') % (
            songs[songid]['title'],
            "/".join(songs[songid]['artist']),
            songs[songid]['year'])
    print "\tDuration: %s" % (
        str(datetime.timedelta(seconds=songs[songid]['duration'])))
    print "\tPlaycount: %i (%i)" % (
            songs[songid]['playcount'],
            songs[songid]['playcount_en'])
    print "\tRating: %i (%i)" % (
            songs[songid]['rating'],
            songs[songid]['rating_en'])
    print "\tMusicBrainz ID: %s" % songs[songid]['musicbrainztrackid']

def songs_info(songs):
    """Display song details from song id"""
    logger.debug('call songs_info')
    print
    print "Total number of songs: %i" % len(songs)
    total_duration = 0
    for songid in songs:
        total_duration += songs[songid]['duration']
    duration_str = str(datetime.timedelta(seconds=total_duration))
    print "Total duration: %s" % duration_str

def songs_sync(f_scan, ru_songsids, pcu_songids):
    """Display result of the songs sync process"""
    logger.debug('call songs_sync')
    print
    if f_scan:
        print "Full scan."
    else:
        print "Delta scan."
        print
        print "\tRatings updated: {}".format(len(ru_songsids))
        print "\tPlay counts updated: {}".format(len(pcu_songids))

# playlist

def playlist_show(position, songids, songs):
    """Display playlist"""
    logger.debug('call playlist_show')
    print
    if songids:
        for i, songid in enumerate(songids):
            if i == position:
                print ">>>",
            print "\t",
            print "{}. \"{}\" by {} ({}) [{}]".format(
                str(i+1).zfill(2),
                songs[songid]['title'].encode('utf-8'),
                "/".join(songs[songid]['artist']).encode('utf-8'),
                songs[songid]['year'],
                songid
            )
    else:
        print "\t[playlist empty]"

def playlist_now_playing(item, properties):
    """Display the now playing part of play_what"""
    print
    if not item:
        print "   [not playing anything]"
        return
    # build rating display
    disp_rating = '.....'
    for i in range(item['rating']):
        disp_rating[i] = '*'
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
    print "Let's play the album \"%s\" by %s [%i]." % (
            albums[albumid]['title'], albums[albumid]['artist'], albumid)

def play_ban(songid, songs):
    """Confirm ban"""
    print
    print "   The song \"{}\" by {} [{}] has been banned forever.".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8)'),
        songid
    )

def play_favorite(songid, songs):
    """Confirm favorite"""
    print
    print "   The song \"{}\" by {} [{}] is now a favorite.".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8)'),
        songid
    )

def play_skip(songid, songs):
    """Confirm skip"""
    print
    print "   You just have skipped the song \"{}\" by {} [{}].".format(
        songs[songid]['title'].encode('UTF-8'),
        "/".join(songs[songid]['artist']).encode('UTF-8'),
        songid
    )

# echonest

def en_sync(songids):
    """Display echonest sync results"""
    if len(songids) == 0:
        print "Echonest tasteprofile up to date."
    else:
        print
        print "{} song(s) have been updated.".format(len(songids))

def en_display(song_data):
    """Display echonest song data"""
    print
    print "\"{}\" by {}".format(
        song_data['song_name'].encode('UTF-8'),
        song_data['artist_name'].encode('UTF-8')
    )
    print
    print "\tEchonest ID: \t\t{}".format(song_data['song_id'])
    print "\tForeign ID: \t\t{}".format(song_data['foreign_id'])
    print "\tMusicBrainz ID: \t{}".format(song_data['request']['song_id'])
    print
    print "\tDate added: {} - Last modified: {}".format(
        song_data['date_added'], song_data['last_modified'])
    print
    print "\tThis song has been played {} time(s) and skipped {} time(s)".format(
        song_data.get('play_count', 0), song_data.get('skip_count', 0))
    print "\tRating: {} - Favorite: {} - Banned: {}".format(
        song_data.get('rating', 0),
        song_data.get('favorite', False),
        song_data.get('banned', False))
    print
    print "\tSong type(s): {}".format(", ".join(song_data['song_type']))
    print
    print "\tSong currency: \t\t{}".format(song_data['song_currency'])
    print "\tSong hotttnesss: \t{}".format(song_data['song_hotttnesss'])
    print
    print "\tArtist familiarity: \t{}".format(song_data['artist_familiarity'])
    print "\tArtist hotttnesss: \t{}".format(song_data['artist_hotttnesss'])
    print "\tArtist discovery: \t{}".format(song_data['artist_discovery'])

def en_info(catalog):
    """Display echnonest tasteprofile info"""
    logger.debug('call en_info')
    print
    print "\tTotal songs/resolved: {} / {}".format(catalog['total'], catalog['resolved'])
    print "\tID: {}".format(catalog['id'])
    print "\tDate created: {}".format(catalog['created'])
    print "\tPending tickets: {}".format(" / ".join(
        [pending_ticket['ticket_id'] for pending_ticket in catalog['pending_tickets']])
    )

def en_sure_delete_tasteprofile(api_key, profile_id):
    """Warning before taste profile deletion."""
    print
    print "WARNING: you are about to delete your taste profile. All your"
    print "favorite, ban and skip data will be lost. playcount and rating"
    print "data are safe in your Kodi library."
    print
    rep = raw_input("Are you sure (Y/c)? ")
    return rep == 'Y'

def en_delete():
    """Print delete output"""
    print
    print "Your echonest profile has been deleted."