# Story Stage: a speech-practice theatre for kids

A small web app that helps children aged about 4–6 practise speech sounds at home.
Classic fairy tales are played out in a puppet theatre, and the child is one of the actors:
in every scene a character comes on stage, and the child plays its part by copying its sound.

It is a static web page with no build step: `index.html`, the tales in `stories.js`,
illustrations in `art/` and recorded voices in `audio/`.

## How it plays

1. Pick a fairy tale on the home screen.
2. Tap **Open the curtain**. A storyteller reads each scene, and the characters speak in their own voices.
3. In each scene the child:
   - **copies a character's sound** three times (the hen's *Cluck*, the wolf's *Knock, knock*, Papa Bear's *Grrr*, the goats' *Trip, trap*…),
   - **plays a mouth game** (puff cheeks, click the tongue, press the lips, lick the lips), then taps a target,
   - or **plays a breathing game** (be the wind, huff and puff, cool the porridge, blow the troll off the bridge).
4. At the end the whole cast takes a bow to applause, and the tale earns a gold star.

**Magic ears 👂:** with microphone access, the story moves on when the child makes a sustained
sound or blows. They hear *that* a sound was made, not *how well*, so a grown-up should stay close
and can always tap the golden button instead.

## The tales

| Tale | Scenes | Practises |
|---|---|---|
| 🐔 The Little Red Hen | 13 | K, L, M, W, N, P, T, tongue tapping, lip licking, breathing |
| 🐷 The Three Little Pigs | 13 | W, K, N, P, H, R, OO, OW, cheek puffing, tongue clicks, lip pressing, breathing |
| 🐻 Goldilocks and the Three Bears | 12 | G, R, L, M, Z, B, H, P, tongue up and down, wide-open mouth, breathing |
| 🧣 Little Red Riding Hood | 12 | B, T, W, S, N, F, K, D, NG, R, CH, tongue up, lip licking, breathing |
| 🐐 The Three Billy Goats Gruff | 11 | M, G, R, TR, S, PL, SH, CH, chewing, breathing |

These are traditional public-domain folk tales, retold gently: nobody gets eaten. Grandma hides in the
wardrobe, and the wolves and the troll run away or are washed away.

## Look and feel

- A gold-framed proscenium with velvet curtains that gather open, a spotlight with floating dust, footlights and a wooden stage.
- Painted scenery in layers (sky, hills, a river with a footbridge, a cosy cottage room) that shifts slightly when the tablet tilts.
- 3D character illustrations that hop, breathe and bow; a second character can share the stage.
- Glass-style captions where each word lights up as it is spoken, with characters' words in quotes.

## Sound

- **Voices:** every line is pre-recorded with [Kokoro](https://github.com/hexgrad/kokoro), an open-source neural
  text-to-speech model (Apache 2.0). There is a warm storyteller voice and a separate voice for each character:
  a deep wolf, a growly troll, a tiny Baby Bear and so on. If a recording is missing (or the page is opened as a
  local file), the device's own voice reads the line instead.
- **Effects** are synthesized in code through a soft room reverb: a plucked harp, a wooden marimba, a water-drop pop and applause.
- Snoring (*Zzzz*) is shaped from filtered noise, because voice engines read it as letters.

### Changing a line or adding a tale

Recordings are keyed by voice and text, so after editing `stories.js` record the new lines:

```bash
pip install kokoro-onnx soundfile numpy        # and ffmpeg
# model files: https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
node tools/extract-lines.js > lines.json
python tools/record.py lines.json --model kokoro-v1.0.onnx --voices voices-v1.0.bin
```

Only new lines are recorded, and recordings for removed lines are deleted. Character voices are set in
`VOICE_CAST` at the bottom of `stories.js` (Kokoro voice, speed, pitch shift).

## Running it

- **On a tablet or phone:** turn on GitHub Pages (Settings → Pages → branch `main`) and open
  `https://<user>.github.io/<repo>/logopedia/`. Use “Add to Home Screen” for an app icon.
- **Locally:** run `python3 -m http.server` in this folder and open `http://localhost:8000`.
  Opening `index.html` directly as a file works too, but then the device voice is used and the microphone is off.

Stars and settings are stored only in that browser (localStorage).

## Credits

- Illustrations in `art/` are [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) by Microsoft, MIT License
  (see `art/LICENSE-fluentui-emoji.txt`). Little Red Riding Hood and the Little Red Hen are recoloured versions.
- Voices recorded with Kokoro-82M (Apache 2.0).
- The title font, Fraunces, loads from Google Fonts. Without a connection, a system serif font is used instead.

> This app supports speech practice at home. It does not replace a speech therapist.
