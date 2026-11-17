# Hovorílko – logopedické cvičenia pre deti

Jednoduchá webová aplikácia na domáce precvičovanie výslovnosti pre deti v predškolskom veku (cca 4–6 rokov).
Je to jeden súbor `index.html` a nič netreba inštalovať.

## Čo obsahuje

- **👅 Rozcvička jazýčka**: 12 oromotorických cvičení (koníček, hodinky, hojdačka, maliar, zmrzlina, hadík…). Pri každom cvičení sa odpočítavajú opakovania.
- **🎂 Fúkanie**: dychové cvičenie, pri ktorom dieťa sfukuje sviečky na torte. S mikrofónom sviečky zhasínajú pri skutočnom fúknutí, bez neho sa ťuká na tlačidlo.
- **🗣️ Hlásky** R, L, S, Z, C, Š, Ž, Č, K, každá v týchto krokoch:
  1. samostatná hláska (napr. „motorka robí rrrr“),
  2. slabiky (RA, RO, TRA…),
  3. slová s hláskou na začiatku, na konci a v strede, s obrázkom a farebne zvýraznenou hláskou.
  - 🔊 aplikácia slovo prečíta nahlas,
  - 🎤 nahrá dieťa a ▶️ mu nahrávku prehrá, aby sa počulo,
  - ⭐ „Podarilo sa!“ pridá hviezdičku.
- **🎁 Nálepky**: za každých 5 hviezdičiek dieťa dostane novú nálepku do albumu.
- **⚙️ Pre rodičov**: výber hlások, ktoré sa trénujú, prehľad cvičenia za posledné dni, nastavenie hlasu a tipy.

Pokrok sa ukladá iba v danom zariadení a prehliadači (localStorage).

## Ako spustiť

- **Najjednoduchšie:** otvoriť `index.html` v prehliadači.
  Mikrofón (nahrávanie a fúkanie) však funguje iba cez `https://` alebo `localhost`.
- **Na tablete alebo telefóne:** zapnúť GitHub Pages (Settings → Pages → branch) a otvoriť
  `https://<pouzivatel>.github.io/<repozitar>/logopedia/`. Potom v prehliadači zvoliť
  „Pridať na plochu“ a aplikácia sa bude otvárať ako ikonka.
- **Lokálne s mikrofónom:** `python3 -m http.server` v priečinku `logopedia` a otvoriť `http://localhost:8000`.

## Slovenský hlas

Čítanie nahlas používa hlas zariadenia. Ak slová znejú zle, doinštalujte slovenský hlas:
- iPhone/iPad: Nastavenia → Prístupnosť → Hovorený obsah → Hlasy → Slovenčina
- Android: Nastavenia → Prevod textu na reč → Google → Slovenčina

> Aplikácia nenahrádza logopéda, len pomáha pri domácom precvičovaní.
