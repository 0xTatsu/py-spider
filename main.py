import urllib.request
from bs4 import BeautifulSoup
import re
import ssl


def get_oxford(w):
    try:
        url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'

        page = urllib.request.urlopen(url + w)
        soup = BeautifulSoup(page, "html.parser")

        word = soup.select('h1[class="headword"]')[0].getText()
        # get word type: noun, verb, adj, adv ...
        wordTypeSelect = soup.select('span[class="pos"]')
        wordType = wordTypeSelect[0].getText() if len(
            wordTypeSelect) > 0 else ''
        # word ipa
        phonetic = soup.select('div[class="phons_n_am"] span[class="phon"]')
        amerian_ipa = phonetic[0].getText() if len(phonetic) > 0 else ''
        amerian_mp3 = soup.find(
            'div', {"class": "pron-us"})['data-src-mp3']  # audio
        audio_name = word + '_' + wordType + '_' + 'us.mp3'
        urllib.request.urlretrieve(
            amerian_mp3, audio_dir + audio_name)  # download
        audio = '[sound:' + audio_name + ']'

        return word + separator + wordType + separator + amerian_ipa + separator + audio + separator
    except ValueError:
        print('====================ERROR: ' + w)
        # print(ValueError)
        return
    except urllib.error.HTTPError:
        print('====================ERROR: ' + w)
        # print(urllib.error.HTTPError)
        return


separator = '@'
input_file = 'input.txt'
test_file = 'test.txt'
output_file = 'output.txt'
error_file = 'error.txt'
audio_dir = '/Users/1041828/oxford_mp3/'

result = list()
err = list()
with open(input_file) as rfile:
    for line in rfile:
        line_list = line.rstrip('\n').split('|')
        print('processing... '+line_list[0])
        word = line_list[0].strip().lower().replace(" ", "-")
        data = get_oxford(word)
        if (data):
            if (len(line_list) > 1):
                data = data + line_list[1]
            result.append(data)
        else:
            err.append(line_list[0])

with open(output_file, 'w') as wfile:
    wfile.write("\n".join(result))

with open(error_file, 'w') as wfile:
    wfile.write("\n".join(err))
