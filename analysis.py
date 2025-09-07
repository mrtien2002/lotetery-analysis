import pandas as pd

def explode_raw_daily_lo2d(raw_df: pd.DataFrame):
    rows = []
    for _, row in raw_df.iterrows():
        for i in range(1, 28):
            n = row.get(f'n{i}')
            if pd.notna(n):
                rows.append({'date': row['date'], 'number': int(n)})
    return pd.DataFrame(rows)

def make_full_calendar_counts(counts_df: pd.DataFrame, start_date, end_date):
    all_days = pd.date_range(start_date, end_date, freq='D')
    all_numbers = list(range(0, 100))
    idx = pd.MultiIndex.from_product([all_days, all_numbers], names=['date', 'number'])
    full = pd.DataFrame(index=idx).reset_index()
    merged = full.merge(counts_df.groupby(['date','number']).size().reset_index(name='count'),
                        on=['date','number'], how='left').fillna(0)
    return merged

def make_analysis_table(full_df: pd.DataFrame, target_date):
    subset = full_df[full_df['date'] <= pd.to_datetime(target_date)]
    recent = subset.groupby('number')['count'].sum().reset_index()
    recent = recent.sort_values('count', ascending=False)
    return recent
