
# DOMAIN: BACKEND
# LAST_MODIFIED: 2026-01-11 04:40:00
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sqlalchemy.orm import Session
from app.models import Order, PaymentStatus
from app.core.ai_guards import ai_resource_guard, validate_dataset_size
from datetime import datetime, timedelta

class AiPredictionService:
    @staticmethod
    @ai_resource_guard
    def predict_sales(db: Session, company_id: str, days_ahead: int = 7):
        """
        Retorna a previsão de vendas com proteção de recursos (RFC-011).
        """
        data = AiPredictionService._get_historical_data(db, company_id)
        
        # Validação de Limites (RFC-011)
        validate_dataset_size(len(data))
        
        if len(data) < 10:
            return {
                "status": "insufficient_data", 
                "message": "Mínimo de 10 pedidos necessários para análise preditiva."
            }

        df = pd.DataFrame(data, columns=['date', 'amount'])
        df['date'] = pd.to_datetime(df['date']).dt.date
        
        # Agregação diária
        daily = df.groupby('date')['amount'].sum().reset_index()
        
        if len(daily) < 5:
            return {
                "status": "insufficient_data", 
                "message": "Histórico de dias insuficiente (mínimo 5 dias)."
            }

        return AiPredictionService._train_and_forecast(daily, days_ahead)

    @staticmethod
    def _get_historical_data(db, company_id):
        # Limita a busca aos últimos 90 dias para manter o dataset leve
        start_date = datetime.now() - timedelta(days=90)
        return db.query(Order.created_at, Order.total_amount).filter(
            Order.company_id == company_id,
            Order.payment_status == PaymentStatus.PAID,
            Order.created_at >= start_date
        ).limit(10000).all() # Hard limit no DB

    @staticmethod
    def _train_and_forecast(daily, days_ahead):
        daily['ordinal'] = pd.to_datetime(daily['date']).map(datetime.toordinal)
        X = daily[['ordinal']]
        y = daily['amount']
        
        model = LinearRegression().fit(X, y)
        
        last_date = daily['date'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, days_ahead + 1)]
        future_X = np.array([d.toordinal() for d in future_dates]).reshape(-1, 1)
        
        preds = model.predict(future_X)
        
        forecast = [
            {
                "date": d.strftime("%Y-%m-%d"), 
                "predicted_revenue": max(0, round(float(p), 2))
            }
            for d, p in zip(future_dates, preds)
        ]
        
        return {
            "status": "success", 
            "forecast": forecast, 
            "accuracy_score": round(float(model.score(X, y)), 4),
            "engine": "LinearRegression_v1"
        }

