from typing import List
from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from crud import get_product_by_barcode, get_product_category_by_id, get_product_template_by_id, get_stock_quant_by_product_id, mettre_a_jour_prix, tous_les_produits
from dependencies import get_current_user, get_db
from schemas import IrProperty, ProductTemplate, UserInDB
from config import SessionLocal
import sys
import os

# Ajouter le répertoire parent au chemin d'importation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'API')))




router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======================================== Afficher un Produit par son code barre ==================================================


@router.get("/obtenir les produits par:/{barcode}", response_model=ProductTemplate)
def lire_le_produit(
    code_barre: str, 
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
    ):
    product = get_product_by_barcode(db, code_barre)
    if product is None:
        raise HTTPException(status_code=404, detail="Aucun produit trouvé")

    product_template = get_product_template_by_id(
        db, product.product_tmpl_id)
    if product_template is None:
        raise HTTPException(
            status_code=404,
            detail="Modèle de produit non trouvé")

    product_category = get_product_category_by_id(
        db, product_template.categ_id)
    if product_category is None:
        raise HTTPException(status_code=404,
                            detail="Catégorie de produit non trouvée")
    

    stock_quant = get_stock_quant_by_product_id(db, product.id)
    if stock_quant is None:
        raise HTTPException(
            status_code=404, 
            detail="Aucun stock trouvé avec une date valide")


    return ProductTemplate(
        name=product_template.name,
        categ_id=product_template.categ_id,
        list_price=product_template.list_price,
        categ_name=product_category.name,
        quantity=stock_quant.quantity
    )


# ======================================== Afficher la liste des Produits ===============================================





@router.get("/liste des produits/", response_model=List[ProductTemplate])
def voir_tous_les_produits(
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
    ):
    return tous_les_produits(db)




# ======================================== Mettre à jour la liste des Produits ============================================







@router.patch("/modifier un produit par:/{barcode}/catégorie/")
def nouvelle_categorie(
    code_barre: str, 
    nouvelle_id: int = Query(description="ID de la nouvelle catégorie. Choisissez parmi :\n1. All\n2. Saleable\n3. Expeses"),
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    
    categories = {
        1: "All",
        2: "Saleable",
        3: "Expenses"
    }

    if nouvelle_id not in categories:
        raise HTTPException(status_code=400, detail="ID de catégorie invalide")


    product_template = nouvelle_categorie(db, code_barre, nouvelle_id)
    if product_template is None:
        raise HTTPException(status_code=404, detail="Produit ou modèle du produit non trouvé")


    return {
        "message": f"Catégorie mise à jour avec succès en '{categories[nouvelle_id]}'",
        "Modification apportée sur": product_template.name
    }





@router.patch("/modifier un produit par:/{barcode}/prix/")
def nouveau_prix(
    code_barre: str, 
    nouveau_prix: float, 
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
    ):
    product_template = nouveau_prix(db, code_barre, nouveau_prix)
    if product_template is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product_template





@router.patch("/modifier_cout_vente/{product_id}/", response_model=IrProperty)
def modifier_cout_vente(
    product_id: int,
    nouveau_cout: float,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user)
):
    return mettre_a_jour_prix(db, product_id, nouveau_cout)
