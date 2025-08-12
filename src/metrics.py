from __future__ import annotations
import pandas as pd

def compute_basic_kpis(df: pd.DataFrame) -> dict:
    total_loads = int(len(df))
    gross_revenue = float(df['gross_revenue'].sum())
    gross_margin = float(df['gross_margin'].sum())
    margin_pct = float(gross_margin / gross_revenue) if gross_revenue else 0.0
    otp = float((df['on_time'] == 1).mean())
    return {
        "total_loads": total_loads,
        "gross_revenue": gross_revenue,
        "gross_margin": gross_margin,
        "margin_pct": margin_pct,
        "on_time_rate": otp,
    }

def lane_profitability(df: pd.DataFrame) -> pd.DataFrame:
    grp = (df.groupby('lane', as_index=False)
             .agg(loads=('load_id', 'count'),
                  revenue=('gross_revenue','sum'),
                  margin=('gross_margin','sum'),
                  margin_pct=('margin_pct','mean'),
                  otp=('on_time','mean')))
    grp = grp.sort_values('margin', ascending=False)
    return grp

def shipper_profitability(df: pd.DataFrame) -> pd.DataFrame:
    grp = (df.groupby('shipper_id', as_index=False)
             .agg(loads=('load_id', 'count'),
                  revenue=('gross_revenue','sum'),
                  margin=('gross_margin','sum'),
                  margin_pct=('margin_pct','mean'),
                  otp=('on_time','mean')))
    grp = grp.sort_values('margin', ascending=False)
    return grp
