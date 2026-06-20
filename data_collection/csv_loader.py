# ai_investment_dss/data_collection/csv_loader.py

import csv
from pathlib import Path
from datetime import datetime
from config.settings import RAW_MARKET_DIR

class CSVDataLoader:
    """Handles resilient loading, parsing, and data cleaning for historical PSX market assets."""
    
    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        self.file_path = RAW_MARKET_DIR / f"{self.ticker}.csv"
        
    def _clean_numeric_string(self, value: str) -> str:
        """Removes commas, spaces, and currency symbols from numeric fields safely."""
        if not value or value.strip() == "-":
            return "0"
        return value.replace(",", "").replace("Rs.", "").strip()

    def _parse_flexible_date(self, date_str: str) -> datetime.date:
        """Attempts to parse various common PSX historical date formats safely."""
        cleaned_date = date_str.strip()
        # Common date formats found across financial portals
        formats = ["%Y-%m-%d", "%d-%b-%y", "%d-%b-%Y", "%d/%m/%Y", "%m/%d/%Y"]
        
        for fmt in formats:
            try:
                return datetime.strptime(cleaned_date, fmt).date()
            except ValueError:
                continue
                
        raise ValueError(f"Unsupported date token configuration: '{date_str}'")

    def load_historical_data(self) -> list:
        """
        Reads local CSV files, automatically cleans formatting defects, handles missing 
        dividend headers defensively, and returns a chronologically sorted data array.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"[ERROR] Historical data file for ticker '{self.ticker}' missing at path: {self.file_path}"
            )
            
        cleaned_records = []
        
        with open(self.file_path, mode='r', encoding='utf-8-sig') as file: # utf-8-sig handles potential BOM markers
            reader = csv.DictReader(file)
            
            # Clean header spaces that occur during manual CSV exports
            headers = {h.strip() if h else "" for h in reader.fieldnames or []}
            
            # Core baseline structural check (Dividends made optional to support raw daily pricing sheets)
            absolute_minimum_headers = {"Date", "Open", "High", "Low", "Close", "Volume"}
            if not absolute_minimum_headers.issubset(headers):
                missing = absolute_minimum_headers - headers
                raise ValueError(f"[ERROR] Fatal structural omission in {self.ticker}.csv. Missing: {missing}")
            
            # Map clean, normalized lookups to handle uneven casing (e.g. 'volume' vs 'Volume')
            header_map = {h.lower().strip(): h for h in reader.fieldnames or []}
            
            for row_idx, row in enumerate(reader, start=1):
                try:
                    # Defensive parsing of the date index
                    raw_date = row[header_map["date"]]
                    parsed_date = self._parse_flexible_date(raw_date)
                    
                    # Clean numerical string formatting defects before casting types
                    raw_open = self._clean_numeric_string(row[header_map["open"]])
                    raw_high = self._clean_numeric_string(row[header_map["high"]])
                    raw_low = self._clean_numeric_string(row[header_map["low"]])
                    raw_close = self._clean_numeric_string(row[header_map["close"]])
                    raw_volume = self._clean_numeric_string(row[header_map["volume"]])
                    
                    # Dynamic check for dividend allocations if present in the source file
                    div_key = header_map.get("dividends_paid") or header_map.get("dividend")
                    if div_key and row[div_key]:
                        raw_div = self._clean_numeric_string(row[div_key])
                        parsed_div = float(raw_div)
                    else:
                        parsed_div = 0.0

                    record = {
                        "date": parsed_date,
                        "open": float(raw_open),
                        "high": float(raw_high),
                        "low": float(raw_low),
                        "close": float(raw_close),
                        "volume": int(raw_volume),
                        "dividends_paid": parsed_div
                    }
                    cleaned_records.append(record)
                    
                except Exception as e:
                    # Keeps your engine up and running even if a row has a severe data typo
                    print(f"[WARNING] Row processing skipped at sequence index {row_idx} for {self.ticker}: {e}")
                    continue
                    
        # Verify execution context array yields data
        if not cleaned_records:
            print(f"[WARNING] Ticker source for '{self.ticker}' yielded zero functional records.")
            
        # Chronological sorting alignment baseline
        cleaned_records.sort(key=lambda x: x["date"])
        return cleaned_records
