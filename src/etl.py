from __future__ import annotations
import random
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
PROC = BASE / "data" / "processed"
FIGS = BASE / "reports" / "figures"

random.seed(42)
np.random.seed(42)

def random_date(start: datetime, end: datetime) -> datetime:
    delta = end - start
    return start + timedelta(seconds=int(random.random() * delta.total_seconds()))

def generate_synthetic(n_loads: int = 10000):
    states = ['TX','CA','IL','GA','FL','NY','PA','OH','NC','MI','IN','TN','NJ','VA','WA','AZ','MA','WI','CO','MN','MO','AL','SC','KY','OR']
    equipment_types = ['VAN','REEFER','FLATBED']
    start = datetime(2023,1,1)
    end = datetime(2025,7,31)

    n_shippers = 500
    n_carriers = 300

    # carrier quality (affects on_time)
    carrier_quality = {i: np.clip(np.random.normal(0.9, 0.05), 0.7, 0.99) for i in range(1, n_carriers+1)}

    rows = []
    for load_id in range(1, n_loads+1):
        shipper_id = random.randint(1, n_shippers)
        carrier_id = random.randint(1, n_carriers)
        equip = random.choice(equipment_types)
        pickup_state = random.choice(states)
        dest_state = random.choice(states)
        while dest_state == pickup_state:
            dest_state = random.choice(states)

        # miles
        miles = max(50, int(np.random.gamma(5, 120)))  # skewed, realistic 100-1500+
        # RPM by equipment
        rpm_base = {'VAN': 1.9, 'REEFER': 2.2, 'FLATBED': 2.1}[equip]
        rpm = max(1.2, np.random.normal(rpm_base, 0.35))
        linehaul = round(miles * rpm, 2)

        fuel = round(max(0, np.random.normal(80, 40)), 2)

        # detention hours and accessorials
        det_hours = max(0.0, np.random.normal(0.6, 0.8))
        det_rate = 50.0
        lumper = max(0, np.random.normal(30, 25))
        tonu = 0 if random.random() > 0.03 else max(50, np.random.normal(150, 50))
        accessorials = round(det_hours * det_rate + lumper + tonu, 2)

        gross_revenue = round(linehaul + fuel + accessorials, 2)

        # carrier cost ~ 78% to 92% of revenue with noise
        cost_pct = np.clip(np.random.normal(0.84, 0.05), 0.72, 0.95)
        carrier_cost = round(gross_revenue * cost_pct, 2)

        gross_margin = round(gross_revenue - carrier_cost, 2)
        margin_pct = round(gross_margin / gross_revenue if gross_revenue else 0.0, 4)

        # dates
        pu = random_date(start, end)
        # transit time scaled by miles
        days = max(1, int(np.random.normal(miles/600, 0.7)))
        deliv = pu + timedelta(days=days)

        # on_time depends on carrier quality and detention
        base_otp = carrier_quality[carrier_id]
        otp_noise = np.random.normal(0, 0.06)
        on_time_prob = np.clip(base_otp - (det_hours * 0.03) + otp_noise, 0.5, 0.99)
        on_time = 1 if random.random() < on_time_prob else 0

        rows.append({
            "load_id": load_id,
            "shipper_id": shipper_id,
            "carrier_id": carrier_id,
            "equipment": equip,
            "pickup_state": pickup_state,
            "dest_state": dest_state,
            "lane": f"{pickup_state}->{dest_state}",
            "miles": miles,
            "linehaul_revenue": linehaul,
            "fuel_surcharge": fuel,
            "accessorials": accessorials,
            "carrier_cost": carrier_cost,
            "gross_revenue": gross_revenue,
            "gross_margin": gross_margin,
            "margin_pct": margin_pct,
            "detention_hours": round(det_hours,2),
            "on_time": on_time,
            "pickup_date": pu.date().isoformat(),
            "delivery_date": deliv.date().isoformat(),
        })

    df = pd.DataFrame(rows)
    return df

def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df['pickup_date'] = pd.to_datetime(df['pickup_date'])
    df['delivery_date'] = pd.to_datetime(df['delivery_date'])
    df['pu_month'] = df['pickup_date'].dt.to_period('M').astype(str)
    df['lane_length'] = pd.cut(
        df['miles'],
        bins=[0,250,500,1000,2000,100000],
        labels=['0-250','251-500','501-1000','1001-2000','2000+'],
        include_lowest=True
    )
    return df

def save_plots(df: pd.DataFrame):
    # 1) Top shippers by total margin
    top_ship = (df.groupby('shipper_id')['gross_margin'].sum()
                  .sort_values(ascending=False).head(15))
    ax = top_ship.plot(kind='bar', title='Top 15 Shippers by Total Margin')
    ax.set_xlabel('Shipper ID'); ax.set_ylabel('Total Margin ($)')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGS / "top_shippers_margin.png")
    plt.close(fig)

    # 2) Lane profitability (avg margin % by lane)
    lane = (df.groupby('lane')['margin_pct'].mean()
              .sort_values(ascending=False).head(20))
    ax = lane.plot(kind='bar', title='Top 20 Lanes by Avg Margin %')
    ax.set_xlabel('Lane'); ax.set_ylabel('Avg Margin %')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGS / "top_lanes_margin_pct.png")
    plt.close(fig)

    # 3) Margin % vs On-Time scatter (sample 3000 for speed)
    s = df.sample(min(3000, len(df)), random_state=42)
    ax = s.plot(kind='scatter', x='on_time', y='margin_pct', title='Margin % vs On-Time (0/1)')
    fig = ax.get_figure()
    fig.tight_layout()
    fig.savefig(FIGS / "scatter_margin_vs_otp.png")
    plt.close(fig)

def main():
    raw_path = RAW / "loads.csv"
    clean_path = PROC / "loads_clean.csv"

    print("Generating synthetic loads...")
    df = generate_synthetic(n_loads=10000)
    df.to_csv(raw_path, index=False)
    print("Saved raw:", raw_path)

    print("Enriching and cleaning...")
    df = enrich(df)
    df.to_csv(clean_path, index=False)
    print("Saved clean:", clean_path)

    print("Saving example charts to reports/figures ...")
    save_plots(df)
    print("Done.")

if __name__ == "__main__":
    main()
