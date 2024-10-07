from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from API.models import Ir_Property, Product_Category, Product_Product, Product_Template, Stock_Quant, User
from API.schemas import ProductTemplate, UserCreate
from API.dependencies import get_password_hash
import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))









def get_product_by_barcode(db: Session, code_barre: str):
    return db.query(Product_Product).filter(
        Product_Product.barcode == code_barre
        ).first()



def get_product_template_by_id(db: Session, product_tmpl_id: int):
    return db.query(Product_Template).filter(
        Product_Template.id == product_tmpl_id
        ).first()



def get_product_category_by_id(db: Session, categ_id: int):
    return db.query(Product_Category).filter(
        Product_Category.id == categ_id
        ).first()



def get_stock_quant_by_product_id(db: Session, product_id: int):
    return db.query(Stock_Quant).filter(
        Stock_Quant.product_id == product_id, 
        Stock_Quant.inventory_date != None
        ).first()





#======================================== Afficher la liste des Produits ============================================





        

def tous_les_produits(db: Session) -> List[ProductTemplate]:
    les_produits = db.query(Product_Product).all()
    result = []

    for un_produit in les_produits:
        if un_produit.product_tmpl_id:
            product_template = db.query(Product_Template).filter(Product_Template.id == un_produit.product_tmpl_id).first()
            if not product_template:
                continue
            
            le_stock = db.query(Stock_Quant).filter(Stock_Quant.product_id == un_produit.id, Stock_Quant.inventory_date.isnot(None)).all()

            if le_stock:
                for quantité in le_stock:
                    la_categorie = db.query(Product_Category).filter(Product_Category.id == product_template.categ_id).first()
                    result.append(ProductTemplate(
                        name=product_template.name,
                        categ_id=product_template.categ_id,
                        list_price=product_template.list_price,
                        categ_name=la_categorie.name if la_categorie else "Catégorie Inconnue",
                        quantity=int(quantité.quantity) if quantité.quantity is not None else 0
                    ))

    return result




# ======================================== Mettre à jour la liste des Produits ============================================








def nouvelle_categorie(db: Session, code_barre: int, nouvelle_id: str):
    product = db.query(Product_Product).filter(Product_Product.barcode == code_barre).first()
    if product is None:
        return None

    product_template = db.query(Product_Template).filter(Product_Template.id == product.product_tmpl_id).first()
    if product_template is None:
        return None

    product_template.categ_id = nouvelle_id
    db.commit()
    return product_template






def nouveau_prix(db: Session, barcode: str, new_price: float):
   
    product = db.query(Product_Product).filter(Product_Product.barcode == barcode).first()
    
    if not product:
        return None 
    product_template = db.query(Product_Template).filter(Product_Template.id == product.product_tmpl_id).first()
    
    if not product_template:
        return None  
    product_template.list_price = new_price
    db.commit()
    db.refresh(product_template)
    
    return product_template





def mettre_a_jour_prix(db: Session, product_id: int, nouveau_prix: float):
    property_entry = db.query(Ir_Property).filter(Ir_Property.res_id == f'product.product,{product_id}').first()

    if property_entry is None:
        raise HTTPException(status_code=404, detail="Propriété non trouvée pour ce produit")

    property_entry.value_float = nouveau_prix
    db.commit()
    db.refresh(property_entry)

    return property_entry







# ============================ Authentification ================================



def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()



def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user