from fastapi import FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI()

# CORS (si tu utilises un front local)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser tous les domaines (à adapter en prod)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Personnage(BaseModel):
    nom: str
    role: str

personnages = [
    Personnage(nom="Link", role="Héros d'Hyrule"),
    Personnage(nom="Samus Aran", role="Chasseuse de primes"),
    Personnage(nom="Mario", role="Plombier")
]

@app.get("/personnages", response_model=List[Personnage])
def get_personnages(token: str = Header(...), prenom: Optional[str] = Query(None)):
    if token != "secret123":
        raise HTTPException(status_code=401, detail="Token invalide")

    if prenom:
        return [p for p in personnages if p.nom.lower().startswith(prenom.lower())]
    return personnages
