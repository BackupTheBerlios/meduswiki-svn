# Author: Edvardas Scerbavicius
# E-mail: edvardas@gmail.com
""" WikiFormatter class
    If you want to implement new Formatter: extend this class and overwrite format method. 
"""
from medus.cfg import Config
import cgi, re;

class WikiFormatter:
    """Formatter for wiki content
       'DataStore' object must be added to Config before, instanciating object of this class
    """
    def __init__(self):
        """Initilize WikiFormatter
           'DataStore' object must be added to Config before, instanciating object of this class
        """
        self.datastore = Config.get('DataStore')
    
    def format(self, s):
        """Return formatted wiki content, (s) - file name"""
        return reduce(lambda s, r: re.sub('(?m)'+r[0], r[1], s),
        (
        # Process headings
        (r'^! (.*)$', '<h1>\g<1></h1>'),
        (r'^!! (.*)$',  '<h2>\g<1></h2>'),
        (r'^!!! (.*)$', '<h3>\g<1></h3>'),
        # {images/img.jpg|alttext}
        (r'\{(([^|]+).(gif|jpg|jpe|jpeg|png))\|([^\}]+)\}', '<img src="\g<1>" alt="\g<2>" border="0" />'),
        # [http://url|Name]
        (r'\[((http|ftp|mailto|news):[^\]]*)\|([^\]]+)\]', '<a href="\g<1>">\g<3></a>'),
        # [?WikiName|Name]
        (r'\[(\?[^\]]*)\|([^\]]+)\]', '<a href="\g<1>">\g<2></a>'),
        # Bold and Italic
        (r'\'{3}(.+?)\'{3}', '<b>\g<1></b>'),
        (r'\'{2}(.+?)\'{2}', '<em>\g<1></em>'),
        # WikiNames example: MedusWiki
        (r'(?<!\!|\"|\>|\#|\=|\/|\?)\b[A-Z][a-z]+([A-Z][a-z]+)+', lambda m:
          ("%s<a href='?%s%s%s'>%s</a>") %
          ((m.group(0), 'wn=', m.group(0),'&amp;job=edit','?'), \
           ('', m.group(0), '','',m.group(0)))
          [self.datastore.exists(m.group(0))]
        ),
        # Lists * ** ***
        (r'^\*\ (.*?)$', '<ul><li>\g<1></li></ul>'),
        (r'^\*\*\ (.*?)$', '<ul><ul><li>\g<1></li></ul></ul>'),
        (r'^\*\*\*\ (.*?)$', '<ul><ul><ul><li>\g<1></li></ul></ul></ul>'),
        (r'<\/ul>\r*(\n)<ul>', '\g<1>'),
        # numbered # ## ###
        (r'^\#\ (.*?)$', '<ol><li>\g<1></li></ol>'),
        (r'^\#\#\ (.*?)$', '<ol><ol><li>\g<1></li></ol></ol>'),
        (r'^\#\#\#\ (.*?)$', '<ol><ol><ol><li>\g<1></li></ol></ol></ol>'),
        (r'<\/ol>\r*(\n)<ol>', '\g<1>'),
        # Preformatted (indent with space)
        (r'^ +(.*)\n', '<pre>\g<0></pre>'),
        # with a subsequent match and replace of
        (r'</pre><pre>', ''),
        # Horizontal rule ----\n   
        (r'-{4,}\r\n', '<hr />'),
        # scheme://url/path
        (r'(?<!\")(ht|f)tp:[^<>"\s]+','<a href="\g<0>">\g<0></a>'),
        # new lines
        (r'\r\n', '<br />'),
        ), cgi.escape(s))
