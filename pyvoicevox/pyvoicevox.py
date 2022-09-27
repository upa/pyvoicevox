
import requests


WORD_TYPE_COMMON_NOUN = "COMMON_NOUN"
WORD_TYPE_PROPER_NOUN = "PROPER_NOUN"
WORD_TYPE_VERB = "VERB"
WORD_TYPE_ADJECTIVE = "ADJECTIVE"
WORD_TYPE_SUFFIX = "SUFFIX"

WORD_TYPE_LIST = [
    WORD_TYPE_COMMON_NOUN, WORD_TYPE_PROPER_NOUN, WORD_TYPE_VERB,
    WORD_TYPE_ADJECTIVE, WORD_TYPE_SUFFIX,
]

class UserWord:
    def __init__(self, surface, pronounce, accent_type, word_type = None, uuid = None):
        if not isinstance(accent_type, int) or len(pronounce) < accent_type:
            raise ValueError("invalid accent_type {}".format(accent_type))
        if word_type and not word_type in WORD_TYPE_LIST:
            raise ValueError("invalid word_type {}".format(word_type))

        self.surface = surface
        self.pronounce = pronounce
        self.accent_type = accent_type
        self.word_type = word_type
        self.uuid = uuid # only for get_registered_user_words

    def __str__(self):
        return "{} pronounce:{} accent:{}".format(self.surface,
                                                  self.pronounce, self.accent_type)


class VVoxEngine:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.speaker = 2 # default speaker

    def get_speakers(self, raw_format = False):
        uri = "{}/speakers".format(self.endpoint)
        r = requests.get(uri)
        r.raise_for_status()
        if raw_format:
            return r.json()

        speakers = {} # key is id, value is "Character Name, Style Name"
        for char in r.json():
            char_name = char["name"]
            for style in char["styles"]:
                speakers[style["id"]] = { "name": char_name, "style": style["name"]}

        # return [ (id, name), (id, name), ... ]
        return [ (x[0], x[1]) for x in sorted(speakers.items(), key = lambda x: x[0])]

    def set_speaker(self, speaker_id):
        speakers = self.get_speakers()
        ids = [ x[0] for x in speakers ]
        if not speaker_id in ids:
            raise ValueError("invalid speaker id {}".format(speaker_id))
        self.speaker = speaker_id

    def get_registered_user_words(self, raw_format = False):
        uri = "{}/user_dict".format(self.endpoint)
        r = requests.get(uri)
        r.raise_for_status()

        if raw_format:
            return r.json()

        d = {} # key is surface, value is UserWords
        for uuid, item in r.json().items():
            surface = zen2han(item["surface"])
            pronounce = item["pronunciation"]
            accent_type = item["accent_type"]
            # XXX: word_type is isolated into part_of_speech
            word = UserWord(surface, pronounce, accent_type, uuid = uuid)
            d[surface] = word
        return d

    def delete_user_word(self, uuid):
        uri = "{}/user_dict_word/{}".format(self.endpoint, uuid)
        r = requests.delete(uri)
        r.raise_for_status()

    
    def add_user_word(self, uw, check = True):
        """
        add or update a user word. if check is Ture, check the
        surface of word is already registered, and then add or update
        the word depending on the check result. if check is False,
        add the word.
        """
        if not isinstance(uw, UserWord):
            raise ValueError("1st argument must be UserWord object")

        params = {
            "surface": uw.surface,
            "pronunciation": uw.pronounce,
            "accent_type": uw.accent_type,
        }
        if uw.word_type:
            params["word_type"] = uw.word_type


        # 1. check this surface is already registered
        if check:
            registered = self.get_registered_user_words()
            if uw.surface in registered:
                # already registered. do update with post
                uuid = registered[uw.surface].uuid
                params["word_uuid"] = uuid
                uri = "{}/user_dict_word/{}".format(self.endpoint, uuid)
                r = requests.put(uri, params = params)
                r.raise_for_status()
                return

        # check is unnecesary, or not registered word. do add with put

        uri = "{}/user_dict_word".format(self.endpoint)
        r = requests.post(uri, params = params)
        r.raise_for_status()
        

    def _check_speaker_id(self, speaker):
        if not speaker:
            return self.speaker
        else:
            if not isinstance(self.speaker, int):
                raise ValueError("speaker must be int")
            return speaker

    def synthesize(self, text, speaker = None):
        speaker_id = self._check_speaker_id(speaker)

        query_json = self.do_audio_query(text, speaker = speaker_id)
        wav = self.do_synthesis(query_json, speaker = speaker_id)
        return wav

    def do_audio_query(self, text, speaker = None):
        params = {
            "speaker": self._check_speaker_id(speaker),
            "text": text,
        }
        uri = "{}/audio_query".format(self.endpoint)
        r = requests.post(uri, params = params)
        r.raise_for_status()
        return r.json()


    def do_synthesis(self, query_json, speaker = None):
        params = {
            "speaker": self._check_speaker_id(speaker),
        }
        uri = "{}/synthesis".format(self.endpoint)
        r = requests.post(uri, params = params, json = query_json)
        r.raise_for_status()
        return r.content # binary of wav

    def save_wav(self, wav, path):
        _save_wav(wav, path)



def zen2han(text):
    # From https://qiita.com/YuukiMiyoshi/items/6ce77bf402a29a99f1bf
    return text.translate(str.maketrans({chr(0xFF01 + i):
                                         chr(0x21 + i) for i in range(94)}))
    
def _save_wav(wav, path):
    with open(path, "wb") as f:
        f.write(wav)

def save_wav(wav, path):
    _save_wav(wav, path)
