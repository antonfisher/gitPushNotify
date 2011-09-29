#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Anton Fischer <a.fschr@gmail.com>'
__date__ = '$30.08.2011 23:33:33$'

class GitParser:
    """
    Class for raw git console output
    """
    def __init__(self, rawText = ''):
        self.rawText = rawText
        self.listChanges = []

    def setRawText(self, text):
        """
        Raw text setter
        """
        self.rawText = text
        return self

    def getChangesList(self):
        listSource = self.rawText.split('\n')
        listGroup = {}
        i = 0
        for string in listSource:
            if string != '':
                if listGroup.has_key(i):
                    listGroup[i].append(string)
                else :
                    listGroup[i] = [string]
            else:
                i += 1

        listChanges = []
        for group in listGroup.values():
            if len(group) < 4:
                continue
            change = {
                'id':       group[0],
                'author':   group[1],
                'email':    group[2],
                'time':     group[3],
                'message':  group[4],
                'files':    [],
                }
            for i in range(5, len(group)):
                change['files'].append(self._getFileNameStatus(group[i]))
            listChanges.append(change)
        return listChanges

    def _getFileNameStatus(self, text):
        """
        ":000000 100644 0000000... bd725c6... A  daemon.py" -> "A daemon.py"
        """
        tmp = text.split("\t")
        return  tmp[0].split().pop() + ' ' + tmp[1]
