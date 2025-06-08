import json
import re
import requests
from app import models
from sqlalchemy.orm import Session

class PaymanService:
    BASE_URL = "http://localhost:3000"  # Gdje ti je pokrenut Node.js backend

    @staticmethod
    def ask_payman(question: str):
        url = f"{PaymanService.BASE_URL}/ask"
        payload = {"question": question}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling Payman SDK: {e}")
            return None

    @staticmethod
    def parse_and_store_response(response: dict, db: Session, user_id: int):
        if response is None or response.get("status") != "COMPLETED":
            return

        content = response.get("artifacts", [{}])[0].get("content", "")
        print("AI content: ", content)

        # REGEX koji traži sve payee blokove
        pattern = re.compile(r'Payee Name: (.+?)\n\s+- Type: (.+?)\n\s+- Currency: (.+?)(?:\n\s+- Wallet ID: (.+?))?', re.MULTILINE)

        matches = pattern.findall(content)
        print("Parsed payees:", matches)

        for match in matches:
            supplier_name = match[0].strip()
            type_value = match[1].strip()
            currency = match[2].strip()
            wallet_id = match[3].strip() if match[3] else None

            payee = models.Payee(
                user_id=user_id,
                supplier_name=supplier_name,
                iban=None,  # Za sada dummy
                wallet_address=wallet_id or "DUMMY_WALLET",
                kyc_status="pending",
                country="Unknown"
            )
            db.add(payee)

        db.commit()
        print(f"Inserted {len(matches)} payees into database.")
        
    @staticmethod
    def log_payman_response(db: Session, response: dict, user_id: int):
        log_entry = models.AuditLog(
            user_id=user_id,
            event_type="PAYMAN_RESPONSE",
            data=json.dumps(response)
        )
        db.add(log_entry)
        db.commit()