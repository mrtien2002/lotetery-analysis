from datetime import date, timedelta
import pandas as pd
import numpy as np

def _normalize_two_digit(x):
    x = str(x).strip()
    if x == '' or x.lower() == 'nan':
        return None
    # Keep last two digits
    digits = ''.join(ch for ch in x if ch.isdigit())
    if digits == '':
        return None
    return f"{int(digits[-2:]):02d}"

def explode_raw_daily_lo2d(raw_df: pd.DataFrame) -> pd.DataFrame:
    """raw_df columns: date, n1..n27 (strings two-digit). Returns rows: date, number, count(=1 each), then groupby."""
    if 'date' not in raw_df.columns:
        return pd.DataFrame(columns=['date','number','count'])
    value_cols = [c for c in raw_df.columns if c != 'date']
    rows = []
    for _, r in raw_df.iterrows():
        d = pd.to_datetime(r['date']).date()
        for c in value_cols:
            val = _normalize_two_digit(r[c])
            if val is not None:
                rows.append((d, val))
    if not rows:
        return pd.DataFrame(columns=['date','number','count'])
    df = pd.DataFrame(rows, columns=['date','number'])
    df['count'] = 1
    # Aggregate duplicates within a day
    return df.groupby(['date','number'], as_index=False)['count'].sum()

def make_full_calendar_counts(daily_counts: pd.DataFrame, start_date: date, end_date: date) -> pd.DataFrame:
    """Ensure every date in range has all numbers 00..99 with count >=0 (0 if missing)."""
    all_nums = [f"{i:02d}" for i in range(100)]
    all_dates = pd.date_range(start_date, end_date, freq='D').date
    idx = pd.MultiIndex.from_product([all_dates, all_nums], names=['date','number'])
    base = pd.DataFrame(index=idx).reset_index()
    merged = base.merge(daily_counts, on=['date','number'], how='left')
    merged['count'] = merged['count'].fillna(0).astype(int)
    return merged

def compute_last_seen_gap(full_counts: pd.DataFrame, ref_date: date) -> pd.Series:
    """Return days since last seen for each number as of ref_date."""
    subset = full_counts[full_counts['date'] <= ref_date]
    last_seen = subset[subset['count'] > 0].groupby('number')['date'].max()
    gaps = {}
    for n in [f"{i:02d}" for i in range(100)]:
        last = last_seen.get(n, None)
        if last is None:
            gaps[n] = np.nan  # never seen in range
        else:
            gaps[n] = (pd.to_datetime(ref_date) - pd.to_datetime(last)).days
    return pd.Series(gaps, name='last_seen_days')

def window_freq(full_counts: pd.DataFrame, ref_date: date, days: int) -> pd.Series:
    start = ref_date - timedelta(days=days-1)
    win = full_counts[(full_counts['date'] >= start) & (full_counts['date'] <= ref_date)]
    freq = win.groupby('number')['count'].sum().reindex([f"{i:02d}" for i in range(100)], fill_value=0)
    return freq.rename(f'freq_{days}d')

def method1_score_current_month(full_counts: pd.DataFrame, ref_date: date) -> pd.Series:
    """Method 1 (approx): sum of gaps between consecutive appearances *within the current month* for each number."""
    start_month = ref_date.replace(day=1)
    month_df = full_counts[(full_counts['date'] >= start_month) & (full_counts['date'] <= ref_date)]
    scores = {}
    for n, grp in month_df[month_df['count'] > 0].groupby('number'):
        # list of dates it appeared this month
        dts = sorted(set(grp['date'].tolist()))
        if len(dts) <= 1:
            scores[n] = 0
        else:
            # sum day gaps between consecutive in-month appearances
            gaps = [(pd.to_datetime(dts[i]) - pd.to_datetime(dts[i-1])).days for i in range(1, len(dts))]
            scores[n] = int(sum(gaps))
    # numbers with no hits this month -> 0
    for n in [f"{i:02d}" for i in range(100)]:
        scores.setdefault(n, 0)
    return pd.Series(scores, name='method1_score_month')

def method2_points_and_group(full_counts: pd.DataFrame, ref_date: date):
    """Method 2: points = frequency in current month, group by thresholds (MAX>=9, TRUNG 5-8, MIN 0-4) as provided."""
    start_month = ref_date.replace(day=1)
    month_df = full_counts[(full_counts['date'] >= start_month) & (full_counts['date'] <= ref_date)]
    pts = month_df.groupby('number')['count'].sum().reindex([f"{i:02d}" for i in range(100)], fill_value=0)
    def to_group(x):
        if x >= 9: return 'MAX'
        if x >= 5: return 'TRUNG'
        return 'MIN'
    group = pts.apply(to_group).rename('group_method2')
    return pts.rename('method2_points'), group

def make_analysis_table(full_counts: pd.DataFrame, ref_date: date) -> pd.DataFrame:
    last_gap = compute_last_seen_gap(full_counts, ref_date)
    f30 = window_freq(full_counts, ref_date, 30)
    f60 = window_freq(full_counts, ref_date, 60)
    f90 = window_freq(full_counts, ref_date, 90)
    f300 = window_freq(full_counts, ref_date, 300)
    m1 = method1_score_current_month(full_counts, ref_date)
    m2_pts, m2_grp = method2_points_and_group(full_counts, ref_date)

    df = pd.concat([last_gap, f30, f60, f90, f300, m1, m2_pts, m2_grp], axis=1).reset_index()
    df = df.rename(columns={'index':'number'})
    # Khan rule (>=7 days since last seen)
    df['khan_ge7'] = df['last_seen_days'] >= 7
    # sort example: by group then freq_30 desc
    df = df.sort_values(by=['group_method2','freq_30d'], ascending=[True, False])
    return df
