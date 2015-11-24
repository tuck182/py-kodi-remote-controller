#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

"""
Module of display function for PyKodi.
"""

import datetime
import logging

logger = logging.getLogger(__name__)


#TODO: song_ids and not songs_id + just albums or songs
def albums_index(albums_id, kodi_albums):
    '''Display albums list from internal index'''
    logger.debug('call disp_albums_index')
    print
    for i, album_id in enumerate(albums_id):
        print ("%02i. %s by %s (%s) [%i]") % (
                i + 1,
                kodi_albums[album_id]['title'],
                kodi_albums[album_id]['artist'],
                kodi_albums[album_id]['year'],
                album_id )
    print
    print "Total number of albums: %i" % len(kodi_albums)
    print

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
                songs[songid]['title'],
                "/".join(songs[songid]['artist']),
                songs[songid]['year'],
                songid
            )
    else:
        print "\t[playlist empty]"

def echonest_info(catalog):
    """Display echnonest tasteprofile info"""
    logger.debug('call echonest_info')
    print
    print "\tTotal/resolved:{}/{}".format(catalog['total'], catalog['resolved'])
    print "\tID: {}".format(catalog['id'])
    print "\tDate created: {}".format(catalog['created'])
    print "\tPending tickets:".format("/".join(catalog['pending_tickets']))

def now_playing(item, properties):
    '''Display the now playing part of display_what'''
    print
    #TODO: merge somehow with songs_display 
    if item:
        disp_rating = '.....'
        for i in range(item['rating']):
            disp_rating[i] = '*'
        print 'Now Playing:'
        print
        print "%s - %s (%s)" % (item['artist'][0], item['album'], item['year'])
        print "   %s - [%s]" % (item['title'], disp_rating)
        print "   %02d:%02d:%02d / %02d:%02d:%02d - %i %%" % (
            properties['time']['hours'],
            properties['time']['minutes'],
            properties['time']['seconds'],
            properties['totaltime']['hours'],
            properties['totaltime']['minutes'],
            properties['totaltime']['seconds'],
            properties['percentage'] )
    else:
        print "[not playing anything]"

def next_playing(properties, items):
    '''Display the next playing part of display_what'''
    print
    if properties:
        print "(%i / %i) - Next: %s - %s" % (
                properties['position'] + 1,
                len(items),
                items[properties['position'] + 1]['artist'][0],
                items[properties['position'] + 1]['title'] )
        print

def skip(song_id, songs):
    '''Confirm skip'''
    print "You just have skipped the song \"%s\" by %s [%i]." % (
            songs[song_id]['title'], songs[song_id]['artist'], song_id)

def favorite(song_id, songs):
    '''Confirm favorite'''
    print "The song \"%s\" by %s [%i] is now a favorite." % (
            songs[song_id]['title'], songs[song_id]['artist'], song_id)

def play_album(album_id, albums):
    '''Confirm play album'''
    print "Let's play the album \"%s\" by %s [%i]." % (
            albums[album_id]['title'], albums[album_id]['artist'], album_id)

def add_album(album_id, albums):
    '''Confirm add album'''
    print "Let's add the album \"%s\" by %s [%i]." % (
            albums[album_id]['title'], albums[album_id]['artist'], album_id)

def play_song(song_id, songs):
    '''Confirm play song'''
    print "Let's play the song \"%s\" by %s [%i]." % (
            songs[song_id]['title'], songs[song_id]['artist'], song_id)

def add_song(song_id, songs):
    '''Confirm add song'''
    print "Let's add the song \"%s\" by %s [%i]." % (
            songs[song_id]['title'], songs[song_id]['artist'], song_id)

def echonest_read(song_data):
    '''Display echonest song data'''
    # clean display
    if 'rating' in song_data:
        rating = song_data['rating']
    else:
        rating = 0
    if 'play_count' in song_data:
        play_count = song_data['play_count']
    else:
        play_count = 0
    if 'skip_count' in song_data:
        skip_count = song_data['skip_count']
    else:
        skip_count = 0
    favorite = 'favorite' in song_data
    banned = 'banned' in song_data
    # output
    print "\"%s\" by %s" % (song_data['song_name'], song_data['artist_name'])
    print
    print "   Echonest ID: \t%s" % song_data['song_id']
    print "   Foreign ID: \t\t%s" % song_data['foreign_id']
    print "   MusicBrainz ID: \t%s" % song_data['request']['song_id']
    print
    print "   Date added: %s - Last modified: %s" % (
            song_data['date_added'], song_data['last_modified'])
    print
    print "   This song has been played %i time(s) and skipped %i time(s)" % (
            play_count, skip_count)
    print "   Rating: %s - Favorite: %s - Banned: %s" % (
            rating, favorite, banned)
    print
    print "   Song type(s): %s" % (", ".join(song_data['song_type']))
    print
    print "   Song currency: \t%s" % (song_data['song_currency'])
    print "   Song hotttnesss: \t%s" % (song_data['song_hotttnesss'])
    print
    print "   Artist familiarity: \t%s" % (song_data['artist_familiarity'])
    print "   Artist hotttnesss: \t%s" % (song_data['artist_hotttnesss'])
    print "   Artist discovery: \t%s" % (song_data['artist_discovery'])

# prompt for confirmation

def validate_playlist():
    '''Request what should be done with a playlist proposal.'''
    print
    rep = raw_input(
            "What now? (P)lay or (R)egenerate? Anything else to cancel: ")
    return rep.lower()

def sure_delete_tasteprofile(api_key, profile_id):
    """Warning before taste profile deletion."""
    print
    print "WARNING: you are about to delete your taste profile. All your"
    print "favorite, ban and skip data will be lost. playcount and rating"
    print "data are safe in your Kodi library."
    print
    rep = raw_input("Are you sure (Y/c)? ")
    return rep == 'Y'

# stub for smart help

def smart_help():
    '''Help messages that make sense.'''
    # welcome message
    print
    print "For a quick start, try play_album"
    print
