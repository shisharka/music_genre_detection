from acrcloud.recognizer import ACRCloudRecognizer
import json
import os
from helper import GENRES, FILES_PER_GENRE, AUDIO_DATA_PATH

config = {
    'host':'identify-eu-west-1.acrcloud.com',
    'access_key':'0fdbb63df9fabb64c1b0909b6f8a76ae',
    'access_secret':'bQcyrUipFRe2c49E9OcVEAjfFic0bw0QHArQvYuU',
    'timeout':10 # seconds
}

re = ACRCloudRecognizer(config)

# json_response = json.loads(re.recognize_by_file('data/genres/blues/blues.00073.au', 0))
# print json_response['status']['code']
# print json_response['metadata']['music'][0]['artists'][0]['name']
# print json_response['metadata']['music'][0]['title']

dict = {}
for genre_index, genre_name in enumerate(GENRES):
    for i in range(0, FILES_PER_GENRE):
        filename = '{}.000{}.au'.format(genre_name,
                                        str(i).zfill(2))
        path = os.path.join(AUDIO_DATA_PATH, genre_name, filename)
        print 'Processing', filename
        json_response = json.loads(re.recognize_by_file(path, 0))
        if json_response['status']['code'] != 0:
            print filename
        else:
            dict[filename] = {}
            dict[filename]['artist'] = json_response['metadata']['music'][0]['artists'][0]['name']
            dict[filename]['title'] = json_response['metadata']['music'][0]['title']

# print dict
with open('metadata.json', 'w') as outfile:
    json.dump(dict, outfile)