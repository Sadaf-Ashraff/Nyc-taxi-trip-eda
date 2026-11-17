# Findings

Based on 22,699 trips from the 2017 NYC Yellow Taxi sample.

## Data quality

- No null values; 18 columns (3 object, 8 float, 7 int). The `Unnamed: 0` column is a leftover index and can be dropped.
- Pickup/dropoff timestamps are stored as strings and should be converted to datetime.
- `trip_distance` ranges 0 to 33.96 miles (mean about 2.9). Many trips have distance 0.
- `total_amount` ranges from -$120.30 to $1,200.29 (mean about $16.31). Negative values are mostly dispute / no-charge trips (`payment_type` 3 or 4).
- `passenger_count` includes 0; `RatecodeID` has a value of 99 (not in the data dictionary).
- The highest-total trips are not the longest trips: many are RatecodeID 5 (negotiated fare), often with distance 0 and a very short duration, so they are suspect.

## Business-relevant patterns

| Question | Result |
|---|---|
| Payment split | About 67% credit card, 32% cash, under 1% each for no charge and dispute |
| Tips by payment type | Cash tips recorded as $0, so only credit card tips are usable |
| Vendor effect | Vendor 2: 12,626 trips, vendor 1: 10,073. Mean total about $16.32 vs $16.30 |
| Passenger count vs tip (credit card) | Roughly flat: $2.61 to $2.83 |

## Variables for a predictive model

`trip_distance` and `fare_amount` are the strongest candidates. Caveat: if the target is `total_amount`, `fare_amount` is a component of it (leakage), so use it as a predictor only for `tip_amount`, or predict `fare_amount` from `trip_distance`, duration and location.

`VendorID` and `passenger_count` showed almost no relationship with amounts.
