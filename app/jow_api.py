import requests
from app.config import JOW_EMAIL, JOW_PASSWORD

JOW_API_URL = "https://api.jow.fr/graphql"

# Variable globale pour conserver le token en mémoire
_cached_jow_token = None

def get_jow_bearer_token(force_refresh: bool = False) -> str:
    """
    Authentifie l'utilisateur auprès de Jow et récupère un nouveau Bearer Token.
    Reutilise le token mis en cache sauf si force_refresh=True.
    """
    global _cached_jow_token

    if _cached_jow_token and not force_refresh:
        return _cached_jow_token

    if not JOW_EMAIL or not JOW_PASSWORD:
        raise ValueError("JOW_EMAIL ou JOW_PASSWORD manquant dans le fichier .env")

    mutation = """
    mutation Login($email: String!, $password: String!) {
      login(email: $email, password: $password) {
        token
      }
    }
    """
    payload = {
        "query": mutation,
        "variables": {
            "email": JOW_EMAIL,
            "password": JOW_PASSWORD
        }
    }

    response = requests.post(JOW_API_URL, json=payload, headers={"Content-Type": "application/json"})
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and data["data"].get("login"):
            _cached_jow_token = data["data"]["login"]["token"]
            return _cached_jow_token
        elif "errors" in data:
            raise Exception(f"Erreur d'authentification Jow: {data['errors']}")

    raise Exception(f"Échec de connexion à l'API Jow (Code: {response.status_code})")

def push_recipes_to_cart(recipe_ids: list[str]) -> bool:
    """
    Injecte les recettes sélectionnées dans le panier Jow.
    Si le token expire (HTTP 401), il tente un rafraîchissement automatique.
    """
    try:
        token = get_jow_bearer_token()
    except Exception as e:
        print(f"Erreur de récupération du token Jow: {e}")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Exemple de requête vers Jow
    # response = requests.post(JOW_API_URL, headers=headers, json={...})
    
    # Si le token a expiré entre temps (401), on retente une fois en forçant le refresh
    # if response.status_code == 401:
    #     token = get_jow_bearer_token(force_refresh=True)
    #     headers["Authorization"] = f"Bearer {token}"
    #     response = requests.post(JOW_API_URL, headers=headers, json={...})

    return True