#!/usr/bin/env python
# Copyright (C) 2004 Edvardas Scerbavicius <edvardas@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, visit the following URL:
# http://www.gnu.org/copyleft/gpl.html
"""
MedusWiki
http://meduswiki.berlios.de/
"""
import os, os.path, cgi, traceback, sys
sys.path.append('lib')
from medus.data.SimpleDataStore import SimpleDataStore
from medus.content.WikiFormatter import WikiFormatter
from medus.cfg import Config

#<Configuration>
# possible modes are: 'simple', 'zpt', 'xtm'
mode = 'xtm'

cfg = {} # configuration dict
cfg['encoding'] = 'utf-8' # 'iso-8859-13'

svnrepos = 'svn://svn.berlios.de/meduswiki/trunk'

cfg['version'] = os.popen("svnversion . %s" % svnrepos).read()
cfg['link'] = 'http://meduswiki.berlios.de/'
cfg['logo'] = 'http://meduswiki.berlios.de/medus.png'
cfg['css'] = 'http://meduswiki.berlios.de/meduswiki.css'

cfg['data_path'] = 'data'
cfg['content_path'] = os.path.join(cfg['data_path'], 'content')
cfg['xtm_path'] = os.path.join(cfg['data_path'], 'topicmap.xml')
cfg['zpt_path'] = os.path.join('templates', mode)
#</Configuration>
Config.adddict(cfg)


def main(fields):
    """(fields) - dict of HTTP pairs"""
    sys.stderr = sys.stdout
    print "Content-type: text/html; charset=%s\r\n" % cfg['encoding']

    try:

        wn = fields.get('wn') or os.getenv("QUERY_STRING") or ''
        # if wn=WikiName is given, then this one is used, if not, then checks for cgi.py?QUERY_STRING
        # at this moment we have WikiName in the variable (wn)

        if wn.isalnum(): # so WikiName as '4Suite' could be used here
            fields['wn'] = wn
        else:
            fields['wn'] = 'HomePage'

        # create data store and content formatter
        Config.add('DataStore', SimpleDataStore())
        Config.add('ContentFormatter', WikiFormatter())

        # process mode
        if mode == 'simple':
            from medus.page.SimplePageFormatter import SimplePageFormatter
            pagelayout = SimplePageFormatter()

        elif mode == 'zpt':
            from medus.page.ZPTPageFormatter import ZPTPageFormatter
            pagelayout = ZPTPageFormatter()

        elif mode == 'xtm':
            from medus.page.XTMPageFormatter import XTMPageFormatter
            from xtm.Handler import Handler
            Config.add('XTMHandler', Handler(cfg['xtm_path']))
            pagelayout = XTMPageFormatter()
        else:
            raise mode, " is not implemented"

        # process POST query
        if os.getenv("REQUEST_METHOD") == "POST": # this means that FormProcessing must be done
            if mode == 'simple' or mode == 'zpt' :
                from medus.form.SimpleFormProcessor import SimpleFormProcessor
                formproc = SimpleFormProcessor()
            elif mode == 'xtm':
                from medus.form.XTMFormProcessor import XTMFormProcessor
                formproc = XTMFormProcessor()
               
            formproc.process(fields)

        print pagelayout.getpage(fields)

    except:
        print "\n\n<pre>"
        traceback.print_exc()


if __name__=="__main__":
    # Leave out the "keep_blank_values" bit to filter out empty fields
    cgifields = cgi.FieldStorage(keep_blank_values=1)
    fields = {}

    for key in cgifields.keys():
        if type(cgifields[key]) == type([]):
            fields[key] = [i.value for i in cgifields[key]]
        else:
            fields[key] = cgifields[key].value
                                         
    main(fields)
