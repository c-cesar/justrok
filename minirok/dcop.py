#! /usr/bin/env python
## vim: fileencoding=utf-8
#
# Copyright (c) 2007 Adeodato Simó (dato@net.com.org.es)
# Licensed under the terms of the MIT license.

import qt
import dcopexport

import minirok
from minirok import util

##

class Player(dcopexport.DCOPExObj):

    def __init__(self):
        dcopexport.DCOPExObj.__init__(self, 'player')

        for method, action in [
                ('play', 'action_play'),
                ('pause', 'action_pause'),
                ('playPause', 'action_play_pause'),
                ('stop', 'action_stop'),
                ('next', 'action_next'),
                ('previous', 'action_previous'),
                ('toggleWindow', 'action_toggle_window'),
                ('stopAfterCurrent', 'action_toggle_stop_after_current'),
        ]:
            self.addMethod('void %s()' % method, self.get_action(action))

        self.addMethod('QString nowPlaying()', self.formatted_now_playing)
        self.addMethod('QString nowPlaying(QString)', self.formatted_now_playing)
        self.addMethod('void appendToPlaylist(QStringList)', self.append_to_playlist)

    def formatted_now_playing(self, format=None):
        tags = minirok.Globals.playlist.get_current_tags()

        if not tags:
            formatted = ''
        else:
            if format is not None:
                try:
                    formatted = str(format) % tags
                except (KeyError, ValueError, TypeError), e:
                    formatted = '>> Error when formatting string: %s' % e
            else:
                title = tags['Title']
                artist = tags['Artist']
                if artist is not None:
                    formatted = '%s - %s' % (artist, title)
                else:
                    formatted = title

        return qt.QString(formatted)

    def append_to_playlist(self, qstringlist):
        files = [ util.kurl_to_path(x) for x in qstringlist ]
        minirok.Globals.playlist.add_files_untrusted(files)

    @staticmethod
    def get_action(action_name):
        """Returns the activate() method of a named action."""
        action = minirok.Globals.action_collection.action(action_name)
        if action is None:
            minirok.logger.critical('action %r not found', action_name)
            return lambda: None
        else:
            return action.activate
