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
            print(x)
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
 
_________
 showing $results out of $total-results results
```'''

    parsed = json.dumps(get_urban_definitions(keyword), indent=4)
    final = json.loads(parsed)
    if len(final) > 1:

        key1 = random.randint(0, len(final) - 1)
        key2 = random.randint(0, len(final) - 1)
        if key1 == key2:
            while key2 == key1:
                key2 = random.randint(0, len(final) - 1)
        text_format = text_format.replace('$word', keyword)
        text_format = text_format.replace('$underline', returnDash(keyword))

        text_format = text_format.replace('$definition1', final[key1]['definition'])
        text_format = text_format.replace('$example1', final[key1]['example'])

        text_format = text_format.replace('$definition2', final[key2]['definition'])
        text_format = text_format.replace('$example2', final[key2]['example'])
        text_format = text_format.replace('$total-results', str(len(final)))
        text_format = text_format.replace('$results', '2')
        print(key1, key2)
    elif len(final) == 1:
        text_format = text_format.replace('$word', keyword)
        text_format = text_format.replace('$underline', returnDash(keyword))

        text_format = text_format.replace('$definition1', final[0]['definition'])
        text_format = text_format.replace('$example1', final[0]['example'])

        text_format = text_format.replace('$definition2', 'No Found')
        text_format = text_format.replace('$example2', 'Not Found')
        text_format = text_format.replace('$results', '1')
        text_format = text_format.replace('$total-results', str(len(final)))
    else:
        text_format = 'No results found'
    return text_format
