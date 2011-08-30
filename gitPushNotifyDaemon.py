#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Anton Fischer"
__date__ = "$30.08.2011 23:33:33$"

import sys, time, os
from daemon import Daemon
 
class GitPushNotifyDaemon(Daemon):
    def run(self):
        while True:
            level = 'normal'
            icon = ''
            head = 'Good new everyone!'
            msg = 'ok!'
            os.system('notify-send -u "%s" -i "%s" "%s" "%s"' % (level, icon, head, msg))
            time.sleep(30)

if __name__ == "__main__":
    daemon = GitPushNotifyDaemon('/tmp/daemon-example.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
                daemon.start()
        elif 'stop' == sys.argv[1]:
                daemon.stop()
        elif 'restart' == sys.argv[1]:
                daemon.restart()
        else:
                print "Unknown command"
                sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)