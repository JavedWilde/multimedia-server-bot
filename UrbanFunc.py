import requests
import urllib
import json
import random


def get_urban_definitions(word):
    url = 'http://api.urbandictionary.com/v0/define?term=%s' % urllib.parse.quote(word)
    dat = requests.get(url).json()
    return dat['list']


def returnDash(string):
    dash = '---'
    if len(string) > 3:
        for x in string[3:]:
            dash += '-'
    return dash


def runUrban(keyword):
    text_format = '''```asciidoc
$word
$underline

[Definition 1]
 $definition1
[example]
 $example1

[Definition 2]
 $definition2
[example]
 $example2
 
 --------------
 showing 2 out of $result results
```'''

    parsed = json.dumps(get_urban_definitions(keyword), indent=4)
    final = json.loads(parsed)
    if len(final) > 1:
        text_format = text_format.replace('$word', keyword)
        text_format = text_format.replace('$underline', returnDash(keyword))
        key = random.randint(0, len(final)-1)
        text_format = text_format.replace('$definition1', final[key]['definition'])
        text_format = text_format.replace('$example1', final[key]['example'])
        key = random.randint(0, len(final)-1)
        text_format = text_format.replace('$definition2', final[key]['definition'])
        text_format = text_format.replace('$example2', final[key]['example'])
        text_format = text_format.replace('$result', str(len(final)))
    else:
        text_format = 'No results found'
    return text_format
