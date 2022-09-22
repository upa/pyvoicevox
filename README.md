

### pyvoicevox

A simple python library for interacting with [VOICEVOX
Engine](https://github.com/VOICEVOX/voicevox_engine)


Install `pip install .`

```shell-session
> python
Python 3.8.8 (default, Apr 13 2021, 12:59:45) 
[Clang 10.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import pyvoicevox as pv2
>>> v2e = pv2.VVoxEngine("http://localhost:50021")
>>> wav = v2e.synthesize("ほげ")
>>> pv2.save_wav(wav, "hoge.wav")
```
