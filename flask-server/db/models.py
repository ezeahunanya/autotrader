from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .database import engine, Base
from sqlalchemy.dialects.postgresql import JSONB


class Prediction(Base): 
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True)
    price_prediction = Column(Float, nullable=False)
    feature_values = Column(JSONB)
    shap_values = Column(JSONB)
    ip_address = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # using 'server_default' parameter instead of 'default' ensures the DateTime value will be handled by the sql server as opposed to us here on the app (client of the db server)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

Base.metadata.create_all(engine)