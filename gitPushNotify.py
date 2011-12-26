#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Anton Fischer <a.fschr@gmail.com>'
__date__ = '$30.08.2011 23:33:33$'

import commands, os, pynotify, logging, tempfile, ConfigParser, sys
from datetime import datetime
import gitParser

class GitPushNotify:
    useNotifySend       = True
    useNotifySound      = False #no yet
    repositoryPath      = None
    repositoryBranch    = 'origin/master'
    daemonTimeout       = 60 #sec

    def __init__(self):
        # log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/gitPushNotify.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s %(levelname)s: %(message)s',
                            datefmt = '%Y-%m-%d %I:%M:%S')
        logging.info('Daemon start')

        # read config
        config = ConfigParser.ConfigParser()
        configPath = os.path.dirname(__file__) + '/config.cfg'
        if os.path.exists(configPath):
            config.read(configPath)
        else:
            self.fireNotify('File "config.cfg" does not exist. Daemon stopped.')
            sys.exit(2)

        # -- repository path
        if config.has_option('git', 'repository'):
            self.repositoryPath = config.get('git', 'repository')
        else:
            message = 'Is not define repository path in "config.cfg". Daemon stopped.'
            self.fireNotify(message)
            logging.error(message)
            sys.exit(2)

        # -- repository branch
        if config.has_option('git', 'branch'):
            self.repositoryBranch = config.get('git', 'branch')

        # -- daemon timeout
        if config.has_option('daemon', 'timeout'):
            self.daemonTimeout = config.getint('daemon', 'timeout')

        # -- use notify-send
        if config.has_option('notify', 'useNotifySend'):
            self.useNotifySend = config.getboolean('notify', 'useNotifySend')

        # -- use notify-sound
        if config.has_option('notify', 'useNotifySound'):
            self.useNotifySound = config.getboolean('notify', 'useNotifySound')

        # start notify
        self.fireNotify('Start!')

    def fireNotify(self, msg = '', title = 'GitPushNotify'):
        """
        Fire notify action
        """
        logging.info('Called fireNotify()')
        if (self.useNotifySend):
            #commands.getstatusoutput('notify-send -u "%s" -i "%s" "%s" "%s"' % (level, icon, title, msg))
            if pynotify.init('icon-summary-body'):
                pynotify.Notification(title, msg, self.getSystemIcon()).show()
            else:
                print 'Notify not supported. You need to install python-notify package first.'

        if (self.useNotifySound):
            # play sound
            pass

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

    def getDaemonTimeout(self):
        """
        Get daemon checking timeout
        """
        return self.daemonTimeout

    def check(self, lastCheckTime = None, repositoryPath = None):
        """
        Get git log as string
        """
        logging.info('Called check()')
        if (not lastCheckTime):
            lastCheckTime = self.getLastCheckTime()

        if (not repositoryPath):
            repositoryPath = self.getRepositoryPath()

        #sourceOutput = commands.getoutput(
        sourceOutput = subprocesses.check_output(
            'cd ' + repositoryPath + ' &&'\
            + ' git fetch' + ' &&'\
            + ' git whatchanged ' + self.repositoryBranch + ' -10 --date=raw --date-order --pretty=format:"%H %n%cn %n%ce %n%ct %n%s"'
        )
        logging.debug('sourceOutput: %s', sourceOutput)
        parser = gitParser.GitParser(sourceOutput)
        listChanges = parser.getChangesList()
        message = ''
        countCommits = 0

        logging.info('Count commits: %s', len(listChanges))
        for item in listChanges:
            commitTime = datetime.fromtimestamp(int(item['time']))
            if (commitTime >= lastCheckTime):
                message += '...\n' + commitTime.strftime('%x %X') + '\n' + item['author'] + ' &lt;' + item['email']\
                           + '&gt;\n' + item['message'] + '\n'
                countCommits += 1

        if (countCommits > 0):
            logging.info('Count new commits: %s', countCommits)
            message += '...\n%s new commit(s)\n\n' % countCommits

            self.fireNotify(message)
            self.setLastCheckTime()

        logging.info('End check()')
        return self

if __name__ == '__main__':
    c = GitPushNotify()
    c.check()
