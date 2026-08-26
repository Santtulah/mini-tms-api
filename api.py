from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import save_message, get_all_deliveries, save_telematics_ping
from text_parser import extract_delivery_info

# Alustaa API-sovelluksen
app = FastAPI(
    title="LogiApp Mini-TMS API",
    description="Rajapinta kuljetustilausten hallintaan"
)

# Pydantic-malli: Tämä kertoo API:lle, että POST-pyynnön mukana 
# on pakko tulla JSON-objekti, jolla on avain "message" ja arvona tekstiä (str).
class DeliveryPayload(BaseModel):
    message: str

class TelematicsPing(BaseModel):
    license_plate: str
    latitude: float
    longitude: float

# Esimerkkireitti (GET), jolla näemme että palvelin on hengissä
@app.get("/")
def health_check():
    return {"status": "API on pystyssä!"}

@app.get("/api/deliveries")
def get_deliveries():
    """
    Hakee kaikki kuljetustilaukset tietokannasta ja palauttaa ne listana.
    """
    try:
        deliveries = get_all_deliveries()
        return {"status": "success", "deliveries": deliveries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Palvelinvirhe: {e}")

@app.post("/api/deliveries/parse-text")
def parse_delivery_text(payload: DeliveryPayload):
    """
    Tämä reitti vastaanottaa POST-pyynnön, jossa on JSON-objekti, 
    joka sisältää avaimen "message" ja arvona kuljetustilauksen tekstin.
    Se käsittelee tekstin ja tallentaa sen tietokantaan.
    """
    clean_message = extract_delivery_info(payload.message)
    
    if not clean_message.get("license_plate") or not clean_message.get("postal_code"):
        raise HTTPException(status_code=400, detail="Virheellinen syöte: rekisterinumero tai postinumero puuttuu.")

    try:
        success = save_message(clean_message)
        if success:
            return {"status": "success", "message": "Kuljetustilaus käsitelty ja tallennettu tietokantaan."}
        else:
            raise HTTPException(status_code=400, detail="Virhe käsiteltäessä kuljetustilausta. Tarkista syöte.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Palvelinvirhe: {e}")

@app.post("/api/telematics/ping")
def telematics_ping(ping: TelematicsPing):
    """
    Tämä reitti vastaanottaa telematiikkapingin, joka sisältää rekisterinumeron, 
    leveyspiirin ja pituuspiirin. Se tallentaa tiedot tietokantaan.
    """
    try:
        success = save_telematics_ping(ping.license_plate, ping.latitude, ping.longitude)
    except Exception as e:
            raise HTTPException(status_code=500, detail=f"Palvelinvirhe: {e}") 
    
    if success:
        return {"status": "success", "message": "Telematiikkapingi tallennettu."}
    else:
        raise HTTPException(status_code=400, detail="Virhe tallennettaessa telematiikkapingiä. Tarkista syöte.")
