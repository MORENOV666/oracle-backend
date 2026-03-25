from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import hashlib
import random

app = FastAPI()

# --- CORS CONFIG -------------------------------------------------------------

origins = [
    "https://a1quantumoracleai.com",
    "https://www.a1quantumoracleai.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REQUEST MODEL -----------------------------------------------------------

class ProphecyRequest(BaseModel):
    question: str
    mode: str | None = "free"  # reserved for future (bound glyph, etc.)

# --- SIXFOLD ANALYTIC CORE ---------------------------------------------------

def seed_from_question(question: str) -> int:
    """
    Deterministic seed from the question so:
    - Same question → same prophecy
    - Different question → different prophecy
    """
    h = hashlib.sha256(question.strip().encode("utf-8")).hexdigest()
    # Take a slice to keep it in int range
    return int(h[:12], 16)


def analyze_intent(question: str) -> str:
    q = question.lower()
    if any(word in q for word in ["love", "partner", "relationship", "marriage"]):
        return "heart"
    if any(word in q for word in ["work", "career", "job", "business"]):
        return "path_of_work"
    if any(word in q for word in ["money", "finance", "wealth", "debt"]):
        return "coin"
    if any(word in q for word in ["health", "body", "illness", "energy"]):
        return "vitality"
    if any(word in q for word in ["future", "destiny", "fate", "timeline"]):
        return "destiny"
    return "mystery"


def extract_tension(question: str) -> str:
    q = question.lower()
    if any(word in q for word in ["afraid", "fear", "worried", "anxious"]):
        return "fear"
    if any(word in q for word in ["stuck", "blocked", "trapped"]):
        return "stagnation"
    if any(word in q for word in ["hope", "excited", "eager"]):
        return "anticipation"
    return "uncertainty"


def map_timeline(question: str, rng: random.Random) -> str:
    # Rough symbolic timing, not literal
    options = [
        "near-term currents",
        "mid-cycle unfolding",
        "long-arc convergence",
        "hidden, slow-forming strata",
    ]
    return rng.choice(options)


def weigh_convergence(intent: str, tension: str, rng: random.Random) -> str:
    # Blend intent + tension into a qualitative outcome
    base = rng.randint(0, 100)

    if intent == "heart":
        base += 10
    if intent == "path_of_work":
        base += 5
    if tension == "fear":
        base -= 10
    if tension == "stagnation":
        base -= 5
    if tension == "anticipation":
        base += 5

    if base >= 75:
        return "favored_shift"
    elif base >= 50:
        return "possible_with_alignment"
    elif base >= 30:
        return "delayed_or_conditional"
    else:
        return "unlikely_in_current_pattern"


def derive_lesson(question: str, rng: random.Random) -> str:
    fragments = [
        "a lesson in trust of your own signal",
        "a call to refine what you are truly asking for",
        "an invitation to release an old pattern that no longer fits",
        "a reminder that your pace and the world’s pace rarely match perfectly",
        "a nudge to name your desire more clearly, even to yourself",
        "a quiet insistence that you are not behind, only mid‑cycle",
    ]
    return rng.choice(fragments)


def compose_prophecy(question: str) -> str:
    # Seed RNG from question for deterministic uniqueness
    seed = seed_from_question(question)
    rng = random.Random(seed)

    intent = analyze_intent(question)
    tension = extract_tension(question)
    timeline = map_timeline(question, rng)
    convergence = weigh_convergence(intent, tension, rng)
    lesson = derive_lesson(question, rng)

    # Intent-specific flavor
    if intent == "heart":
        domain_line = "In the chambers of connection and affection, the pattern brightens around you."
    elif intent == "path_of_work":
        domain_line = "Along the corridors of work and craft, new structures begin to outline themselves."
    elif intent == "coin":
        domain_line = "In the ledgers of exchange and resource, subtle rebalancing is already underway."
    elif intent == "vitality":
        domain_line = "Within the fields of body and vitality, your system seeks a more honest rhythm."
    elif intent == "destiny":
        domain_line = "Across the broader arcs of destiny, your thread glows more distinctly than you think."
    else:
        domain_line = "In the unlabelled territory of your question, the pattern refuses simple naming."

    # Convergence interpretation
    if convergence == "favored_shift":
        convergence_line = "Under this symbolic sky, the shift you seek is strongly favored."
    elif convergence == "possible_with_alignment":
        convergence_line = "The shift is possible, but it leans toward those who act in alignment with their own truth."
    elif convergence == "delayed_or_conditional":
        convergence_line = "The shift is delayed, or arrives only when a condition you already sense is finally met."
    else:
        convergence_line = "In the current pattern, the shift resists forming, asking you to reconsider the frame of the question."

    # Timeline line
    timeline_line = f"The currents cluster around {timeline}, not as a fixed date, but as a phase of readiness."

    # Closing
    closing_options = [
        "Several timelines shimmer; your choices determine which one condenses into form.",
        "Nothing is guaranteed, but your attention is already bending the field.",
        "The Oracle does not command outcomes; it shows you where the pattern is softest to your touch.",
        "From here, even a small, honest action can tilt the entire arrangement.",
    ]
    closing_line = rng.choice(closing_options)

    # Final assembly
    prophecy = (
        "The Veil stirs. The currents gather around your question. "
        f"{domain_line} "
        f"{convergence_line} "
        f"{timeline_line} "
        f"In this, the Oracle reads {lesson}. "
        f"{closing_line}"
    )

    return prophecy

# --- ENDPOINT ----------------------------------------------------------------

@app.post("/prophecy")
async def prophecy_endpoint(payload: ProphecyRequest):
    question = (payload.question or "").strip()

    if not question:
        return {
            "oracle_text": (
                "The Veil stirs, but finds no clear glyph to read. "
                "Offer a question with shape, and the pattern will respond."
            )
        }

    oracle_text = compose_prophecy(question)
    return {"oracle_text": oracle_text}
