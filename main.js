/* ============================================================
   main.js - site behavior
   Three small jobs:
     1. The card pull (shuffle -> draw -> reveal with glow)
     2. The mobile nav toggle
     3. A friendly confirmation on the booking form
   Data lives in cards.js (TAROT_DECK); this file only handles
   interaction, so the two concerns stay cleanly separated.
   ============================================================ */

/* ---------- 1. CARD PULL ---------------------------------- */

// Grab the elements we'll touch repeatedly.
const deck      = document.getElementById("deck");
const reveal    = document.getElementById("reveal");
const pullAgain = document.getElementById("pullAgain");
const againBtn  = document.getElementById("againBtn");

// Track whether a draw is mid-animation so we can't double-fire.
let drawing = false;

/**
 * Pick a random card from the deck.
 * Math.random() gives 0–0.999…, scaled to a valid array index.
 */
function randomCard() {
  const i = Math.floor(Math.random() * TAROT_DECK.length);
  return TAROT_DECK[i];
}

/**
 * Build the inner HTML for a revealed card.
 * Keywords become little pills; everything else is plain text.
 */
function renderCard(card) {
  const pills = card.keywords
    .map((k) => `<span>${k}</span>`)
    .join("");

  // Card art is a CSS-drawn suit emblem (no emojis). The suit field
  // ("major"|"wands"|"cups"|"swords"|"pentacles") picks the shape.
  return `
    <div class="r-num">${card.num}</div>
    <div class="r-suit r-suit-${card.suit}" aria-hidden="true"></div>
    <div class="r-name">${card.name}</div>
    <div class="r-keys">${pills}</div>
    <p class="r-meaning">${card.meaning}</p>
  `;
}

/**
 * The full draw sequence:
 *   shuffle wiggle -> hide deck -> reveal glowing card -> show "pull again"
 */
function drawCard() {
  if (drawing) return;          // ignore taps while animating
  drawing = true;

  // 1. play the shuffle wiggle on the deck
  deck.classList.add("shuffling");

  // 2. after the wiggle, swap deck out for the revealed card
  window.setTimeout(() => {
    const card = randomCard();

    deck.classList.remove("shuffling");
    deck.classList.add("hidden");          // hide face-down deck

    reveal.innerHTML = renderCard(card);   // fill in the card
    reveal.classList.remove("hidden");     // triggers the flipIn + glow

    pullAgain.classList.remove("hidden");  // offer another draw
    drawing = false;
  }, 520); // matches the 0.5s shuffle animation in CSS
}

/**
 * Reset back to the face-down deck so the user can draw again.
 */
function resetDeck() {
  reveal.classList.add("hidden");
  pullAgain.classList.add("hidden");
  deck.classList.remove("hidden");
}

// Wire up the deck: click + keyboard (Enter/Space) for accessibility.
deck.addEventListener("click", drawCard);
deck.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " ") {
    e.preventDefault();
    drawCard();
  }
});
againBtn.addEventListener("click", resetDeck);


/* ---------- 2. MOBILE NAV --------------------------------- */

const navToggle = document.getElementById("navToggle");
const navLinks  = document.getElementById("navLinks");

navToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

// Close the menu after tapping a link (so the page isn't covered).
navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
  });
});


/* ---------- 3. BOOKING FORM ------------------------------- */

const bookBtn  = document.getElementById("bookBtn");
const formNote = document.getElementById("formNote");

bookBtn.addEventListener("click", () => {
  const name    = document.getElementById("name").value.trim();
  const email   = document.getElementById("email").value.trim();
  const reading = document.getElementById("reading").value;

  // Light validation: just enough to be helpful, not strict.
  if (!name || !email || !reading) {
    formNote.style.color = "var(--ink)";
    formNote.textContent = "Just need your name, email, and a reading first.";
    return;
  }

  // No backend in this demo, so we confirm warmly and reset.
  formNote.style.color = "var(--ink)";
  formNote.textContent = `Thank you, ${name}! I'll email you within a day to find a time.`;

  document.getElementById("name").value = "";
  document.getElementById("email").value = "";
  document.getElementById("reading").value = "";
  document.getElementById("note").value = "";
});