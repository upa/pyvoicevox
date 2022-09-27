
import pytest
import pyvoicevox as pv2

# Run this test while running voicevox-core on localhost:50021
endpoint = "http://127.0.0.1:50021"

def test_v2e_get_speakers():
    v2e = pv2.VVoxEngine(endpoint)

    speakers = v2e.get_speakers()
    for id, name in speakers:
        print("{:2} {}".format(id, name))

    speakers = v2e.get_speakers(raw_format = True)


def test_v2e_set_speaker():
    v2e = pv2.VVoxEngine(endpoint)
    v2e.set_speaker(1)
    assert v2e.speaker == 1

    with pytest.raises(Exception) as e:
        v2e.set_speaker(999)
    assert str(e.value) == "invalid speaker id 999"

def test_userword():
    uw = pv2.UserWord("hoge", "ほげ", 1, word_type = pv2.WORD_TYPE_COMMON_NOUN)
    print(uw)

def delete_all_registered_user_word():
    v2e = pv2.VVoxEngine(endpoint)
    raw_word_json = v2e.get_registered_user_words(raw_format = True)
    for uuid in raw_word_json.keys():
        v2e.delete_user_word(uuid)


def test_v2e_delete_and_get_registered_user_words():
    delete_all_registered_user_word()
    v2e = pv2.VVoxEngine(endpoint)
    d = v2e.get_registered_user_words()
    assert d == {}

def test_v2e_add_user_word():
    delete_all_registered_user_word()    

    v2e = pv2.VVoxEngine(endpoint)
    uw = pv2.UserWord("tutorial", "チュートリアル", 1,
                      word_type = pv2.WORD_TYPE_COMMON_NOUN)    

    v2e.add_user_word(uw) # add by post
    v2e.add_user_word(uw) # update by put

def test_v2e_synthesis_save():
    v2e = pv2.VVoxEngine(endpoint)
    wav = v2e.synthesize("テストですよ")
    pv2.save_wav(wav, "pv2-tiral-speaker-{}.wav".format(v2e.speaker))

    wav = v2e.synthesize("テストですよ", speaker = 11)
    v2e.save_wav(wav, "pv2-trial-speaker-{}.wav".format(11))

