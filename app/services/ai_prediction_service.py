# DOMAIN: BACKEND
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from app.models import Order, OrderStatus, PaymentStatus
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("AiPredictionService")

class AiPredictionService:
    @staticmethod
    def predict_sales(db: Session, company_id: str, days_ahead: int = 7):
        """
        Gera previsão de vendas diárias usando Regressão Linear simples.
        """
        # 1. Extrair dados históricos
        # Busca pedidos pagos dos últimos 90 dias
        start_date = datetime.now() - timedelta(days=90)
        
        orders = db.query(Order.created_at, Order.total_amount).filter(
            Order.company_id == company_id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_date
        ).all()

        if not orders or len(orders) < 10:
            return {"status": "insufficient_data", "message": "Mínimo de 10 pedidos necessários para previsão."}

        # 2. Preparar DataFrame
        df = pd.DataFrame(orders, columns=['date', 'amount'])
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Agrupar por dia
        daily_sales = df.groupby('date')['amount'].sum().reset_index()
        
        if len(daily_sales) < 5:
             return {"status": "insufficient_data", "message": "Mínimo de 5 dias de vendas necessários."}

        # Converter datas para ordinal (numérico) para regressão
        daily_sales['date_ordinal'] = pd.to_datetime(daily_sales['date']).map(datetime.toordinal)

        # 3. Treinar Modelo
        X = daily_sales[['date_ordinal']]
        y = daily_sales['amount']

        model = LinearRegression()
        model.fit(X, y)

        # 4. Prever Futuro
        future_dates = []
        last_date = daily_sales['date'].max()
        
        for i in range(1, days_ahead + 1):
            future_date = last_date + timedelta(days=i)
            future_dates.append(future_date)

        future_ordinal = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
        predictions = model.predict(future_ordinal)

        # 5. Formatar Saída
        forecast = []
        for date, amount in zip(future_dates, predictions):
            # Evitar previsões negativas
            predicted_amount = max(0, round(float(amount), 2))
            forecast.append({
                "date": date.strftime("%Y-%m-%d"),
                "predicted_revenue": predicted_amount
            })

        return {
            "status": "success",
            "model": "linear_regression",
            "forecast": forecast,
            "accuracy_score": float(model.score(X, y)) # R² Score (simples)
        }
