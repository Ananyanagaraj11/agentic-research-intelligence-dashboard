from fastapi import APIRouter

from backend.app.agents.report_agent import generate_weekly_report
from backend.app.services.sample_data import (
    get_data_insights,
    get_entity_distribution,
    get_kpis,
    get_radar_metrics,
    get_trend_series,
)

router = APIRouter()


@router.get("/kpis")
def kpis():
    return get_kpis()


@router.get("/entity-distribution")
def entity_distribution():
    return get_entity_distribution()


@router.get("/radar-metrics")
def radar_metrics():
    return get_radar_metrics()


@router.get("/trend-series")
def trend_series():
    return get_trend_series()


@router.get("/insights")
def insights():
    return get_data_insights()


@router.get("/weekly-report")
def weekly_report():
    kpis = get_kpis()
    trends = get_trend_series()
    return generate_weekly_report(kpis, trends)
