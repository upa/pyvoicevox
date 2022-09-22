

### pyvoicevox

A simple python library for interacting with [VOICEVOX
Engine](https://github.com/VOICEVOX/voicevox_engine)


Install: `pip3 install .` or `pip3 install git+https://github.com/upa/pyvoicevox`

```python
import pyvoicevox as pv2

v2e = pv2.VVoxEngine("http://localhost:50021")
wav = v2e.synthesize("ほげ")
pv2.save_wav(wav, "hoge.wav")

# with a different speaker.
wav = v2e.synthesize("ほげ", speaker = 4)
pv2.save_wav(wav, "hoge.wav")

# print speaker list
print("\n".join(map(lambda m: "id={} {}".format(m[0], m[1]), v2e.get_speakers())))
```
