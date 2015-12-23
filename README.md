py-kodi-remote-controller
=========================

Kodi remote controller module written in Python

## Summary

Initially developped as a simple command line client, PyKodi is now a standalone module that could be used to develop Kodi clients in Python. PyKodi allows you to do many operations on your audio library, like searching for songs and albums, creating playlist, starting or stopping the player (only audio controls are provided).

In some specific context, it would be great to control Kodi from a terminal, wouldn't it? Let's say that you are coding something and want to play some background music. The ``cmd`` client is here for that. This client provides a command line interface to the PyKodi module.

![screenshot](https://raw.githubusercontent.com/Arn-O/py-kodi-remote-controller/master/assets/img/screenshot.png)

The integration with [echonest][echonest] has been introduced with the version 0.2. Echonest is the recommendation engine that powers Spotify. This feature will allow you to create instantly smart playlists, tailored to your tastes. Read [this blog post][variogr.am] to learn more about echonest and how it works.

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

No Kodi params file found, this is probably the first launch. Check
your Kodi parameters (IP, port, user and password) and create an
Echonest account: https://developer.echonest.com/account/register

Read the API key on the Echonest account, it will be requested
later on. When you are ready, try params_create.

(Cmd) 
````

Execute the command ``params_create`` and type in the parameters as requested. The prompt will change to the Kodi system name, meaning that the client has been able to fetch some information. You can skip the echonest API for this quick start.

````
(Cmd) params_create

Kodi server IP: 192.168.1.102
Kodi server port: 8080
Kodi server user: kodi
Kodi server password: abcd1234
Echonest developer key:

(Kodi (OpenELEC)) 
````

The next step is to sync the audio library locally. It is not absolutly mandatory, but it will be far more convenient. For example, you will be able to search for a string in your library instantly, since all your library will be store in memory. This has to be done for the songs and/or the albums. The sync process can take several minutes if your library is large.

````
(Kodi (OpenELEC)) albums_sync

Albums: 100% [####################################] (1055 in 1055) Time: 0:00:09

(Kodi (OpenELEC)) songs_sync

Songs: 100% [###################################] (15165 in 15165) Time: 0:03:13

   A full scan has been performed.

(Kodi (OpenELEC)) 
````

The library is stored on local files, so the next time that you start the client, there is no need to sync again.

### Let's play something

Search for the string ``lana`` in the albums library with the following command line:

````
(Kodi (OpenELEC)) albums_search lana

   "Born to Die: The Paradise Edition" by Lana Del Rey (2012) [478]
   "Ultraviolence" by Lana Del Rey (2014) [479]
   "Young & Beautiful (remix)" by Lana Del Rey vs. Cédric Gervais (2013) [480]
   "Honeymoon" by Lana Del Rey (2015) [1059]
   
(Kodi (OpenELEC)) 
````

The search is done in the albums titles and artists. The list of hits is displayed with the ``albumid`` in bracket. This ID has to be used to play something. Let's say that you want to play the album ``478``:

````
(Kodi (OpenELEC)) play_albums 478
````

The album ``478`` should now rock the room!

### More features

The ``cmd`` module supports online help and autocompletion. You can find documentation from the ``cmd`` application by itself. The functions are organized by prefix. So just enter the prefix and click on ``tab`` to have a list of available functions:

+ ``params_`` Kodi parameters management and echonest API
+ ``albums_`` albums library management and search
+ ``genres_`` albums genres library management and search 
+ ``songs_`` songs library management and search
+ ``play_`` player start, stop, information and echonest feedback
+ ``playlist_`` playlist management
+ ``echonest_`` echonest integration management

You can update the local library ``rating`` and ``playcounts`` metadata by syncing again the albums and songs library with ``albms_sync`` and ``songs_sync``.

### Smart playlist with echonest

It is great to listening to music that you like by a simple command. This is done by smart playlist generation.

PyKodi has echonest playlists generation enabled. Once your Kodi library has been synced locally,  update your tasteprofile with ``echonest_sync``. At the first call, it will create a catalog, aka a tasteprofile, with all your songs (mind the prerequisites exposed above). Echonest will use this catalog to propose songs that are in your library.

The generation of playlist is based on your listening habits and preferences. So you should regulary update your local library, and update your echonest profile afterwards. Only the songs with an update on the ``rating`` and ``playcounts`` will be updated in echonest (delta sync). The first echonest update can be long, but the following one will be really fast.

````
(Kodi (OpenELEC)) playlist_tasteprofile

   "Postcards From Italy" by Beirut (2006) [1242]
   "Goodnight Moon" by Shivaree (2004) [14099]
   "Complainte de la butte" by Rufus Wainwright (2001) [14260]
   "Heaven Can Wait" by Charlotte Gainsbourg (2009) [2222]
   "Lover, You Should've Come Over" by Jeff Buckley (2004) [5702]
   "My Beloved Monster" by EELS (1997) [3269]
   "Loser" by Beck (1994) [1214]
   "15 Step" by Radiohead (2009) [9967]
   "Goshen" by Beirut (2011) [1253]
   "The Distance" by CAKE (1996) [2128]
   "Do You Realize??" by The Flaming Lips (2002) [12428]
   "Orange Crush" by R.E.M. (2011) [9943]
   "The Universal" by Blur (2000) [1623]
   "Cherokee" by Cat Power (2012) [2195]
   "Homeward Bound" by Simon & Garfunkel (1999) [11072]
````

You can improve further the recommandation system. When a song is playing, make it a favorite with ``play_favorite``, skip it with ``play_skip`` or ban it with ``play_ban``. The commands will update the song metadata in echonest.

### Library updates

The built-in syncing process only support updates on the ``rating`` and ``playcounts``. Also, if new albums are detected, a full sync will be triggered.

After a migration, you may scan your music folder from scratch. As a consequence, the **internal Kodi items ID may change** and PyKodi will not detect it. In this case, you have to delete all the pickle files except ``params.pickle`` and sync again your library. 

## Contributions

Contributions are welcome. You can just post an issue to improve the stability (many improvement items are already logged) or request a new feature, develop a new client, add new features to the module or ine the ``cmd`` client. If the module does not meet your requirement for creating a new client, contact me to see how to make it evolve.

### Hand-on

The code has been deeply refactored to make PyKodi a standalone module. It may not be perfect, but the structure is clean and hopefully readable. The functions interfaces are homogenous.

The module is actually a package with several submodules:

+ ``core`` all the high-level commands to interact with Kodi, usually there is no output
+ ``rpc`` low-level function to call Kodi API
+ ``echonest`` low-level function to call echonest API
+ ``display`` fancy outputs, translate internal variables from the ``core`` module into user-friendly information

### Useful links

Some links to learn more on the Kodi API and what you can do with it:

+ Kodi wiki, ["JSON-RPC API"][api-gen], some general explanations about the API
+ Kodi wiki, ["JSON-RPC API/v6"][api-v6], the full methods list and description
+ Kodi wiki, ["JSON-RPC API/Examples"][api-example], json-rpc examples
+ Python docs, ["18.2. json — JSON encoder and decoder"][python-json], using json in Python

## License

Copyright 2015 Arn-O under the [MIT license][license].

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
