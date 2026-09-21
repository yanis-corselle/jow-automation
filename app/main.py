import random
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

from app.config import API_KEY, load_meat_keywords
from app.jow_api import fetch_and_filter_recipes, push_recipes_to_cart

app = FastAPI(
    title="Jow Automation API",
    description="API de génération de menu haute protéine avec séparation boucherie et panier Drive",
    version="1.0.0"
)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API invalide ou manquante",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

class MenuRequest(BaseModel):
    meal_count: int = 7
    min_protein: int = 30

class MenuResponse(BaseModel):
    selected_meals: list[str]
    boucherie_list: list[str]
    drive_items_count: int
    jow_push_status: str

@app.post("/api/v1/generate-menu", response_model=MenuResponse, dependencies=[Depends(verify_token)])
def generate_menu(payload: MenuRequest):
    meat_keywords = load_meat_keywords()
    filtered_recipes = fetch_and_filter_recipes(min_protein=payload.min_protein)

    if not filtered_recipes:
        raise HTTPException(status_code=404, detail="Aucune recette trouvée respectant le critère de protéines.")

    # Tirage aléatoire sans répétition
    count = min(payload.meal_count, len(filtered_recipes))
    selected = random.sample(filtered_recipes, k=count)

    boucherie_items = []
    drive_ingredients = []

    for meal in selected:
        for ing in meal.get("ingredients", []):
            ing_name = ing.get("name", "")
            if any(kw in ing_name.lower() for kw in meat_keywords):
                boucherie_items.append(f"{ing_name} ({ing.get('qty', '')}) — pour {meal['name']}")
            else:
                drive_ingredients.append(ing)

    # Push sur Jow
    selected_ids = [m["id"] for m in selected]
    pushed = push_recipes_to_cart(selected_ids)
    push_status = "Succès" if pushed else "Échec / Token manquant"

    return MenuResponse(
        selected_meals=[f"{m['name']} ({m['protein']}g prot)" for m in selected],
        boucherie_list=boucherie_items,
        drive_items_count=len(drive_ingredients),
        jow_push_status=push_status
    )