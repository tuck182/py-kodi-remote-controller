py-kodi-remote-controller
=========================

Kodi remote controller module written in Python

## summary

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

If you want to release the full potential of PyKodi, you need to [create an account][echonest-register] on the echonest developper web site and request an API key. You also need to upgrade the rate limit to 120 calls by minute. This is absolutly free of charge.

## Quick start

for the cmd client. read the code to learn how to use the module.

cmd module

generally use id

First step, clone this repository localy. Kodi needs to be configured to accept remote controls. This is done differently based on the transport that you want to use.

Note that this will install the version 0.2, considered as an alpha release (under optimized and full of bugs). Go to the releases a select a beta one if you want more stability.

### More features

online documentation


### library updates

delete the local pickles

### HTTP

This type of transport is the default value.  Here is how to launch the script:

```
$ python pykodi.py 192.168.1.251 -p 8080 -u web_user -pw web_password
```

### TCP

Here is the link to the [official documentation][tcp]. Launch the script with the IP of your Kodi server as a parameter and the ``--tcp`` switch:

```
$ python pykodi.py 192.168.1.251 --tcp
```

### First launch

On the first launch, the program will **sync the Kodi audio library** to local files. This may take some times, but will make further requests in the library very very fast.

If everything runs well, you will now see a prompt with the name of your Kodi server.

From the prompt, use the ``help`` command to have the list of available methods, and help + command to display a usage message. Most of the time, parameters are optional and a random value is used. To play a random album, try:

```
(Kodi (OpenELEC)) play_album
```

## Echonest support

This feature is experimental but promising and delivers great results.

Echnonest support is automatically activated if you give an API key to PyKodi with the ``-enk`` switch. Request you own key on the [registration page][echonest-register]. The standard key is limited to 20 calls by minute, which is really low. You can request an upgrade to 120 calls by minute for free.

The song matching relies heavily on MusicBrainz. Your audio files need to be properly tagged with their MusicBrainzID.

## Usage

### Start arguments

The program uses the ``argparse`` module, so all arguments can be displayed using the ``-h`` option. The verbosity has two levels, try ``-v`` or ``-vv``. The default port for TCP calls is used (9090). If you changed it to something else, or for HTTP transport, try ``-p``.

For HTTP transport, if the authentication is required, use the ``-u`` switch for the user and ``-pw`` for the password.

### User interface

Everything is managed using command line with the ``cmd`` module. This module is really powerful and provides a lot of features to make your user life easier, like auto-completion or online usage. Read the [official documentation][cmd-docs] to learn more. 

This [tutorial][cmd-tutorial] is also of a very good value.

### Let's play something

The full list of methods are displayed with the ``help`` command from the prompt. The first part of name of the methods are meaningful:

+ ``albums_`` various request in the albums library to find something to listen to
+ ``play_`` start or stop the player
+ ``playlist_`` manage your audio playlist

### Local library update

This will be developed in a next version. Just delete the pickle files and start again the program.

Since the version 0.2, the songs audio library is also stored locally. The playcount and rating of each songs can be synced with ``songs_sync``. 

### Generate a personalized playlist

Update your tasteprofile with ``echonest_sync``. This will be used by echonest to identify your listening preferences.

Generate a playlist with ``playlist_tasteprofile`` and play it with ``play_pause``. To improve the recommandations, rate your favorite songs, sync with ``songs_syns`` and update your tasteprofile with ``echonest_sync``.

## Contributions

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

[yatse]: http://yatse.leetzone.org/redmine
[chorus]: https://github.com/jez500/chorus
[http]: http://kodi.wiki/?title=JSON-RPC_API#HTTP
[cmd-tutorial]: http://pymotw.com/2/cmd/
[api-gen]: http://kodi.wiki/?title=JSON-RPC_API
[api-v6]: http://kodi.wiki/index.php?title=JSON-RPC_API/v6
[api-example]: http://kodi.wiki/view/JSON-RPC_API/Examples
[python-json]: http://docs.python.org/2/library/json.html
[cmd-docs]: https://docs.python.org/2/library/cmd.html
[variogr.am]: http://notes.variogr.am/post/37675885491/how-music-recommendation-works-and-doesnt-work
[echonest]: http://the.echonest.com/
[echonest-register]: https://developer.echonest.com/account/register
