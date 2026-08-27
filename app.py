from fastapi import FastAPI, HTTPException
from python.nhtsa_vin_decoder import NHTSAVinDecoder
from python.wmi_database import WMIDatabase

app = FastAPI(title="VIN Decoder API")
decoder = NHTSAVinDecoder()

@app.get("/api/decode/{vin}")
def decode_vin(vin: str):
    vin = vin.strip().upper()
    if len(vin) != 17:
        raise HTTPException(status_code=400, detail="Invalid VIN length (must be 17 characters).")
    try:
        vehicle = decoder.decode(vin)
        return {
            "vin": vin,
            "year": getattr(vehicle, "year", None),
            "make": getattr(vehicle, "make", None),
            "model": getattr(vehicle, "model", None),
            "trim": getattr(vehicle, "trim", None),
            "body_class": getattr(vehicle, "body_class", None),
            "raw_data": getattr(vehicle, "raw_data", None)
        }
    except Exception as e:
        manufacturer = WMIDatabase.get_manufacturer(vin)
        year = WMIDatabase.get_year(vin)
        return {
            "vin": vin,
            "year": year,
            "make": manufacturer,
            "source": "offline_fallback",
            "error": str(e)
        }
