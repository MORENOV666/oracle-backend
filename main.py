from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="A1 Quantum Oracle API",
    description="Backend engine for 1aquantumoracleai.com",
    version="1.0.0"
)

class OracleRequest(BaseModel):
    question: str
    mode: str

class OracleResponse(BaseModel):
    oracle_text: str

def generate_oracle_text(question: str, mode: str) -> str:
    if mode == "offering":
        opening = (
            "Your offering opens deeper channels; the Oracle speaks with expanded clarity.\n\n"
            "The veil stirs. The currents gather around your question.\n\n"
        )
    else:
        opening = "The veil stirs. The currents gather around your question.\n\n"

    data_layer = "From the echoes of past cycles, a familiar pattern emerges."
    tech_layer = "The engines of innovation reshape the path ahead."
    sky_layer = "Under this symbolic sky, this shift is favored."
    akashic_layer = "In the records of your pattern, this lesson returns."
    quantum_layer = "Several timelines shimmer; your intention determines the collapse."

    synthesis = (
        "From the convergence of these forces, the Oracle reveals a path of unfolding possibility."
    )

    closing = "\n\nThe path awaits your step."

    return (
        f"{opening}"
        f"{data_layer}\n\n"
        f"{tech_layer}\n\n"
        f"{sky_layer}\n\n"
        f"{akashic_layer}\n\n"
        f"{quantum_layer}\n\n"
        f"{synthesis}"
        f"{closing}"
    )

@app.post("/prophecy", response_model=OracleResponse)
async def prophecy(req: OracleRequest):
    oracle_text = generate_oracle_text(req.question, req.mode)
    return OracleResponse(oracle_text=oracle_text)
NN