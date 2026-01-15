
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 07:05:00

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Numeric, Text, JSON, Time
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.core import GUID, ProductStation, UnitOfMeasure, product_recommendations

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    order_index = Column(Integer, default=0)
    availability_days = Column(JSON, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)

    company = relationship("Company", back_populates="categories")
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    short_code = Column(String(10), nullable=True, index=True)
    track_stock = Column(Boolean, default=False)
    stock_quantity = Column(Integer, default=0)
    
    station = Column(String(50), default=ProductStation.KITCHEN.value, nullable=False)
    
    tags = Column(JSON, default=[])
    ncm = Column(String(10), default="21069090")
    cfop = Column(String(5), default="5102")
    external_id = Column(String(100), nullable=True, index=True)

    category = relationship("Category", back_populates="products")
    option_groups = relationship("OptionGroup", back_populates="product", cascade="all, delete-orphan")
    recipe_items = relationship("ProductRecipe", back_populates="product", cascade="all, delete-orphan")
    
    recommendations = relationship(
        "Product",
        secondary=product_recommendations,
        primaryjoin=id==product_recommendations.c.source_product_id,
        secondaryjoin=id==product_recommendations.c.target_product_id,
        backref="recommended_by"
    )

class OptionGroup(Base):
    __tablename__ = "option_groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(100), nullable=False)
    min_selection = Column(Integer, default=0)
    max_selection = Column(Integer, default=1)

    product = relationship("Product", back_populates="option_groups")
    options = relationship("Option", back_populates="group", cascade="all, delete-orphan")

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_id = Column(Integer, ForeignKey("option_groups.id"), nullable=False)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), default=0)
    is_available = Column(Boolean, default=True)

    group = relationship("OptionGroup", back_populates="options")

class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True)
    name = Column(String(255), nullable=False)
    
    unit = Column(String(20), default=UnitOfMeasure.UN.value, nullable=False)
    
    current_stock = Column(Numeric(10, 3), default=0.000)
    min_stock_alert = Column(Numeric(10, 3), default=0.000)
    cost_per_unit = Column(Numeric(10, 2), default=0.00)

    company = relationship("Company", back_populates="ingredients")
    supplier = relationship("Supplier", back_populates="ingredients")
    product_links = relationship("ProductRecipe", back_populates="ingredient")

class ProductRecipe(Base):
    __tablename__ = "product_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)
    quantity_required = Column(Numeric(10, 3), nullable=False)

    product = relationship("Product", back_populates="recipe_items")
    ingredient = relationship("Ingredient", back_populates="product_links")

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(GUID(), ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    company = relationship("Company", back_populates="suppliers")
    ingredients = relationship("Ingredient", back_populates="supplier")

