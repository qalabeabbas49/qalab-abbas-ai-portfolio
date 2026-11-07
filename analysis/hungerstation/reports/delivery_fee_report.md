# Delivery Fee Deep Dive

- Generated at (UTC): 2026-04-10T03:36:03.251197+00:00
- Source file: `/Users/qq-nux/Downloads/hungerstation_restaurants.json`

## Validation Notes

| metric | value |
| --- | --- |
| total_rows | 8566 |
| restaurants_only_rows | 8496 |
| non_restaurant_rows | 70 |
| missing_location_rows | 0 |
| external_id_non_null_rows | 6 |
| external_id_null_rows | 8560 |
| has_name_ar_key_anywhere_top_level | False |
| has_query_lat_key_anywhere_top_level | False |
| has_query_lng_key_anywhere_top_level | False |
| unique_chain_ids | 6850 |
| unique_chain_names | 6459 |
| multi_branch_chain_ids | 689 |
| multi_branch_chain_names | 842 |

Key validation points:

- The raw payload does not contain `query_lat`, `query_lng`, or `name_ar` as top-level fields.
- `external_id` is mostly null, but not completely null: only 6 rows have a value.
- Delivery-fee modeling must distinguish `restaurants` from the small non-restaurant tail.

## Regression Summary

| scope | n | pearson_r | r_squared | slope | intercept | mae | rmse |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_rows | 8566 | -0.061425 | 0.003773 | -0.009953 | 27.510738 | 5.903059 | 7.057296 |
| restaurants_only | 8496 | 0.910808 | 0.82957 | 1.311257 | 13.753383 | 2.090582 | 2.874811 |
| non_restaurants | 70 | -0.816629 | 0.666883 | -0.019497 | 20.609785 | 3.512618 | 5.870342 |

Interpretation:

- On the full mixed dataset, distance and fee are not meaningfully related because non-restaurant rows introduce extreme long-distance, low-fee cases.
- On `restaurants_only`, the relationship is strong: `fee ≈ 1.311257 × distance_km + 13.753383`.
- The restaurant-only model is still an average relationship. Actual fees snap to discrete tiers rather than following a smooth continuous curve.

## Fee Tier Distribution

| fee_sar | restaurant_count | pct_of_restaurants | distance_median_km | distance_p75_km | distance_max_km |
| --- | --- | --- | --- | --- | --- |
| 9.0 | 9 | 0.1059 | 5.2 | 5.5 | 5.9 |
| 10.0 | 34 | 0.4002 | 1.15 | 1.575 | 2.0 |
| 11.0 | 21 | 0.2472 | 0.6 | 0.9 | 1.0 |
| 12.0 | 5 | 0.0589 | 2.3 | 2.4 | 3.0 |
| 13.0 | 28 | 0.3296 | 1.85 | 3.6 | 3.8 |
| 15.0 | 32 | 0.3766 | 2.4 | 2.8 | 4.6 |
| 16.0 | 1 | 0.0118 | 10.0 | 10.0 | 10.0 |
| 17.0 | 222 | 2.613 | 1.5 | 1.8 | 4.0 |
| 19.0 | 276 | 3.2486 | 3.4 | 3.6 | 4.0 |
| 20.0 | 935 | 11.0052 | 5.1 | 5.5 | 7.0 |
| 21.0 | 58 | 0.6827 | 5.15 | 5.6 | 6.0 |
| 22.0 | 473 | 5.5673 | 6.7 | 6.9 | 9.0 |
| 24.0 | 2153 | 25.3413 | 8.9 | 9.9 | 11.0 |
| 25.0 | 257 | 3.025 | 9.3 | 9.8 | 11.0 |
| 28.0 | 206 | 2.4247 | 10.6 | 11.375 | 12.0 |
| 30.0 | 2038 | 23.9878 | 13.0 | 14.2 | 15.0 |
| 35.0 | 471 | 5.5438 | 13.4 | 16.2 | 30.1 |
| 40.0 | 1277 | 15.0306 | 16.8 | 18.9 | 30.2 |

## Distance Bands

| distance_band_km | restaurant_count | fee_mean_sar | fee_median_sar | dominant_fee_sar | dominant_fee_share_pct | top_fee_mix |
| --- | --- | --- | --- | --- | --- | --- |
| 0-2 | 257 | 15.3619 | 17.0 | 17.0 | 72.7626 | 17:187, 10:33, 11:21, 13:16 |
| 2-5 | 787 | 19.1271 | 20.0 | 20.0 | 51.0801 | 20:402, 19:276, 17:35, 15:32, 21:21 |
| 5-10 | 3039 | 23.2382 | 24.0 | 24.0 | 54.1626 | 24:1646, 20:533, 22:473, 25:198, 30:91 |
| 10-15 | 2954 | 29.3744 | 30.0 | 30.0 | 65.2336 | 30:1927, 24:507, 35:257, 28:151, 25:59 |
| 15-20 | 1188 | 39.0488 | 40.0 | 40.0 | 82.6599 | 40:982, 35:186, 30:20 |
| 20-50 | 271 | 39.4834 | 40.0 | 40.0 | 89.6679 | 40:243, 35:28 |

## Formula Quality

| scope | within_2_sar_of_linear_prediction_pct | exact_match_to_nearest_fee_tier_pct | top_4_fee_tiers_share_pct |
| --- | --- | --- | --- |
| restaurants_only | 60.7462 | 41.4783 | 75.3649 |

## Conclusions

- Delivery fees behave like a stepped pricing ladder with strong distance dependence for real restaurant rows.
- The most important operating tiers are 20, 24, 30, 35, and 40 SAR, with 24 and 30 SAR dominating the middle-distance range.
- Short-range merchants cluster around 17 to 20 SAR, mid-range around 24 to 30 SAR, and long-range around 35 to 40 SAR.
- Any fee model should be built on `vertical='restaurants'` and ideally treated as a tiered classifier or step function, not just a linear regressor.
