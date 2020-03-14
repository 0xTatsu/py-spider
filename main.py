import urllib.request
from bs4 import BeautifulSoup
import re
import ssl


separator = '@'
input_file = 'input.txt'
output_file = 'output.txt'
error_file = 'error.txt'
audio_dir = '/Users/1041828/oxford_mp3/'

result = list()
err = list()
with open(input_file) as rfile:
    for line in rfile:
        line_list = line.rstrip('\n').split('|')
        data = get_oxford(line_list[0])
        if (data):
            if (len(line_list) > 1):
                data = data + line_list[1]
            result.append(data)
        else:
            print(line_list[0])
            err.append(line_list[0])

with open(output_file, 'w') as wfile:
    wfile.write("\n".join(result))

with open(error_file, 'w') as wfile:
    wfile.write(''.join(err))


def get_oxford(w):
    try:
        url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'

        page = urllib.request.urlopen(url + w)
        soup = BeautifulSoup(page, "html.parser")

        word = soup.select('h2[class="h"]')[0].getText()
        # get word type: noun, verb, adj, adv ...
        wordType = soup.select('span[class="pos"]')[0].getText()
        # word ipa
        ipa = soup.select('span[class="phon"]')
        # amerian_ipa = ''
        # audio = ''
        # if len(ipa):
        amerian_ipa = ipa[1].getText()[4:].replace('//', '/')
        amerian_mp3 = soup.find(
            'div', {"class": "pron-us"})['data-src-mp3']  # audio
        audio_name = word + '_' + wordType + '_' + 'us.mp3'
        urllib.request.urlretrieve(
            amerian_mp3, audio_dir + audio_name)  # download
        audio = '[sound:' + audio_name + ']'

        return word + separator + wordType + separator + amerian_ipa + separator + audio + separator
    except ValueError:
        print(ValueError)
        return
    except urllib.error.HTTPError as err:
        print(err)
        return