
#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

"""
Module of functions for echonest API management.
"""

import requests
import json
import logging

logger = logging.getLogger(__name__)

PROFILE_NAME = 'PyKodi library'

def tasteprofile_create(api_key):
    """Create an echonest tasteprofile"""
    logger.debug('call tasteprofile_create')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/create'
    headers = {'content-type': 'multipart/form-data'}
    payload = {
        'api_key': api_key,
        'name': PROFILE_NAME,
        'type': 'general'
    }
    r = requests.post(url, headers=headers, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)

def tasteprofile_delete(api_key, profile_id):
    """Delete echonest tasteprofile"""
    logger.debug('call tasteprofile_delete')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/delete'
    headers = {'content-type': 'multipart/form-data'}
    payload = {
        'api_key': api_key,
        'id': profile_id
    }
    r = requests.post(url, headers=headers, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)

def tasteprofile_profile_name(api_key):
    """Get profile info by name"""
    logger.debug('call tasteprofile_profile_name')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/profile'
    payload = {
        'api_key': api_key,
        'name': PROFILE_NAME
    }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)
    ret = r.json()
    return ret['response']

def tasteprofile_profile_id(api_key, profile_id):
    """Get profile info by id"""
    logger.debug('call tasteprofile_profile_id')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/profile'
    payload = {
        'api_key': api_key,
        'id': profile_id
    }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)
    ret = r.json()
    return ret['response']['catalog']

def tasteprofile_read(item_id, api_key, profile_id):
    """Display dat about a given item"""
    logger.debug('call echonest_read')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/read'
    payload = {
            'api_key': api_key,
            'id': profile_id,
            'item_id': item_id,
            'bucket': [
                'artist_discovery', 'artist_familiarity', 'artist_hotttnesss',
                'song_currency', 'song_hotttnesss', 'song_type',
                ]
            }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)
    ret = r.json()
    return ret['response']['catalog']['items'][0]

def tasteprofile_status(ticket, api_key):
    """Check tasteprofile status update"""
    logger.debug('call tasteprofile_profile_id')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/status'
    payload = {
        'api_key': api_key,
        'ticket': ticket
    }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)

def tasteprofile_update(items, api_key, profile_id):
    """Batch update of items"""
    logger.debug('call tasteprofile_update')
    # crunch items into a single command
    command = []
    for item_id in items:
        command.append({
            'action': 'update',
            'item': {
                'item_id': item_id,
                'song_id': items[item_id]['song_id'],
                'rating': items[item_id]['rating'],
                'play_count': items[item_id]['play_count']
            }
        })
    url = 'http://developer.echonest.com/api/v4/tasteprofile/update'
    headers = {'content-type': 'multipart/form-data'}
    payload = {
        'api_key': api_key,
        'id': profile_id,
        'data': json.dumps(command)
    }
    r = requests.post(url, headers=headers, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)

#TODO: rename to tasteprofile in place of echonest
def echonest_favorite(api_key, profile_id, song_id):
    '''Make a song favorite in echonest tasteprofile'''
    logger.debug('call set_echonest_favorite')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/favorite'
    payload = {"api_key": api_key,
              "id": profile_id,
              "item": str(song_id)
              }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)

def echonest_skip(api_key, profile_id, song_id):
    '''Skip a song favorite in echonest taste profile'''
    logger.debug('call set_echonest_skip')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/skip'
    payload = {"api_key": api_key,
              "id": profile_id,
              "item": str(song_id)
              }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)

def echonest_read(api_key, profile_id, item_id):
    '''Display dat about a given item'''
    logger.debug('call echonest_read')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/read'
    payload = {
            'api_key': api_key,
            'id': profile_id,
            'item_id': str(item_id),
            'bucket': [
                'artist_discovery', 'artist_familiarity', 'artist_hotttnesss',
                'song_currency', 'song_hotttnesss', 'song_type',
                ]
            }
    r = requests.get(url, params=payload)
    logger.debug('URL: %s', r.url)
    logger.debug('return: %s', r.text)
    ret = r.json()
    return ret['response']['catalog']['items'][0]

def echonest_delete(api_key, profile_id):
    '''Delete echonest tasteprofile'''
    logger.debug('call echonest_delete')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/delete'
    headers = {'content-type': 'multipart/form-data'}
    payload = {"api_key": api_key,
            "id": profile_id
            }
    r = requests.post(url, headers=headers, params=payload)
    #TODO: move to disp function
    print(r.url)
    print(r.text)
