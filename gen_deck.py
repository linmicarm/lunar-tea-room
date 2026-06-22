# -*- coding: utf-8 -*-
"""
gen_deck.py — emits cards.js with the full 78-card tarot deck.

We generate the file rather than hand-typing 78 objects so the Minor
Arcana stay perfectly consistent (numerals, suit glyphs, court cards).
Every meaning is hand-authored below in Mabel's warm, plain voice —
nothing is templated or auto-filled.

Output object shape matches the original exactly, plus one new field:
  num, name, emoji, suit, keywords, meaning
"""

import json

# ---- Major Arcana: unchanged from the original, with suit added ----
majors = [
    ("0","The Fool","\U0001FAB6",["new beginnings","trust","leap"],
     "A fresh start is calling. The Fool says yes before knowing every step \u2014 take the leap with an open heart."),
    ("I","The Magician","\u2728",["power","focus","manifest"],
     "You already have the tools you need. Channel your focus and turn an idea into something real."),
    ("II","The High Priestess","\U0001F319",["intuition","mystery","stillness"],
     "Get quiet and listen inward. Your intuition knows something your busy mind hasn't caught up to yet."),
    ("III","The Empress","\U0001F338",["abundance","nurture","creativity"],
     "Something is blooming \u2014 a project, a bond, a softer season. Tend it gently and let it grow."),
    ("IV","The Emperor","\U0001F3DB\uFE0F",["structure","stability","lead"],
     "Build the framework. A little structure right now turns scattered energy into steady progress."),
    ("V","The Hierophant","\U0001F511",["tradition","guidance","learning"],
     "A mentor, teaching, or tried-and-true path has something to offer. There's wisdom in the well-worn road."),
    ("VI","The Lovers","\U0001F495",["connection","choice","harmony"],
     "A meaningful choice about the heart \u2014 partnership, values, alignment. Choose what feels true to you."),
    ("VII","The Chariot","\U0001F3C7",["drive","willpower","victory"],
     "Grab the reins. With determination and a clear direction, you can push through and win the day."),
    ("VIII","Strength","\U0001F981",["courage","patience","soft power"],
     "True strength is gentle. Meet the hard thing with patience and compassion rather than force."),
    ("IX","The Hermit","\U0001F56F\uFE0F",["reflection","solitude","inner light"],
     "Step back for a moment alone. The answer you're seeking comes from quiet reflection, not the crowd."),
    ("X","Wheel of Fortune","\U0001F340",["change","cycles","luck"],
     "The wheel is turning in your favor. Stay open \u2014 a shift in luck or timing is on its way."),
    ("XI","Justice","\u2696\uFE0F",["fairness","truth","balance"],
     "Things are coming into balance. Act with honesty and the outcome will be fair to you."),
    ("XII","The Hanged Man","\U0001FA9E",["pause","new view","surrender"],
     "A pause isn't a setback. Look at the situation from a new angle \u2014 the answer flips into view."),
    ("XIII","Death","\U0001F98B",["endings","rebirth","release"],
     "Not literal \u2014 this is transformation. Let an old chapter close so a new one has room to begin."),
    ("XIV","Temperance","\U0001F9EA",["balance","patience","blend"],
     "Find the middle path. Mixing patience with a little flexibility brings everything into harmony."),
    ("XV","The Devil","\U0001F517",["habits","honesty","release"],
     "Notice what's holding you. A habit or fear feels binding only until you see you hold the key."),
    ("XVI","The Tower","\u26A1",["upheaval","truth","clearing"],
     "A sudden shake-up clears away what wasn't solid. It's startling, but it makes room for something truer."),
    ("XVII","The Star","\u2B50",["hope","healing","renewal"],
     "Breathe \u2014 the hard part is easing. The Star brings hope, healing, and a gentle return of faith."),
    ("XVIII","The Moon","\U0001F311",["dreams","intuition","mystery"],
     "Things aren't fully clear yet, and that's okay. Trust your dreams and instincts to light the path."),
    ("XIX","The Sun","\u2600\uFE0F",["joy","success","warmth"],
     "Pure sunshine. Joy, clarity, and success are shining on you \u2014 enjoy this bright, open moment."),
    ("XX","Judgement","\U0001F4EF",["awakening","calling","renewal"],
     "A wake-up call invites you to rise. Reflect on how far you've come and answer what's calling you forward."),
    ("XXI","The World","\U0001F30D",["completion","wholeness","celebrate"],
     "A cycle completes. Take a bow \u2014 you've come full circle, and the whole world feels open again."),
]

# ---- Minor Arcana suit setup ----
# Each suit: display name, glyph, and its everyday "theme" so meanings stay grounded.
suits = {
    "wands":      {"label": "Wands",      "emoji": "\U0001F525"},  # fire — drive, creativity
    "cups":       {"label": "Cups",       "emoji": "\U0001F4A7"},  # water — feelings, bonds
    "swords":     {"label": "Swords",     "emoji": "\U0001F5E1\uFE0F"},  # air — thought, truth
    "pentacles":  {"label": "Pentacles",  "emoji": "\U0001FA99"},  # earth — work, money, body
}

ranks = ["Ace","Two","Three","Four","Five","Six","Seven","Eight","Nine","Ten",
         "Page","Knight","Queen","King"]

# Hand-authored: [keywords...] and meaning, per suit per rank.
minor = {
"wands": {
  "Ace":     (["spark","new idea","energy"], "A bright new spark of energy or inspiration arrives. Say yes to the idea that's making your hands itch to start."),
  "Two":     (["planning","choice","horizon"], "You're standing at the edge of something, map in hand. Pick a direction and let yourself imagine the bigger picture."),
  "Three":   (["progress","expansion","wait"], "The first efforts are paying off. Ships are on their way back \u2014 keep looking outward and trust your momentum."),
  "Four":    (["celebration","home","milestone"], "A happy little milestone to celebrate. Pause and enjoy the warmth of people and place before the next push."),
  "Five":    (["friction","competition","scrappy"], "A bit of friction or rivalry stirs things up. It's noisy, not dangerous \u2014 find a way to play that's still fair."),
  "Six":     (["recognition","success","pride"], "A well-earned win, and others notice. Let yourself be seen and enjoy the moment of recognition."),
  "Seven":   (["standing firm","defense","conviction"], "You've got the higher ground \u2014 hold it. It's worth defending what you've built when you believe in it."),
  "Eight":   (["momentum","speed","news"], "Things move fast now. Messages, travel, or quick progress \u2014 ride the momentum while it's flowing."),
  "Nine":    (["resilience","one more push","guard"], "You're tired but close. One more round of effort, and a little self-protection, will carry you through."),
  "Ten":     (["burden","almost there","delegate"], "You're carrying a lot. The finish line is near \u2014 set down what isn't yours to hold and ask for a hand."),
  "Page":    (["curiosity","exploration","spark"], "A curious, playful messenger. Follow the thing that excites you, even before you know where it leads."),
  "Knight":  (["adventure","passion","bold"], "Bold, restless energy ready to charge ahead. Channel the fire so your enthusiasm doesn't outrun your plan."),
  "Queen":   (["confidence","warmth","magnetism"], "Warm, self-assured, and magnetic. Lead with your natural glow and people will gather around it."),
  "King":    (["vision","leadership","drive"], "A visionary who turns passion into direction. Take charge of your own big idea with steady confidence."),
},
"cups": {
  "Ace":     (["new love","openness","feeling"], "A cup overflowing with new feeling \u2014 love, compassion, or creative joy. Let your heart open to it."),
  "Two":     (["partnership","mutual","bond"], "A genuine meeting of hearts. Mutual respect and care flow both ways \u2014 cherish this connection."),
  "Three":   (["friendship","joy","community"], "Good friends, good company, something to toast. Lean into the people who celebrate you."),
  "Four":    (["apathy","reflection","reset"], "Feeling a little checked-out or restless. Sit with it \u2014 and notice the offer you might be overlooking."),
  "Five":    (["disappointment","grief","perspective"], "Something didn't go as hoped, and that's worth grieving. Two cups still stand \u2014 turn and see what remains."),
  "Six":     (["nostalgia","comfort","kindness"], "A warm wave of nostalgia or a kind gesture from the past. Let sweetness and simple comfort find you."),
  "Seven":   (["options","daydreams","clarity"], "So many tempting choices, some real and some just shiny. Get clear on what you actually want before you reach."),
  "Eight":   (["walking away","seeking more","growth"], "You're ready to leave behind what no longer fills you. Walking toward something deeper takes quiet courage."),
  "Nine":    (["contentment","wish","satisfaction"], "The 'wish card' \u2014 a deep, satisfied contentment. Savor having what you hoped for."),
  "Ten":     (["harmony","belonging","joy"], "Emotional fullness and belonging \u2014 the happy-home feeling. Soak in the warmth of your people."),
  "Page":    (["wonder","tenderness","message"], "A tender, dreamy messenger. A sweet idea or gentle invitation may arrive \u2014 stay open to it."),
  "Knight":  (["romance","following heart","grace"], "A romantic, idealistic mover who leads with the heart. Follow what you love, gracefully."),
  "Queen":   (["compassion","intuition","care"], "Deeply caring and intuitive. Trust your feelings and offer yourself the same tenderness you give others."),
  "King":    (["calm","balance","emotional mastery"], "Steady at the emotional helm. Stay calm and kind under pressure and others will feel safe with you."),
},
"swords": {
  "Ace":     (["clarity","truth","breakthrough"], "A sudden clear thought cuts through the fog. A breakthrough or honest truth gives you fresh direction."),
  "Two":     (["stalemate","decision","weigh"], "Stuck between two options with a blindfold on. Take the blindfold off \u2014 you have more information than you think."),
  "Three":   (["heartache","release","healing"], "A painful truth or heartache. Let yourself feel it; naming the hurt is the first step to it easing."),
  "Four":    (["rest","recovery","pause"], "Time to genuinely rest. Step back and let your mind recover \u2014 you'll think clearer for it."),
  "Five":    (["conflict","ego","let go"], "A win that doesn't feel like one, or a fight not worth it. Ask whether being right is worth the cost."),
  "Six":     (["transition","moving on","calmer waters"], "Moving away from rougher waters toward calm. The journey forward is gentle, even if leaving was hard."),
  "Seven":   (["strategy","caution","honesty"], "A nudge toward cleverness \u2014 or a warning to watch for it. Choose the honest path; shortcuts have a way of unraveling."),
  "Eight":   (["feeling stuck","self-doubt","freedom"], "The trap feels tighter than it is. Look closely \u2014 the way out has been within reach all along."),
  "Nine":    (["worry","anxiety","dawn"], "Late-night worries can loom large. Most of these fears feel smaller in daylight \u2014 be gentle with your mind."),
  "Ten":     (["rock bottom","ending","sunrise"], "A hard ending, fully felt. The good news hidden here: it can't get worse, and a new dawn is already coming."),
  "Page":    (["curiosity","truth-seeking","alert"], "A sharp, curious mind hungry for the truth. Ask the questions \u2014 just keep your words kind."),
  "Knight":  (["focus","ambition","slow down"], "Fast, focused, and direct \u2014 charging toward a goal. Make sure you're aimed well before you race off."),
  "Queen":   (["clear-eyed","honest","independent"], "Clear-eyed and fair, with healthy boundaries. Speak your truth directly and lead with level-headed kindness."),
  "King":    (["logic","fairness","authority"], "Wise, fair, and grounded in clear thinking. Make the call with both your head and your principles."),
},
"pentacles": {
  "Ace":     (["opportunity","new venture","seed"], "A solid new opportunity \u2014 a job, a plan, a tangible seed. Plant it; this one has real roots."),
  "Two":     (["juggling","balance","flexibility"], "Juggling a couple of things at once. Stay light on your feet and the balance holds just fine."),
  "Three":   (["teamwork","skill","building"], "Good work taking shape through collaboration. Your skill is valued \u2014 keep building together."),
  "Four":    (["security","holding on","loosen"], "Holding tight to what feels safe. A little security is wise; just don't grip so hard nothing new can come in."),
  "Five":    (["hardship","support","reach out"], "A lean or lonely stretch. Help is closer than it looks \u2014 the lit window is right there; reach out."),
  "Six":     (["generosity","fairness","flow"], "Giving and receiving find their balance. Whether you're sharing or being supported, let it flow kindly."),
  "Seven":   (["patience","assessment","long game"], "You've planted; now you wait and tend. Step back, assess honestly, and trust the slow growth."),
  "Eight":   (["craft","diligence","mastery"], "Heads-down, steady practice. Care about the details \u2014 you're quietly getting very good at this."),
  "Nine":    (["self-reliance","comfort","enjoy"], "Earned comfort and independence. Enjoy the fruits of your own effort \u2014 you built this garden."),
  "Ten":     (["stability","legacy","abundance"], "Lasting security and the warmth of roots. Wealth here is also family, home, and things that endure."),
  "Page":    (["study","ambition","new skill"], "A studious, ambitious messenger. A chance to learn something practical \u2014 start, and stay curious."),
  "Knight":  (["reliability","routine","patience"], "Dependable and methodical, in for the long haul. Slow and steady really does win this one."),
  "Queen":   (["nurturing","practical","grounded"], "Warm, capable, and down-to-earth. Tend to both your work and your wellbeing \u2014 you're good at both."),
  "King":    (["abundance","security","provider"], "Grounded success and steady provision. You've built something solid; lead it generously."),
},
}

def js_string(s):
    # Emit a JS double-quoted string with non-ASCII as \uXXXX escapes,
    # matching the original file's style.
    out = ['"']
    for ch in s:
        cp = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == '\\':
            out.append('\\\\')
        elif 32 <= cp < 127:
            out.append(ch)
        elif cp <= 0xFFFF:
            out.append('\\u{:04X}'.format(cp))
        else:
            out.append('\\u{{{:X}}}'.format(cp))
    out.append('"')
    return ''.join(out)

def obj(num, name, emoji, suit, keywords, meaning, indent="  "):
    kw = "[" + ", ".join(js_string(k) for k in keywords) + "]"
    return (
        f"{indent}{{\n"
        f"{indent}  num: {js_string(num)},\n"
        f"{indent}  name: {js_string(name)},\n"
        f"{indent}  emoji: {js_string(emoji)},\n"
        f"{indent}  suit: {js_string(suit)},\n"
        f"{indent}  keywords: {kw},\n"
        f"{indent}  meaning:\n"
        f"{indent}    {js_string(meaning)},\n"
        f"{indent}}},"
    )

header = '''/* ============================================================
   cards.js — the deck data (full 78-card deck)
   ------------------------------------------------------------
   The complete tarot deck: 22 Major Arcana + 56 Minor Arcana
   (Wands, Cups, Swords, Pentacles — Ace through King).

   This file is generated by gen_deck.py so the Minor Arcana
   stay perfectly consistent, but every meaning is hand-written
   in plain, friendly language. Edit gen_deck.py to change copy,
   then re-run it to regenerate this file.

   Each card object:
     - num     : numeral / rank shown on the card face
     - name    : the card's full name
     - emoji   : a simple glyph standing in for full artwork
     - suit    : "major" | "wands" | "cups" | "swords" | "pentacles"
     - keywords: 2–3 quick-glance themes (shown as little pills)
     - meaning : a friendly, plain-language reading (upright)

   The draw logic in main.js only reads these fields, so the
   deck can grow without touching any interaction code.
   ============================================================ */

const TAROT_DECK = [
'''

parts = [header]

parts.append("  /* ---------- Major Arcana ---------- */")
for num, name, emoji, kw, meaning in majors:
    parts.append(obj(num, name, emoji, "major", kw, meaning))

for suit_key, suit_info in suits.items():
    parts.append(f"\n  /* ---------- Minor Arcana: {suit_info['label']} {suit_info['emoji']} ---------- */")
    for rank in ranks:
        kw, meaning = minor[suit_key][rank]
        name = f"{rank} of {suit_info['label']}"
        # Aces show "Ace", number cards show the word, courts show their title — all via num field.
        num = rank
        parts.append(obj(num, name, suit_info["emoji"], suit_key, kw, meaning))

parts.append("];\n")

js = "\n".join(parts)
with open("cards.js", "w", encoding="utf-8") as f:
    f.write(js)

# Sanity report
total = len(majors) + sum(len(minor[s]) for s in minor)
print(f"Wrote cards.js — {total} cards "
      f"({len(majors)} major + {sum(len(minor[s]) for s in minor)} minor)")