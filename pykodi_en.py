
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
import logging

logger = logging.getLogger(__name__)

PROFILE_NAME = 'PyKodi library'

def tasteprofile_delete(api_key, profile_id):
    """Delete echonest tasteprofile"""
    logger.debug('call echonest_delete')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/delete'
    headers = {'content-type': 'multipart/form-data'}
    payload = {
        'api_key': api_key,
        'id': profile_id
    }
    r = requests.post(url, headers=headers, params=payload)
    ret = r.json()
    return ret['response']['status']

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
    return ret['response']['catalog']

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
