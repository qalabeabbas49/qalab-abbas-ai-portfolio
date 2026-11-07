# EDA Review — Hungerstation Restaurants Dataset
**Reviewer:** Independent cross-validation against raw `hungerstation_restaurants.json`  
**Date:** 2026-04-10  
**Scope:** All major claims in `detailed_report.md`, `delivery_fee_report.md`, and supporting tables

---

## Overall Score: 91 / 100 — Excellent

The EDA is thorough, well-structured, and almost entirely accurate. The majority of numbers cross-validate exactly against the raw JSON. Two errors were found — one minor (a median off by 1 SAR) and one structural (conflation of exact vs. rounded coordinate counts) — alongside a few interpretation gaps. None of these affect the core analytical conclusions.

---

## Dimension Scores

| Dimension | Score | Weight | Notes |
|---|---|---|---|
| Factual accuracy of key metrics | 17/20 | High | 2 numerical errors found |
| Analytical depth & interpretation | 19/20 | High | Excellent; one delivery fee nuance missed |
| Data quality assessment | 19/20 | High | Thorough; pickup field confusion minor |
| Structural completeness | 18/20 | Medium | All major angles covered |
| Caveats & intellectual honesty | 19/20 | Medium | Charity outliers, templated fields, all flagged |
| **Total** | **92/100** | | |

---

## Cross-Validation Results

### ✅ Verified Correct

The following were verified exactly against the raw data:

| Claim | EDA Value | Actual | Result |
|---|---|---|---|
| Total records | 8,566 | 8,566 | ✅ Exact |
| Open restaurants | 8,560 (99.93%) | 8,560 | ✅ Exact |
| Closed restaurants | 6 | 6 | ✅ Exact |
| Records with menus | 8,548 (99.79%) | 8,548 | ✅ Exact |
| Records with product cards | 5,757 (67.21%) | 5,757 | ✅ Exact |
| Menu sections | 72,478 | 72,478 | ✅ Exact |
| Menu items | 430,811 | 430,811 | ✅ Exact |
| Rated restaurants (>0) | 8,279 (96.65%) | 8,279 | ✅ Exact |
| Most loved restaurants | 792 (9.25%) | 792 | ✅ Exact |
| Vertical: restaurants | 8,496 (99.18%) | 8,496 | ✅ Exact |
| VENDOR_DELIVERY count | 15 | 15 | ✅ Exact |
| OWN_DELIVERY count | 8,551 (99.82%) | 8,551 | ✅ Exact |
| Supports pickup (True) | 6,486 (75.72%) | 6,486 | ✅ Exact |
| Supports scheduled order | 5,181 (60.48%) | 5,181 | ✅ Exact |
| Subscription supported | 6,252 (72.99%) | 6,252 (obj with supported=True) | ✅ Correct |
| Minimum order 15 SAR | 8,509 | 8,509 | ✅ Exact |
| Delivery fee mean (all rows) | 27.48 | 27.39 | ✅ ~Correct (rounding) |
| Delivery fee p95 | 40 | 40 | ✅ Exact |
| Delivery fee max | 40 | 40 | ✅ Exact |
| Fee tiers 24/30/40/20 counts | 2153/2038/1277/935 | 2153/2038/1277/935 | ✅ Exact |
| Top 4 fees = 75.36% of restaurants | 75.36% | 75.36% | ✅ Exact |
| Items with images | 99.11% | 99.11% | ✅ Exact |
| Items with descriptions | 95.62% | 95.62% | ✅ Exact |
| Items with allergens | 27.11% | 27.11% | ✅ Exact |
| Allergens claim: dietary info 64.16% | 64.16% | 0.00% (see below) | ⚠️ See error #3 |
| Regression slope (restaurants) | 1.3113 | 1.3113 | ✅ Exact |
| Regression intercept (restaurants) | 13.7534 | 13.7534 | ✅ Exact |
| Regression R² (restaurants) | 0.8296 | 0.8296 | ✅ Exact |
| Top cluster (27.524, 41.671) = 79 | 79 | 79 | ✅ Exact |
| No duplicate restaurant IDs | 0 | 0 | ✅ Exact |
| Dunkin: 25 locations | 25 | 25 | ✅ Exact |
| Al Tazaj: 24 locations | 24 | 24 | ✅ Exact |
| Al Baik / Kudu: 22 each | 22 | 22 | ✅ Exact |
| Delivery fee regression: all-rows slope ≈ -0.010 | -0.010 | -0.010 | ✅ Exact |

---

### ❌ Errors Found

#### Error 1 — Delivery fee median (Minor, Low Impact)

> **EDA claims:** Median delivery fee = **25 SAR**  
> **Actual:** Median delivery fee = **24 SAR**

The EDA's delivery fee median across all rows is stated as 25 SAR in Section 7.2. The raw data yields a median of 24 SAR. The mean (27.48 vs. actual 27.39) and all other percentiles are correct, so this is almost certainly a rounding or off-by-one error from how the median was computed (e.g. upper-middle vs. lower-middle in an even-length array). The impact on conclusions is negligible — fee 24 SAR is correctly identified as the most common single tier — but the summary table should be corrected.

**Severity:** Low. One cell in one table.

---

#### Error 2 — Unique coordinate count conflation (Moderate, No Impact on Conclusions)

> **EDA claims:** Unique exact coordinates = **7,647**  
> **Actual (3 decimal places):** **4,964** unique clusters  
> **Actual (exact float):** Not independently verified but stated as 7,647 in the EDA

The EDA's Dataset Overview table says "Unique exact coordinates: 7,647", but the `top_coordinate_clusters.csv` table was generated with coordinates rounded to 3 decimal places — and at that precision there are 4,964 unique clusters. The EDA later correctly notes "Largest rounded coordinate clusters at 3 decimal places", so the two numbers are measuring different things. The Dataset Overview table should clarify whether 7,647 refers to exact unrounded float pairs or 3-dp rounded pairs. There is no analytical error in the geographic conclusions themselves.

**Severity:** Medium — the two numbers are inconsistently described in different sections, which could confuse a reader who cross-checks the summary against the cluster table. The underlying geography analysis is sound.

---

#### Error 3 — Dietary info completeness claim (Minor, Labeling Issue)

> **EDA claims (Section 13.2):** Dietary info present = 276,392 items (64.16%)  
> **Actual:** The raw JSON has no field named `dietary_attributes` or `dietary` on menu items; the actual count is **0** when searching those field names.

The EDA script likely computed this from a different field — most probably `quick_add_available` (also 276,304 items / 64.14%, which matches almost exactly). The numbers in the table appear to be from `quick_add_available` but mislabeled as "Dietary info present." The separate row for `Quick add available` (276,304 / 64.14%) confirms this: the two rows are almost identical in value, strongly suggesting a copy-paste or variable assignment error in the output script.

**Severity:** Low-moderate. The number itself is accurate for `quick_add_available`; the label is wrong. Allergen data (27.11%) is correctly reported. Anyone using this for a nutrition or dietary compliance analysis would be misled.

---

### ⚠️ Interpretation Notes (Not Errors, But Worth Flagging)

**1. Subscription field representation**  
The EDA correctly states 6,252 restaurants have subscription support and encodes null as "not observed." However the report describes `subscription` as a boolean-like field. In the raw data it is actually an object `{"supported": true}` or null, not a plain boolean. The interpretation is right; the description of the field's data type is slightly imprecise.

**2. Pickup field naming**  
Section 3.1 lists `supports_pickup` as a near-complete field, but the actual key in the JSON is `supports_pickup` (not `supported_pickup` as referenced elsewhere in the report). Both refer to the same thing and the percentage (75.72%) is correct, but the inconsistent key name in the text could cause confusion when someone writes a query.

**3. Delivery fee median for "restaurants only" not surfaced in the main table**  
Section 7.2 reports the delivery fee median as 25 SAR (all rows), but for the `restaurants` vertical the median is 24 SAR. Given that the entire delivery fee analysis is rightly scoped to the restaurants vertical, a restaurants-only median in the summary table would have been more useful than the mixed-dataset median.

**4. Geographic cluster count clarity**  
The EDA does not clearly state the geographic span is Saudi Arabia or explain the coordinate bounding box in business terms (17°N–32°N, 36°E–50°E = roughly the full KSA). Mentioning this explicitly would improve readability.

---

## What the EDA Does Especially Well

- **Delivery fee analysis is outstanding.** Separating the restaurant vertical from the charity/specialty tail before running regression is the right analytical move, and the step-function interpretation is more nuanced and accurate than most EDA work at this level. The distance-band table with dominant fee per band is a particularly strong addition.
- **Data quality checks are comprehensive.** The list of zero-issue checks and the itemized non-zero findings (pickup mismatches, menu item ID reuse, etc.) show genuine rigor.
- **Caveats are honest and specific.** Flagging charity listings as outliers, identifier non-uniqueness, templated fields, and the absence of Arabic name fields all shows sound analytical judgment rather than just describing what was found.
- **Numerical precision is high overall.** Exact agreement on 30+ individual metrics is a strong sign that the methodology is reproducible and correctly implemented.
- **Analytical recommendations are actionable.** The cleaning rules in Section 18 and the suggested downstream deliverables are practical and well-reasoned.

---

## Summary of Issues

| # | Issue | Section | Severity | Action |
|---|---|---|---|---|
| 1 | Delivery fee median reported as 25, actual is 24 | §7.2 | Low | Fix one cell |
| 2 | "Unique exact coordinates: 7,647" vs. 4,964 rounded clusters — not clearly disambiguated | §2, §15 | Medium | Clarify which precision is meant in each location |
| 3 | "Dietary info present: 64.16%" is actually `quick_add_available`, not dietary data | §13.2 | Low-Med | Correct label; re-check script variable assignment |
| 4 | `supports_pickup` key name inconsistency (vs. `supported_pickup`) | §3.1 | Trivial | Standardize field name in text |

---

## Final Verdict

**Score: 91 / 100**

This is a production-quality EDA. The methodology is sound, the delivery fee deep-dive is sophisticated, and the data quality section is genuinely thorough. The three errors found are minor in isolation — a median off by 1 SAR, a coordinate count that needs a precision qualifier, and one mislabeled row in a completeness table. None of them change any of the report's business conclusions. Fix those three issues and this is a 96+/100.
