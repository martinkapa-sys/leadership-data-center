# Story Stage: a speech-practice theatre for kids

A small web app that helps children aged about 4–6 practise speech sounds at home.
Each story is a short play in a fairytale puppet theatre. The child is the actor: in every
scene a new animal comes on stage, and the child plays its part by imitating its sound.

It is a single `index.html` file plus an `art/` folder of illustrations, so there is nothing to install.

## How it plays

1. Pick a storybook on the home screen.
2. Tap **Open the curtain**. A storyteller voice reads each scene aloud.
3. In each scene the child:
   - **imitates an animal sound** three times (snake *Sssss*, bee *Zzzz*, lion *Rrroar*, chick *Cheep*…),
   - **plays a mouth game** (stick the tongue out like a frog, lick lips like a kitten, click like pony hooves), then taps a target,
   - or **plays a breathing game** (blow away fog, balloons or ice).
4. At the end the whole cast takes a bow to applause, and the story earns a gold star.

**Magic ears 👂:** with microphone access, the story moves on when the child makes a sustained
sound or blows. They hear *that* a sound was made, not *how well*, so a grown-up should stay close
and can always tap the golden button instead.

## Look and feel

- A gold-framed proscenium with velvet curtains that gather open, a spotlight with floating dust, footlights and a wooden stage.
- Painted scenery in layers (sky, far hills, near hills) that shifts slightly when the tablet tilts.
- 3D character illustrations that hop, breathe and bow, plus glass-style captions where each word lights up as the storyteller reads it.
- Sound design built in code, played through a soft room reverb: a plucked harp (Karplus-Strong string synthesis) for the
  curtain and scene wins, a wooden marimba for each success, a water-drop pop, and applause from 26 individual "clappers".
- The snake, bee and owl hiss, buzz and hush with sounds shaped from filtered noise, because voice engines read "Sssss" as letters.
- Confetti, and a short vibration on Android phones.

The storyteller uses the device's own voice, picking the most natural one available (Natural, Premium, Enhanced or Google voices).
On iPhone and iPad, downloading an "Enhanced" or "Premium" English voice in Settings › Accessibility › Spoken Content makes a big difference.

## Stories and sounds

| Story | Practises |
|---|---|
| 🐄 The Farm Show | M, B, W, P, lip licking, breathing |
| 👑 The Lost Crown | S, Z, SH, CH, tongue out, breathing |
| 🐉 The Sleepy Dragon | R, L, K, G, tongue clicks, breathing |

New stories are easy to add: each one is a list of scenes in the `STORIES` array at the top of the script.

## Running it

- **Quick look:** open `index.html` in a browser. The microphone only works over `https://` or `localhost`.
- **On a tablet or phone:** turn on GitHub Pages (Settings → Pages → branch `main`) and open
  `https://<user>.github.io/<repo>/logopedia/`. Use “Add to Home Screen” for an app icon.
- **Locally with the microphone:** run `python3 -m http.server` in this folder and open `http://localhost:8000`.

Stars and settings are stored only in that browser (localStorage).

## Credits

Illustrations in `art/` are [Fluent Emoji](https://github.com/microsoft/fluentui-emoji) by Microsoft, used under the MIT License
(see `art/LICENSE-fluentui-emoji.txt`). The title font, Fraunces, loads from Google Fonts. Without a connection, a system serif font is used instead.

> This app supports speech practice at home. It does not replace a speech therapist.
