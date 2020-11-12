import requests
import urllib
import json
import random
from discord import Embed, Color


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


def runUrbanEmbed(keyword):
    urban_dict = dict()
    embed = Embed(title=keyword + '\n\u200b', color=Color.red())

    parsed = json.dumps(get_urban_definitions(keyword), indent=4)
    final = json.loads(parsed)

    if len(final) > 1:
        key1 = random.randint(0, len(final) - 1)
        key2 = random.randint(0, len(final) - 1)
        if key1 == key2:
            while key2 == key1:
                key2 = random.randint(0, len(final) - 1)

        urban_dict['Definition 1'] = final[key1]['definition']
        urban_dict['Example 1'] = final[key1]['example']

        urban_dict['Definition 2'] = final[key2]['definition']
        urban_dict['Example 2'] = final[key2]['example']
        footer = f'_______________________\nShowing 2 out of {str(len(final))} results'

    elif len(final) == 1:
        urban_dict['Definition 1'] = final[0]['definition']
        urban_dict['Example 1'] = final[0]['example']

        footer = f'_______________________\nShowing 1 out of {str(len(final))} results'

    else:
        return Embed(title=keyword + '\u200b',
                     description='No Results Found')

    for key in urban_dict:
        if key[:-2].lower() == 'example':
            embed.add_field(name=str(key[:-2]), value=str(urban_dict.get(key)) + '\n\u200b', inline=False)
        else:
            embed.add_field(name=key, value=str(urban_dict.get(key)), inline=False)
    embed.set_footer(text=footer)

    return embed


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
    urban_dict = dict()
    parsed = json.dumps(get_urban_definitions(keyword), indent=4)
    final = json.loads(parsed)
    if len(final) > 1:

        key1 = random.randint(0, len(final) - 1)
        key2 = random.randint(0, len(final) - 1)
        if key1 == key2:
            while key2 == key1:
                key2 = random.randint(0, len(final) - 1)

        urban_dict['Word'] = keyword
        text_format = text_format.replace('$word', keyword)
        text_format = text_format.replace('$underline', returnDash(keyword))

        text_format = text_format.replace('$definition1', final[key1]['definition'])
        text_format = text_format.replace('$example1', final[key1]['example'])

        urban_dict['Definition 1'] = final[key1]['definition']
        urban_dict['Example 1'] = final[key1]['example']

        text_format = text_format.replace('$definition2', final[key2]['definition'])
        text_format = text_format.replace('$example2', final[key2]['example'])

        urban_dict['Definition 2'] = final[key2]['definition']
        urban_dict['Example 2'] = final[key2]['example']

        text_format = text_format.replace('$total-results', str(len(final)))
        text_format = text_format.replace('$results', '2')

        urban_dict['Footer'] = 'This is a footer'

        print(key1, key2)

        print(urban_dict)
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
