from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
import models, schemas
from dependencies import get_password_hash









def get_product_by_barcode(db: Session, code_barre: str):
    return db.query(models.Product_Product).filter(
        models.Product_Product.barcode == code_barre
        ).first()



def get_product_template_by_id(db: Session, product_tmpl_id: int):
    return db.query(models.Product_Template).filter(
        models.Product_Template.id == product_tmpl_id
        ).first()



def get_product_category_by_id(db: Session, categ_id: int):
    return db.query(models.Product_Category).filter(
        models.Product_Category.id == categ_id
        ).first()



def get_stock_quant_by_product_id(db: Session, product_id: int):
    return db.query(models.Stock_Quant).filter(
        models.Stock_Quant.product_id == product_id, 
        models.Stock_Quant.inventory_date != None
        ).first()





#======================================== Afficher la liste des Produits ============================================





        

def tous_les_produits(db: Session) -> List[schemas.ProductTemplate]:
    les_produits = db.query(models.Product_Product).all()
    result = []

    for un_produit in les_produits:
        if un_produit.product_tmpl_id:
            product_template = db.query(models.Product_Template).filter(models.Product_Template.id == un_produit.product_tmpl_id).first()
            if not product_template:
                continue
            
            le_stock = db.query(models.Stock_Quant).filter(models.Stock_Quant.product_id == un_produit.id, models.Stock_Quant.inventory_date.isnot(None)).all()

            if le_stock:
                for quantité in le_stock:
                    la_categorie = db.query(models.Product_Category).filter(models.Product_Category.id == product_template.categ_id).first()
                    result.append(schemas.ProductTemplate(
                        name=product_template.name,
                        categ_id=product_template.categ_id,
                        list_price=product_template.list_price,
                        categ_name=la_categorie.name if la_categorie else "Catégorie Inconnue",
                        quantity=int(quantité.quantity) if quantité.quantity is not None else 0
                    ))

    return result




# ======================================== Mettre à jour la liste des Produits ============================================








def nouvelle_categorie(db: Session, code_barre: int, nouvelle_id: str):
    product = db.query(models.Product_Product).filter(models.Product_Product.barcode == code_barre).first()
    if product is None:
        return None

    product_template = db.query(models.Product_Template).filter(models.Product_Template.id == product.product_tmpl_id).first()
    if product_template is None:
        return None

    product_template.categ_id = nouvelle_id
    db.commit()
    return product_template






def nouveau_prix(db: Session, barcode: str, new_price: float):
   
    product = db.query(models.Product_Product).filter(models.Product_Product.barcode == barcode).first()
    
    if not product:
        return None 
    product_template = db.query(models.Product_Template).filter(models.Product_Template.id == product.product_tmpl_id).first()
    
    if not product_template:
        return None  
    product_template.list_price = new_price
    db.commit()
    db.refresh(product_template)
    
    return product_template





def mettre_a_jour_prix(db: Session, product_id: int, nouveau_prix: float):
    property_entry = db.query(models.Ir_Property).filter(models.Ir_Property.res_id == f'product.product,{product_id}').first()

    if property_entry is None:
        raise HTTPException(status_code=404, detail="Propriété non trouvée pour ce produit")

    property_entry.value_float = nouveau_prix
    db.commit()
    db.refresh(property_entry)

    return property_entry







# ============================ Authentification ================================



def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()



def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user