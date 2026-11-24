// Lists every line the page can speak, for tools/record.py.
// Usage: node tools/extract-lines.js > lines.json
const fs = require('fs'), vm = require('vm'), path = require('path');
const window = {};
vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', 'stories.js'), 'utf8'), { window });
const out = new Map();
const add = (voice, text) => { const key = window.clipKey(voice, text); if (!out.has(key)) out.set(key, { key, voice, text }); };
const addLine = str => window.parseLine(str).forEach(s => add(s.voice, s.text));
for (const st of window.STORIES) {
  add('n', st.title);
  for (const sc of st.scenes) {
    [sc.say, sc.ask, sc.done].forEach(addLine);
    if (sc.model && !sc.fric) add(sc.voice || 'n', sc.model);
  }
}
window.PRAISE.concat(window.SYSTEM_LINES).forEach(t => add('n', t));
for (const { voice } of out.values()) if (!window.VOICE_CAST[voice]) throw new Error('No voice for ' + voice);
console.log(JSON.stringify({ cast: window.VOICE_CAST, lines: [...out.values()] }, null, 1));
