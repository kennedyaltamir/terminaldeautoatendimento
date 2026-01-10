# DOMAIN: BACKEND
import httpx
from bs4 import BeautifulSoup
import json
import logging
from sqlalchemy.orm import Session
from app.models import Category, Product, Company
from decimal import Decimal

logger = logging.getLogger("ImporterService")

class ImporterService:
    @staticmethod
    async def import_from_ifood(db: Session, company_id: str, url: str):
        """
        Realiza o scraping de um cardápio público do iFood e popula o banco de dados.
        Estratégia: Busca por dados estruturados (__NEXT_DATA__) para evitar fragilidade de seletores CSS.
        """
        logger.info(f"Iniciando importação iFood para empresa {company_id} via {url}")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code != 200:
                raise ValueError(f"Erro ao acessar URL: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Tenta extrair dados do Next.js (Padrão moderno)
            next_data = soup.find("script", {"id": "__NEXT_DATA__"})
            
            if not next_data:
                raise ValueError("Estrutura de dados do iFood não reconhecida (Anti-bot ou Layout novo).")

            try:
                data = json.loads(next_data.string)
                # Navegação segura pelo JSON (A estrutura pode variar, usamos try/except genérico para fallback)
                restaurant_data = data.get("props", {}).get("pageProps", {}).get("restaurant", {})
                menu_data = data.get("props", {}).get("pageProps", {}).get("menu", [])
                
                if not menu_data:
                    # Tenta caminho alternativo comum em algumas versões
                    initial_state = data.get("props", {}).get("pageProps", {}).get("initialState", {})
                    menu_data = initial_state.get("restaurant", {}).get("menu", [])

            except Exception as e:
                logger.error(f"Erro ao parsear JSON do iFood: {e}")
                raise ValueError("Falha ao processar dados do cardápio.")

            imported_count = 0
            
            for cat_data in menu_data:
                cat_name = cat_data.get("name")
                if not cat_name: continue

                # Criar ou recuperar Categoria
                category = db.query(Category).filter(
                    Category.company_id == company_id,
                    Category.name == cat_name
                ).first()

                if not category:
                    category = Category(
                        company_id=company_id,
                        name=cat_name,
                        order_index=0 # Ajustar depois se necessário
                    )
                    db.add(category)
                    db.commit()
                    db.refresh(category)

                # Processar Produtos
                items = cat_data.get("itens", []) # 'itens' é comum no iFood BR
                if not items: items = cat_data.get("items", [])

                for item in items:
                    prod_name = item.get("description") or item.get("name")
                    prod_desc = item.get("details") or ""
                    prod_price = item.get("unitPrice") or item.get("price", 0)
                    
                    # Sanitização de Preço
                    try:
                        price_decimal = Decimal(str(prod_price))
                    except:
                        price_decimal = Decimal("0.00")

                    # Evitar duplicidade
                    exists = db.query(Product).filter(
                        Product.category_id == category.id,
                        Product.name == prod_name
                    ).first()

                    if not exists:
                        new_product = Product(
                            category_id=category.id,
                            name=prod_name,
                            description=prod_desc[:500], # Limite DB
                            price=price_decimal,
                            is_available=True,
                            station="kitchen" # Default seguro
                        )
                        db.add(new_product)
                        imported_count += 1
            
            db.commit()
            return {"status": "success", "imported_items": imported_count}
