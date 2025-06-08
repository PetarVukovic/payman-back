
# 🧠 AI Payflow Backend

AI Payflow je SaaS platforma za automatizaciju B2B plaćanja korištenjem AI parsing-a, Payman AI payment agenta, stablecoina i EU-compliant payment procesa.

---

## 🚀 Glavni cilj sustava

AI agent automatski:

- Prima fakture (PDF/XML)
- Parsira invoice podatke
- Validira invoice
- Kreira dobavljače (payees)
- Inicira approval flow (Telegram bot)
- Izvršava plaćanja kroz Payman AI SDK
- Generira ERP reporting za računovodstvo

---

## 🏗 Tehnologije

- Python 3.13
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic v2
- pytest
- Docker (kasnije)
- Telegram Bot API
- Payman SDK (Node.js bridge)

---

## 🛢 Struktura baze podataka

### 📦 1️⃣ USERS

- **Opis**: SaaS korisnici (npr. Ivan, vlasnik IT agencije)
- **Atributi**: email, password_hash, telegram_chat_id, subscription_plan
- **Povezano sa**: Payees, Invoices, Payments, Approvals, Subscriptions, Audit Logs

**Primjer**:
> Ivan ima SaaS račun, upravlja plaćanjem za svoje freelancere i dobavljače.

---

### 📦 2️⃣ PAYEES

- **Opis**: Dobavljači ili freelanceri kojima se plaća
- **Atributi**: supplier_name, IBAN, wallet_address, KYC status, country
- **Povezano sa**: Users, Invoices, Approvals, Payments

**Primjer**:
> Ivan ima 3 freelancera:
> - Marko (Croatia)
> - John (US)
> - Anja (Germany)

---

### 📦 3️⃣ INVOICES

- **Opis**: Invoice-i koje AI agent prima i parsira
- **Atributi**: invoice_number, file_url, amount, currency, due_date, parsing_status
- **Povezano sa**: Users, Payees, Approvals, Payments

**Primjer**:
> Ivan primi invoice od Marka za 2.500 EUR koji dospijeva za 7 dana.

---

### 📦 4️⃣ APPROVAL REQUESTS

- **Opis**: Human-in-the-loop approval flow (Telegram notifikacije)
- **Atributi**: status (pending, approved, rejected), approved_at
- **Povezano sa**: Users, Invoices, Payees

**Primjer**:
> Telegram bot šalje Ivanu poruku:
> "*Primljen invoice za 2500 EUR za Marka. Želite li odobriti?*"

---

### 📦 5️⃣ PAYMENTS

- **Opis**: Izvršene transakcije kroz Payman AI SDK
- **Atributi**: amount, currency, status, payman_tx_id
- **Povezano sa**: Invoices, Payees

**Primjer**:
> Ivan odobrava isplatu → Payman AI izvršava payment → status: PAID

---

### 📦 6️⃣ AUDIT LOGS

- **Opis**: Sve akcije za regulatorni audit i ERP export
- **Atributi**: event_type, data (JSON)
- **Povezano sa**: Users

**Primjer**:
> Log za kreiranje payee-a, upload invoice-a, izvršavanje paymenta.

---

### 📦 7️⃣ SUBSCRIPTIONS

- **Opis**: SaaS billing i subscription management (Stripe)
- **Atributi**: plan, trial_end, status
- **Povezano sa**: Users

**Primjer**:
> Ivan je na PRO planu (1000 EUR/mj) i ima pristup svim agentima.

---

## 🧬 Entity Relationship (ER) Dijagram

```plaintext
[USERS] 1---n [PAYEES] 1---n [INVOICES] 1---1 [APPROVAL_REQUESTS] 1---1 [PAYMENTS]
               ↘                                      ↘
                ↘                                      ↘
             [AUDIT_LOGS]                         [SUBSCRIPTIONS]


⸻

⚙ Arhitektura sustava

User Upload -> FastAPI Backend -> AI Parsing (Mindee) -> Validation -> Payee Auto-Creation ->
Approval Flow (Telegram Bot) -> Payment Orchestration -> Payman Node.js SDK -> Payman Platform ->
Postgres Database -> ERP Export -> Reporting


⸻

📂 Projektna struktura

project_root/
│
├── app/
│   ├── main.py (FastAPI entry)
│   ├── database.py (DB setup)
│   ├── models.py (SQLAlchemy models)
│   ├── schemas.py (Pydantic schemas)
│   ├── crud.py (business logic)
│   └── api/ (API routers)
│        ├── users.py
│        ├── payees.py
│        └── invoices.py ...
│
├── tests/
│   └── test_endpoints.py (pytest tests)
│
├── .env (DB credentials)
├── requirements.txt
└── README.md (ova dokumentacija)


⸻

🔧 Pokretanje projekta

1️⃣ Kreiraj virtualno okruženje:

python -m venv venv
source venv/bin/activate

2️⃣ Instaliraj sve pakete:

pip install -r requirements.txt

3️⃣ Postavi DATABASE_URL u .env:

DATABASE_URL=postgresql://username:password@localhost:5432/payman-ai

4️⃣ Pokreni server:

uvicorn app.main:app --reload

5️⃣ Pokreni testove:

pytest


⸻

🔐 Sigurnosne napomene
	•	Nikada ne upload-ati .env u repozitorij.
	•	Nikada ne hardcodirati API ključeve za Payman SDK i Stripe u kodu.
	•	Svi webhook endpointi moraju imati signature verificiranje.

⸻

📈 Primjer realnog korisničkog scenarija (Ivan IT agencija)

1️⃣ Ivan se registrira kroz SaaS web stranicu (free trial 7 dana).

2️⃣ Povezuje Telegram bota → dobiva personalizirani link.

3️⃣ Počinje uploadati invoice-e svojih freelancera:
	•	Marko šalje fakturu 2.500 EUR
	•	John šalje fakturu 3.000 USD

4️⃣ AI agent parsira invoice-e automatski.

5️⃣ Ivan dobiva Telegram notifikaciju za svaku uplatu → klikne APPROVE.

6️⃣ Payman AI izvršava plaćanja kroz USDC stablecoin → freelancers dobivaju sredstva.

7️⃣ Ivanov računovođa kroz web dashboard preuzima ERP export CSV za knjigovodstvo.

⸻

📊 Approximation za SaaS scale:
	•	✅ 1 korisnik: 5-50 payeea
	•	✅ 1 user ≈ 5-10 invoices mjesečno
	•	✅ SaaS server podnosi 10k invoices mjesečno uz optimizaciju

⸻

🚀 Roadmap za produkciju
	•	Docker Compose full setup
	•	Telegram bot webhook deployment
	•	Payman SDK Node.js microservice
	•	AI parsing pipeline (Mindee)
	•	Subscription billing (Stripe)
	•	ERP export automation

⸻

Lead developer: Petar Vuković
Product version: MVP v1.0
Last update: June 2025

⸻


---

**John:**  
Petre — ovo je sad tvoj pravi SaaS project-level dokument. Možeš ga pokazati svakom developeru, investitoru ili partneru i svi će znati gdje je projekt.

**Chris:**  
Dok ovako dokumentiraš projekt → možeš skalirati i onboardingati nove developere za 1 sat, umjesto 3 tjedna.

---

