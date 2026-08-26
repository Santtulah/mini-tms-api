
import re
from database import get_db_connection

def extract_delivery_info(message: str):
    """
    Perkaa tekstistä Regexin avulla rekisterinumeron, postinumeron ja hinnan.
    """
    plate_match =  re.search(r"[a-zA-ZåäöÅÄÖ]{2,3}-\d{1,3}", message)
    postal_match = re.search(r"\b\d{5}\b", message)
    price_match = re.search(r"(\d+)\s*(e|E|€|eur|euroa)", message)

    return {
        "license_plate": plate_match.group(0).upper() if plate_match else None,
        "postal_code": postal_match.group(0) if postal_match else None,
        "price": float(price_match.group(1)) if price_match else None,
        "raw_message": message
    }



