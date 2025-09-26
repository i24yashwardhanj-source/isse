# -*- coding: utf-8 -*-
"""
Data schemas for validation of input dataframes using pandera.

Ensures data quality and prevents errors in downstream models by enforcing
strict data type and value constraints.
"""
import pandera as pa
from pandera.typing import Series, DateTime

class SyntheticOrdersSchema(pa.SchemaModel):
    """Schema for the synthetic customer orders data."""
    order_id: Series[str] = pa.Field(nullable=False, unique=True)
    customer_id: Series[str] = pa.Field(nullable=False)
    order_date: Series[DateTime] = pa.Field(nullable=False)
    revenue_inr: Series[float] = pa.Field(ge=0, nullable=False)

    class Config:
        strict = True
        coerce = True

class SyntheticMarketingSpendSchema(pa.SchemaModel):
    """Schema for the synthetic marketing spend time-series data."""
    date: Series[DateTime] = pa.Field(nullable=False, unique=True)
    social_media: Series[float] = pa.Field(ge=0, nullable=False)
    search: Series[float] = pa.Field(ge=0, nullable=False)
    influencer: Series[float] = pa.Field(ge=0, nullable=False)

    class Config:
        strict = True
        coerce = True

class SyntheticB2BPipelineSchema(pa.SchemaModel):
    """Schema for the synthetic B2B sales pipeline data."""
    lead_id: Series[str] = pa.Field(nullable=False, unique=True)
    lead_source: Series[str] = pa.Field(isin=['Inbound', 'Outbound'])
    project_type: Series[str] = pa.Field(isin=['HNWI', 'Designer', 'Institutional', 'Developer'])
    potential_value_inr: Series[float] = pa.Field(ge=0, nullable=False)
    is_won: Series[int] = pa.Field(isin=[0, 1], coerce=True)

    class Config:
        strict = True
        coerce = True

class SyntheticWarehouseLocationsSchema(pa.SchemaModel):
    """Schema for the synthetic warehouse location data."""
    warehouse_id: Series[str] = pa.Field(nullable=False, unique=True)
    city: Series[str] = pa.Field(nullable=False)
    latitude: Series[float] = pa.Field(ge=-90, le=90)
    longitude: Series[float] = pa.Field(ge=-180, le=180)

    class Config:
        strict = True
        coerce = True

