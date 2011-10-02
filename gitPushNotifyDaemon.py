#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Anton Fischer <a.fschr@gmail.com>'
__date__ = '$30.08.2011 23:33:33$'

import sys, time, tempfile
import gitPushNotify
from daemon import Daemon
 
class GitPushNotifyDaemon(Daemon):
    def run(self):
        c = gitPushNotify.GitPushNotify()
        while True:
            c.check()
            time.sleep(60)

if __name__ == '__main__':
    daemon = GitPushNotifyDaemon(tempfile.gettempdir() + '/daemonGitPushNotify.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'Daemon started!'
            daemon.start()
        elif 'stop' == sys.argv[1]:
            print 'Daemon stopped!'
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            print 'Daemon restarted!'
            daemon.restart()
        else:
            print 'Unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)