#!/usr/bin/env python
import os
import pprint

from urllib2 import urlopen
from urllib import urlencode
import sys
import json

# The google translate API can be found here: 
# http://code.google.com/apis/ajaxlanguage/documentation/#Examples

class Translator(object):
    def __init__(self, sourcelang, text):
        self.sourcelang = sourcelang
        self.text = text

    def translate_to(self, targetlang):
        langpair='%s|%s'%(self.sourcelang, targetlang)
        text=self.text
        base_url='http://ajax.googleapis.com/ajax/services/language/translate?'
        params=urlencode( (('v',1.0),
                           ('q',text),
                           ('langpair',langpair),) )
        url=base_url+params
        content=urlopen(url).read()
        try:
            trans_dict=json.loads(content)
        except AttributeError:
            trans_dict=json.read(content)

        try:
            data = trans_dict['responseData']['translatedText']
        except:
            data = None
        return data

class TranslationRoot(object):
    def __init__(self, root_file):
        try:
            os.mkdir("export")
        except:
            pass

        f = open('export/__init__.py', 'w') # just in case
        f.close()
        
        self.root_module = __import__(root_file)
        self.source_lang = self.root_module.lang
        self.translators = {}
        for i in self.root_module.data:
            self.translators[i] = Translator(self.source_lang, self.root_module.data[i])

    def translate_to_module(self, target_lang):
        print 'translating to', target_lang,
        if not os.path.exists('export/%s.py' % target_lang):
            f = open('export/%s.py' % target_lang, 'w')
            f.close()
        
        module = __import__('export.' + target_lang)
        module = getattr(module, target_lang)

        excludes = getattr(module, 'excludes', {})
        new_lang = {}
        
        for i in self.translators:
            if i in excludes:
                pass
            else:
                new_lang[i] = self.translators[i].translate_to(target_lang)

        f = open('export/%s.py' % target_lang, 'w')

        f.write("lang = '%s'\n\n" % target_lang)
        f.write("excludes = ")
        pprint.pprint(excludes, f)

        f.write("\ndata = ")
        pprint.pprint(new_lang, f)

        f.close()
        print 'Done.'

if __name__ == "__main__":
    t = TranslationRoot("root")
    t.translate_to_module('en')
    t.translate_to_module('es')
    t.translate_to_module('de')


