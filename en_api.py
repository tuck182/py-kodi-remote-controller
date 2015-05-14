
#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2015 Arn-O. See the LICENSE file at the top-level directory of this
# distribution and at
# https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE.

'''
Module of functions for echonest API management.
'''

import requests
import logging

def echonest_favorite(api_key, profile_id, song_id):
    '''Make a song favorite in echonest tasteprofile'''
    logging.debug('call set_echonest_favorite')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/favorite'
    payload = {"api_key": api_key,
              "id": profile_id,
              "item": str(song_id)
              }
    r = requests.get(url, params=payload)
    logging.debug('URL: %s', r.url)
    logging.debug('return: %s', r.text)

def echonest_skip(api_key, profile_id, song_id):
    '''Skip a song favorite in echonest taste profile'''
    logging.debug('call set_echonest_skip')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/skip'
    payload = {"api_key": api_key,
              "id": profile_id,
              "item": str(song_id)
              }
    r = requests.get(url, params=payload)
    logging.debug('URL: %s', r.url)
    logging.debug('return: %s', r.text)

def echonest_info(api_key, profile_id):
    '''Display info about echonest profile'''
    logging.debug('call echonest_info')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/profile'
    payload = {"api_key": api_key,
              "id": profile_id
              }
    r = requests.get(url, params=payload)
    logging.debug('URL: %s', r.url)
    logging.debug('return: %s', r.text)
    ret = r.json()
    return ret['response']['catalog']

def echonest_read(api_key, profile_id, item_id):
    '''Display dat about a given item'''
    logging.debug('call echonest_read')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/read'
    payload = {
            'api_key': api_key,
            'id': profile_id,
            'item_id': str(item_id)
            }
    r = requests.get(url, params=payload)
    logging.debug('URL: %s', r.url)
    logging.debug('return: %s', r.text)
    ret = r.json()
    return ret['response']['catalog']['items'][0]

def echonest_delete(api_key, profile_id):
    '''Delete echonest tasteprofile'''
    logging.debug('call echonest_delete')
    url = 'http://developer.echonest.com/api/v4/tasteprofile/delete'
    headers = {'content-type': 'multipart/form-data'}
    payload = {"api_key": api_key,
            "id": profile_id
            }
    r = requests.post(url, headers=headers, params=payload)
    #TODO: move to disp function
    print(r.url)
    print(r.text)
