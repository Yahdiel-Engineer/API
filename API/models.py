from sqlalchemy import Column, Date, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from config import Base








class Product_Product(Base):
    __tablename__ = "product_product"

    id = Column(Integer, primary_key=True, index=True)
    product_tmpl_id = Column(Integer, ForeignKey('product_template.id'), index=True)
    barcode = Column(String, unique=True, index=True)

class Product_Template(Base):
    __tablename__ = "product_template"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    categ_id = Column(Integer, ForeignKey('product_category.id'))
    list_price = Column(Float)

class Product_Category(Base):
    __tablename__ = "product_category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Stock_Quant(Base):
    __tablename__ = "stock_quant"

    product_id = Column(Integer, ForeignKey('product_product.id'), primary_key=True, index=True)
    quantity = Column(Integer)
    inventory_date = Column(Date, nullable=True)

class Ir_Property(Base):
    __tablename__ = "ir_property"
    id = Column(Integer, primary_key=True, index=True)
    res_id = Column(Integer, ForeignKey('product_product.id'))
    value_float = Column(Float)



Product_Product.product_template = relationship("Product_Template", back_populates="product_product")
Product_Template.product_product = relationship("Product_Product", back_populates="product_template")
Product_Template.product_category = relationship("Product_Category", back_populates="product_template")
Product_Category.product_template = relationship("Product_Template", back_populates="product_category")
Product_Product.stock_quant = relationship("Stock_Quant", back_populates="product_product")
Stock_Quant.product_product = relationship("Product_Product", back_populates="stock_quant")
Ir_Property.product_product = relationship("Product_Product", back_populates="ir_property")
Product_Product.ir_property = relationship("Ir_Property", back_populates="product_product")




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
