from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "LIEN DE VOTRE DATABASE"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine)
Base = declarative_base()

def create_tables():
    try:
        # Import models here to ensure they are registered with Base
        from models import Product_Product, Product_Template, Product_Category, Stock_Quant, Ir_Property
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully!")
    except Exception as ex:
        print(f"Error creating tables: {ex}")

try:
    conn = engine.connect()
    print("Connecté avec succes")
except Exception as ex:
    print(ex)





SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


