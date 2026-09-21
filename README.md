# 🛒 Jow High-Protein Menu Generator & Butcher List Splitter

A lightweight **FastAPI** microservice designed to run on a Raspberry Pi (or any Linux server). It automates weekly meal planning on **Jow** based on strict macronutrient constraints (minimum protein per serving), selects non-repetitive random recipes, pushes items to your grocery drive, and separates meat products into a dedicated local butcher shopping list.

---

## 🌟 Key Features

- **Macro Filtering:** Selects recipes matching a minimum protein threshold per serving (e.g., $\ge 30\text{g}$).
- **Randomized Selection:** Randomly picks $N$ meals without duplicates to ensure meal variety.
- **Butcher Items Isolation:** Automatically detects meat and poultry ingredients via an external configuration file (`data/meat_keywords.json`) and excludes them from the automated grocery drive cart.
- **Multi-Language Ready:** Meat identification keywords are decoupled from code logic for easy localization.
- **Bearer Token Auth:** Secured endpoint protected by an API key header.

---

## 📁 Repository Structure

```text
jow-automation/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── jow_api.py
│   └── main.py
├── data/
│   └── meat_keywords.json
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── jow-automation.service
```

---

## 🥩 Meat Keyword Configuration

Keywords used to filter out butcher items are decoupled from application logic and stored in `data/meat_keywords.json`. You can modify this file to support different languages or add specific meat types:

```json
{
  "keywords": [
    "poulet",
    "boeuf",
    "dinde",
    "steak",
    "porc",
    "haché",
    "veau",
    "agneau"
  ]
}
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.10+
- A Jow account
- A Linux host (e.g., Raspberry Pi)

### 1. Local Setup
```bash
git clone https://github.com/your-username/jow-automation.git
cd jow-automation

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables
Copy `.env.example` to `.env` and configure your keys:
```bash
cp .env.example .env
```

```ini
API_KEY=your_very_long_secret_api_key_here
JOW_BEARER_TOKEN=your_jow_bearer_token_here
```

### 3. Running Locally
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## ⚙️ Service Deployment (Systemd on Raspberry Pi)

1. Create a systemd unit file:
   ```bash
   sudo nano /etc/systemd/system/jow-automation.service
   ```

2. Add the following content:
   ```ini
   [Unit]
   Description=Jow Automation FastAPI Service
   After=network.target

   [Service]
   User=pi
   WorkingDirectory=/home/pi/jow-automation
   ExecStart=/home/pi/jow-automation/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always
   RestartSec=5

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable jow-automation.service
   sudo systemctl start jow-automation.service
   ```

---

## 🌐 Public Exposure (Freebox Port Forwarding)

1. Reserve a static IP address for your Raspberry Pi in your Freebox admin interface (`http://mafreebox.freebox.fr` -> **Paramètres** -> **DHCP** -> **Baux statiques**).
2. Configure a Port Forwarding rule (**Paramètres** -> **Gestion des accès** -> **Redirection de ports**):
   - **IP Address:** `<RASPBERRY_PI_IP>`
   - **Protocol:** TCP
   - **External Port:** `8443`
   - **Internal Port:** `8000`

---

## 📡 API Reference

### `POST /api/v1/generate-menu`

Generates a randomized menu, filters ingredients, pushes non-butcher items to Jow, and returns the butcher list.

#### Headers
| Header | Value |
|---|---|
| `Authorization` | `Bearer <YOUR_API_KEY>` |
| `Content-Type` | `application/json` |

#### Request Body
```json
{
  "meal_count": 7,
  "min_protein": 30
}
```

#### Response Example (`200 OK`)
```json
{
  "selected_meals": [
    "Poulet Basquaise (38g prot)",
    "Steak Haché & Patates Douces (42g prot)"
  ],
  "boucherie_list": [
    "Filet de poulet (400g) — pour Poulet Basquaise",
    "Steak haché 5% (2) — pour Steak Haché & Patates Douces"
  ],
  "drive_items_count": 4,
  "jow_push_status": "Success"
}
```

---

## 🤖 Mobile Integration

You can trigger this API directly from your smartphone using automation tools like **iOS Shortcuts**, **HTTP Shortcuts (Android)**, or **Tasker**:

1. Configure an HTTP `POST` action targeting `http://<YOUR_PUBLIC_IP>:8443/api/v1/generate-menu`.
2. Pass your `API_KEY` in the `Authorization` header (`Bearer <API_KEY>`).
3. Display the returned `boucherie_list` array directly in a native smartphone note or notification.
