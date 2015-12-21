py-kodi-remote-controller
=========================

Kodi remote controller module written in Python

## Summary

Options to remote control Kodi are numerous, you can use mobile apps ([Yatse][yatse] is a great one), web UI (in this category I recommend [chorus][chorus]) and many more way. In some specific context (let's say you are dealing with several terminals), it is great to control it from a terminal, and PyKodi does it. Initially developped as a simple client, it is now a standalone module that could be used to develop new clients in Python. Only the audio controls are covered.

The ``cmd`` client is ready to use. It allows you to do many operations on your audio library, like searching for songs and albums, creating playlist, starting or stopping the player.

The integration with [echonest][echonest] has been introduced with the version 0.2. Echonest is the recommendation engine that powers Spotify. This feature will allow you to create instantly smart playlists, tailored for your tastes. Read [this blog post][variogr.am] to learn more about echonest and how it works.

## Installation and setup

### Enable JSON-RPC in Kodi

Make sure to activate the communication interface in Kodi. Have a look at the official [documentation][http] to activate the HTTP transport. As a result, you should now know the IP, port, user and password of the Kodi web interface. Those information will have to be entered in the client.

The TCP transport is no longer supported, but could be introduced again later on.

### PyKodi

Simple and straightforward, just clone this repository on your workstation. The code is based on standard modules or best of class external modules (mainly ``requests`` for the API calls).

### Echonest

If you want to release the full potential of PyKodi, you need to [create an account][echonest-register] on the echonest developper web site and request an API key. You also need to upgrade the rate limit to 120 calls by minute (this rate is used by the sync process). The echonest integration relies heavily on clean MusicBrainz metadata. The matching with the echonest database is based on the MusicBrainz ID. Without a proper tagging, you will not be able to use this feature.

This service is absolutly free of charge.

## Quick start

This part describes how to use the ``cmd`` client. If you are interested in the module only, read the code of the ``cmd`` client which is basically a wrapper of the module. ``cmd`` is a line-oriented command interpreter. Considering reading a [tutorial][cmd-tutorial] or the [Python docs][cmd-docs] to learn more on how to use it. It notably supports online help and auto-completion.

### General usage

In the ``cmd`` client, albums and songs are identify with their internal ID, respectively ``albumid`` and ``songid``. To play an album, you have to request to play the album's ID. The application provides seach functions to identify easily the items that you want to play. The IDs is also displayed in all outputs in brackets.

### First start

From the repository folder, call the client. You will see the default ``cmd`` prompt, with a banner requesting to enter the Kodi parameters.

````
$ python pykodi_cmd.py
(cmd) 
````

Execute the command ``params_inputs`` and type in the parameters as requested. The prompt will change to the Kodi system name, meaning that the client has been able to fetch some information. You can skip the echonest API for this quick start.

````
(xxx) params_inputs
````

The next step is to sync the audio library locally. It is not absolutly mandatory, but it will be far more convenient. This has to be done for the songs and the albums. The sync process can take several minutes if your library is large.

````
(xxx) albums_sync
(xxx) songs_sync
````

### Let's play something

Search for the album '25'.

### More features

online documentation

+ ``params_``
+ ``albums_`` various request in the albums library to find something to listen to
+ ``play_`` start or stop the player
+ ``playlist_`` manage your audio playlist

sync again the songs

### Smart playlist with echonest

Update your tasteprofile with ``echonest_sync``. Create a catalog to scope the recommendation.

Update regularly.

This will be used by echonest to identify your listening preferences.

make favorite, skip and ban.

### Library updates

delete the local pickles

## Contributions

An issue in the bug tracker is already great.

### Hand-on

Contributions are welcome and easy.

The code is far from stable, if you face any trouble, post an issue in the GitHub tracking tool. New features can be requested in the bug tracker either. If you want to provide new features by yourself, submit a pull request.

The program can be started in a highly verbose mode with the ``-vv`` argument. All API commands and returns will then be displayed. Use the methods ``call_api`` and ``display_result`` for wrapping new command.

module structure

### Useful links

+ Kodi wiki, ["JSON-RPC API"][api-gen], some general explanations about the API
+ Kodi wiki, ["JSON-RPC API/v6"][api-v6], the full methods list and description
+ Kodi wiki, ["JSON-RPC API/Examples"][api-example], json-rpc examples
+ Python docs, ["18.2. json — JSON encoder and decoder"][python-json], using json in Python

## License

Copyright 2015 Arn-O under the [MIT license][license].

[yatse]: http://yatse.leetzone.org/redmine
[chorus]: https://github.com/jez500/chorus

[http]: http://kodi.wiki/?title=JSON-RPC_API#HTTP
[api-gen]: http://kodi.wiki/?title=JSON-RPC_API
[api-v6]: http://kodi.wiki/index.php?title=JSON-RPC_API/v6
[api-example]: http://kodi.wiki/view/JSON-RPC_API/Examples

[python-json]: http://docs.python.org/2/library/json.html
[cmd-docs]: https://docs.python.org/2/library/cmd.html
[cmd-tutorial]: http://pymotw.com/2/cmd/

[variogr.am]: http://notes.variogr.am/post/37675885491/how-music-recommendation-works-and-doesnt-work
[echonest]: http://the.echonest.com/
[echonest-register]: https://developer.echonest.com/account/register
[license]: https://github.com/Arn-O/py-kodi-remote-controller/blob/master/LICENSE
