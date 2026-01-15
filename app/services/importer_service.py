
import httpx
from bs4 import BeautifulSoup
import json
from sqlalchemy.orm import Session
from app.models import Category, Product
from decimal import Decimal

class ImporterService:
    @staticmethod
    async def import_from_ifood(db: Session, company_id: str, url: str):
        html = await ImporterService._fetch_html(url)
        menu_data = ImporterService._extract_menu_json(html)
        
        imported_count = 0
        for cat_data in menu_data:
            category = ImporterService._get_or_create_category(db, company_id, cat_data.get("name"))
            items = cat_data.get("itens", []) or cat_data.get("items", [])
            for item in items:
                if ImporterService._create_product(db, category.id, item):
                    imported_count += 1
        db.commit()
        return {"status": "success", "imported_items": imported_count}

    @staticmethod
    async def _fetch_html(url):
        headers = {"User-Agent": "Mozilla/5.0"}
        async with httpx.AsyncClient(follow_redirects=True) as client:
            res = await client.get(url, headers=headers)
            if res.status_code != 200: raise ValueError(f"Erro URL: {res.status_code}")
            return res.text

    @staticmethod
    def _extract_menu_json(html):
        soup = BeautifulSoup(html, 'html.parser')
        script = soup.find("script", {"id": "__NEXT_DATA__"})
        if not script: raise ValueError("Estrutura iFood não encontrada")
        data = json.loads(script.string)
        return data.get("props", {}).get("pageProps", {}).get("menu", [])

    @staticmethod
    def _get_or_create_category(db, company_id, name):
        if not name: return None
        cat = db.query(Category).filter(Category.company_id == company_id, Category.name == name).first()
        if not cat:
            cat = Category(company_id=company_id, name=name)
            db.add(cat)
            db.flush()
        return cat

    @staticmethod
    def _create_product(db, category_id, item):
        name = item.get("description") or item.get("name")
        exists = db.query(Product).filter(Product.category_id == category_id, Product.name == name).first()
        if not exists:
            price = Decimal(str(item.get("unitPrice") or item.get("price", 0)))
            new_p = Product(category_id=category_id, name=name, description=item.get("details", "")[:500], price=price)
            db.add(new_p)
            return True
        return False

