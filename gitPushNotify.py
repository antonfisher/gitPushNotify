#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Anton Fischer <a.fschr@gmail.com>'
__date__ = '$30.08.2011 23:33:33$'

import commands, os, pynotify
from datetime import datetime
import gitParser

class GitPushNotify:
    useNotifySend = True
    useSound = False
    repositoryPath = '';

    NOTIFY_TYPE_INFO       = 'info'
    NOTIFY_TYPE_WARNING    = 'warning'
    NOTIFY_TYPE_ERROR      = 'error'

    def __init__(self, repositoryPath = None):
        if (repositoryPath):
            self.repositoryPath = repositoryPath
        else:
            self.repositoryPath = '/home/lenin/python/git-push-notify'
        self.fireNotify('I am run!')

    def fireNotify(self, msg = '', title = 'GitPushNotify', notifyType = NOTIFY_TYPE_INFO):
        """
        Fire notify action
        """
        if (self.useNotifySend):
            level = 'normal'
            icon = self.getSystemIcon()
            #commands.getstatusoutput('notify-send -u "%s" -i "%s" "%s" "%s"' % (level, icon, title, msg))
            if pynotify.init('icon-summary-body'):
                n = pynotify.Notification(title, msg, icon).show()
            else:
                print 'Notify not supported. You need to install python-notify package first.'

        if (self.useSound):
            # play sound
            pass
        return self

    def getSystemIcon(self):
        """
        Get system icon path
        example: notification-power-disconnected
        """
        return ''

    def getLastCheckTime(self):
        """
        To simplicity, time of last modification of the current file is used as the time of last checking
        """
        lastCheckTime = os.path.getmtime(__file__)
        return datetime.fromtimestamp(lastCheckTime)

    def setLastCheckTime(self, time = None):
        """
        Set time of last checking -> touch file
        """
        commands.getoutput('touch ' + __file__)
        return self

    def getRepositoryPath(self):
        """
        Get repository path
        """
        return self.repositoryPath

    def setRepositoryPath(self, path):
        """
        Set repository path
        """
        self.repositoryPath = path
        return self

    def check(self, lastCheckTime = None, repositoryPath = None):
        """
        Get git log as string
        """
        if (not lastCheckTime):
            lastCheckTime = self.getLastCheckTime()

        if (not repositoryPath):
            repositoryPath = self.getRepositoryPath()

        sourceOutput = commands.getoutput(
            'cd ' + repositoryPath + ' &&'\
            + 'git fetch' + ' &&'\
            + 'git whatchanged origin/master -10 --date=raw --date-order --pretty=format:"%H %n%cn %n%ce %n%ct %n%s"'
        )
        parser = gitParser.GitParser(sourceOutput)
        listChanges = parser.getChangesList()
        message = ''
        countCommits = 0

        for item in listChanges:
            commitTime = datetime.fromtimestamp(int(item['time']))
            if (commitTime >= lastCheckTime or True):
                message += '...\n' + commitTime.strftime('%x %X') + '\n' + item['author'] + ' &lt;' + item['email']\
                           + '&gt;\n' + item['message'] + '\n'
                countCommits += 1

        if (countCommits > 0):
            message += '...\n%s new commit(s)\n\n' % countCommits

            self.fireNotify(message)
            self.setLastCheckTime()

        if (len(message) > 0):
            return self

if __name__ == '__main__':
    c = GitPushNotify()
    c.check()
