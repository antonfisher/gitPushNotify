#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anton Fischer"
__date__ = "$30.08.2011 23:33:33$"

import commands

class gitPushNotify:
    useNotifySend = True
    useSound = False
    repositoryPath = '';

    NOTIFY_TYPE_INFO       = 'info'
    NOTIFY_TYPE_WARNING    = 'warning'
    NOTIFY_TYPE_ERROR      = 'error'

    def __init__(self, repositoryPath):
        if (repositoryPath):
            self.repositoryPath = repositoryPath
        pass

    def fireNotify(self, msg = "", title = "GitPushNotify", notifyType = NOTIFY_TYPE_INFO):
        """
        Fire notify action
        """
        if (self.useNotifySend):
            level = 'normal'
            icon = self.getSystemIcon()
            commands.getstatusoutput('notify-send -u "%s" -i "%s" "%s" "%s"' % (level, icon, title, msg))

        if (self.useSound):
            # play sound
            pass

        return self

    def getSystemIcon(self):
        """
        Get system icon path
        """
        return None

    def getGitLog(self):
        """
        Get git log as string
        """
        commands.getoutput('cd %s' % self.repositoryPath)
        sourceOutput = commands.getoutput(
            'git whatchanged -10 --date=raw --date-order --pretty=format:"%H %n%an %n%ae %n%at %n%cn %n%ce %n%ct %n%s"'
        )
        #arrOutput = sourceOutput.split("\n")
        self.fireNotify(sourceOutput)

if __name__ == "__main__":
    c = gitPushNotify('/home/lenin/python/git-push-notify')
    c.getGitLog()
    #c.fireNotify("pip")