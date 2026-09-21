import random
import requests
from app.config import JOW_BEARER_TOKEN

JOW_API_URL = "https://api.jow.fr/graphql"  # Endpoint GraphQL privé Jow

def fetch_and_filter_recipes(min_protein: int = 30) -> list[dict]:
    """
    Interroge l'API Jow pour récupérer les recettes et filtrer par protéines.
    Note : Adapter le payload GraphQL selon les endpoints de Jow.
    """
    # Exemple de structure retournée après parsing des recettes Jow
    # Remplace cette simulation par l'appel requests.post réel vers l'API Jow
    mock_recipes = [
        {"id": "rec_1", "name": "Poulet Basquaise", "protein": 38, "ingredients": [{"name": "Filet de poulet", "qty": "400g"}, {"name": "Poivron", "qty": "2"}]},
        {"id": "rec_2", "name": "Pavé de Saumon et Riz", "protein": 34, "ingredients": [{"name": "Pavé de saumon", "qty": "2"}, {"name": "Riz", "qty": "200g"}]},
        {"id": "rec_3", "name": "Steak Haché & Patates Douces", "protein": 42, "ingredients": [{"name": "Steak haché 5%", "qty": "2"}, {"name": "Patate douce", "qty": "500g"}]},
        {"id": "rec_4", "name": "Pâtes Carbonara", "protein": 18, "ingredients": [{"name": "Pâtes", "qty": "250g"}, {"name": "Lardons", "qty": "150g"}]},
        {"id": "rec_5", "name": "Escalope de Dinde & Quinoa", "protein": 36, "ingredients": [{"name": "Escalope de dinde", "qty": "300g"}, {"name": "Quinoa", "qty": "150g"}]}
    ]
    return [r for r in mock_recipes if r.get("protein", 0) >= min_protein]

def push_recipes_to_cart(recipe_ids: list[str]) -> bool:
    """
    Injecte les recettes sélectionnées dans le panier Drive via l'API Jow.
    """
    if not JOW_BEARER_TOKEN:
        return False
    
    headers = {
        "Authorization": f"Bearer {JOW_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }
    # Exemple d'appel API pour ajouter au panier
    # response = requests.post(JOW_API_URL, headers=headers, json={...})
    # return response.status_code == 200
    return True