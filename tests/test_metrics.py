import pandas as pd
from src.metrics import compute_basic_kpis

def test_basic_kpis():
    df = pd.DataFrame({
        'gross_revenue':[1000, 800],
        'gross_margin':[200, 160],
        'margin_pct':[0.2, 0.2],
        'on_time':[1, 0],
        'load_id':[1,2]
    })
    kpis = compute_basic_kpis(df)
    assert kpis['total_loads'] == 2
    assert round(kpis['gross_revenue'],2) == 1800
    assert round(kpis['gross_margin'],2) == 360
    assert round(kpis['margin_pct'],4) == round(360/1800,4)
    assert 0 <= kpis['on_time_rate'] <= 1
