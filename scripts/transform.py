from scripts.extract import get_data
import pandas as pd
from typing import List


def transform_data(data: List) -> pd.DataFrame:
    
    df = pd.json_normalize(data)

    COLUMNS = [  
        "symbol",         
        "current_price",  
        "total_volume",   
        "price_change_percentage_24h",  
        "market_cap",                   
        "market_cap_rank",              
        "high_24h",                     
        "low_24h"                       
    ]

    df = df[COLUMNS]
    columns_names = {
    "symbol": "symbol",
    "current_price": "price",
    "total_volume": "volume_24h",
    "price_change_percentage_24h": "change_24h",
    "market_cap": "market_cap",
    "market_cap_rank": "rank",
    "high_24h": "high_24h",
    "low_24h": "low_24h"
}
    df = df.rename(columns=columns_names)
    return df


def cleaning_data(df: pd.DataFrame) -> pd.DataFrame:
    
    df['symbol'] = df['symbol'].fillna('unknown')
    
    numeric_columns = df.select_dtypes(include='number').columns
    for c in numeric_columns:
        if c == 'market_cap' or c == 'rank':
            df[c] = df[c].fillna(0).astype('int64')
        else:
            df[c] = df[c].fillna(0.0)
    
    return df


if __name__ == "__main__":
    data = get_data()
    df = transform_data(data)
    df_test = cleaning_data(df)
    print(type(df_test))
    