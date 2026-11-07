# Hungerstation Restaurants EDA

- Generated at (UTC): 2026-04-10T03:35:54.122751+00:00
- Source file: `/Users/qq-nux/Downloads/hungerstation_restaurants.json`
- File size: 461,849,482 bytes

## Overview

| metric | value |
| --- | --- |
| Total records | 8566 |
| Unique chain names | 6459 |
| Unique chain IDs | 6850 |
| Unique brand IDs | 91 |
| Records with menus | 8548 (99.79%) |
| Records with products | 5757 (67.21%) |
| Menu sections | 72478 |
| Menu items | 430811 |
| Products | 18871 |
| Mean rating (rated only) | 4.1529 |
| Weighted rating (by rate count) | 4.2024 |

## Top-Level Schema Completeness

| field | present_count | null_count | empty_list_count | non_empty_count | observed_types |
| --- | --- | --- | --- | --- | --- |
| available_expedition_types | 8560 | 0 | 0 | 8560 | {"list": 8560} |
| average_rating | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| badge | 3860 | 0 | 0 | 3860 | {"dict": 3860} |
| brand_id | 8566 | 0 | 0 | 8566 | {"int": 8566} |
| chain_id | 8566 | 0 | 0 | 8566 | {"int": 8566} |
| chain_name | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| chain_type | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| cover_photo | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| delivery | 8566 | 0 | 0 | 8566 | {"dict": 8566} |
| distance | 8566 | 0 | 0 | 8566 | {"dict": 8566} |
| external_id | 8566 | 8560 | 0 | 6 | {"NoneType": 8560, "str": 6} |
| filtered_count | 8566 | 0 | 0 | 8566 | {"int": 8566} |
| id | 8566 | 0 | 0 | 8566 | {"int": 8566} |
| incentives | 8566 | 0 | 15 | 8551 | {"list": 8566} |
| is_favorable | 8566 | 0 | 0 | 8566 | {"bool": 8566} |
| is_favorite | 8566 | 0 | 0 | 8566 | {"bool": 8566} |
| is_most_loved | 8566 | 0 | 0 | 8566 | {"bool": 8566} |
| kitchens | 8566 | 0 | 4 | 8562 | {"list": 8566} |
| label | 8566 | 8560 | 0 | 6 | {"NoneType": 8560, "dict": 6} |
| location | 8566 | 0 | 0 | 8566 | {"dict": 8566} |
| logo | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| meta | 8566 | 0 | 0 | 8566 | {"dict": 8566} |
| minimum_order | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| price_range | 8509 | 0 | 0 | 8509 | {"dict": 8509} |
| products | 5757 | 0 | 0 | 5757 | {"list": 5757} |
| promotion | 8566 | 15 | 0 | 8551 | {"NoneType": 15, "dict": 8551} |
| promotions | 8566 | 0 | 15 | 8551 | {"list": 8566} |
| rate_count | 8566 | 0 | 0 | 8566 | {"int": 8566} |
| restaurant_menu | 8566 | 18 | 0 | 8548 | {"NoneType": 18, "dict": 8548} |
| status | 8566 | 0 | 0 | 8566 | {"str": 8566} |
| status_indicator | 8 | 0 | 0 | 8 | {"dict": 8} |
| subscription | 8566 | 2314 | 0 | 6252 | {"NoneType": 2314, "dict": 6252} |
| supports_pickup | 8566 | 0 | 0 | 8566 | {"bool": 8566} |
| supports_scheduled_order | 8566 | 0 | 0 | 8566 | {"bool": 8566} |
| tags | 2583 | 0 | 0 | 2583 | {"list": 2583} |
| time_estimation | 8566 | 0 | 0 | 8566 | {"dict": 8566} |
| vertical | 8566 | 0 | 0 | 8566 | {"str": 8566} |

## Restaurant-Level Numeric Summary

| field | count | missing | min | p25 | median | p75 | p95 | max | mean | stddev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| available_expedition_types_count | 8566 | 0 | 0.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 1.7559 | 0.4312 |
| average_rating | 8566 | 0 | 0.0 | 3.9 | 4.2 | 4.4 | 4.8 | 5.0 | 4.0137 | 0.9079 |
| delivery_fee | 8566 | 0 | 0.0 | 22.0 | 24.0 | 30.0 | 40.0 | 40.0 | 27.3885 | 7.0706 |
| delivery_original_fee | 8566 | 0 | 0.0 | 22.0 | 24.0 | 30.0 | 40.0 | 40.0 | 27.3885 | 7.0706 |
| distance_value | 8566 | 0 | 0.1 | 7.0 | 10.2 | 13.9 | 18.6 | 1328.8 | 12.2801 | 43.6363 |
| filtered_count | 8566 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| incentives_count | 8566 | 0 | 0.0 | 1.0 | 1.0 | 2.0 | 2.0 | 2.0 | 1.4596 | 0.5019 |
| kitchens_count | 8566 | 0 | 0.0 | 2.0 | 3.0 | 4.0 | 4.0 | 14.0 | 3.0619 | 1.093 |
| latitude | 8566 | 0 | 17.5619 | 21.592 | 24.1654 | 26.3601 | 28.4298 | 31.6808 | 24.109 | 2.8067 |
| longitude | 8566 | 0 | 36.4643 | 39.1535 | 39.5773 | 43.9191 | 47.2631 | 50.1312 | 41.1631 | 3.2571 |
| menu_item_count | 8566 | 0 | 0.0 | 25.0 | 42.0 | 66.0 | 117.0 | 575.0 | 50.2931 | 37.8563 |
| menu_section_count | 8566 | 0 | 0.0 | 6.0 | 8.0 | 11.0 | 16.0 | 38.0 | 8.4611 | 4.1402 |
| minimum_order | 8566 | 0 | 0.0 | 15.0 | 15.0 | 15.0 | 15.0 | 20.0 | 14.9982 | 0.7187 |
| price_range_rank | 8509 | 57 | 1.0 | 1.0 | 2.0 | 2.0 | 2.0 | 3.0 | 1.6256 | 0.5663 |
| price_range_total | 8509 | 57 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 0.0 |
| products_count | 8566 | 0 | 0.0 | 0.0 | 3.0 | 3.0 | 5.0 | 6.0 | 2.203 | 1.7657 |
| promotions_count | 8566 | 0 | 0.0 | 1.0 | 1.0 | 2.0 | 2.0 | 2.0 | 1.4596 | 0.5019 |
| rate_count | 8566 | 0 | 0.0 | 16.0 | 60.0 | 168.0 | 658.5 | 5531.0 | 161.0719 | 311.6608 |
| tags_count | 8566 | 0 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 | 2.0 | 0.306 | 0.4703 |
| time_max | 8566 | 0 | 1.5 | 45.0 | 50.0 | 55.0 | 70.0 | 80.0 | 49.5952 | 10.2157 |
| time_min | 8566 | 0 | 1.0 | 30.0 | 35.0 | 40.0 | 50.0 | 60.0 | 34.3272 | 9.5091 |
| time_window | 8566 | 0 | 0.5 | 15.0 | 15.0 | 15.0 | 20.0 | 20.0 | 15.268 | 1.3526 |

## Core Categorical Distributions

### Vertical

| value | count | pct_of_total |
| --- | --- | --- |
| restaurants | 8496 | 99.1828 |
| specialty_and_ethnic | 20 | 0.2335 |
| nuts_and_dried_fruits | 17 | 0.1985 |
| charity | 15 | 0.1751 |
| coffee_grinders | 10 | 0.1167 |
| bakery | 7 | 0.0817 |
| snacks_and_sweets | 1 | 0.0117 |

### Chain Type

| value | count | pct_of_total |
| --- | --- | --- |
| RESTAURANT | 8560 | 99.93 |
| DARKSTORE | 6 | 0.07 |

### Status

| value | count | pct_of_total |
| --- | --- | --- |
| OPEN | 8560 | 99.93 |
| CLOSE | 6 | 0.07 |

### Delivery Type

| value | count | pct_of_total |
| --- | --- | --- |
| OWN_DELIVERY | 8551 | 99.8249 |
| VENDOR_DELIVERY | 15 | 0.1751 |

### Delivery Fee Buckets

| value | count | pct_of_total |
| --- | --- | --- |
| > 10 | 8508 | 99.3229 |
| 5.01 - 10 | 43 | 0.502 |
| 0 | 15 | 0.1751 |

### Rating Buckets

| value | count | pct_of_total |
| --- | --- | --- |
| 4.0 - 4.49 | 4325 | 50.4903 |
| 4.5 - 5.0 | 2059 | 24.0369 |
| 3.0 - 3.99 | 1653 | 19.2972 |
| Unrated / zero reviews | 287 | 3.3505 |
| < 3.0 | 242 | 2.8251 |

### Top Kitchens

| value | count | pct_of_total |
| --- | --- | --- |
| Desserts | 3385 | 39.5167 |
| Fast Food | 2511 | 29.3136 |
| Arabic | 1899 | 22.169 |
| Coffee | 1647 | 19.2272 |
| Sandwich | 1570 | 18.3283 |
| Pastries | 1506 | 17.5811 |
| Grill | 1412 | 16.4838 |
| Saudi | 1275 | 14.8844 |
| Burgers | 1210 | 14.1256 |
| Breakfast | 1046 | 12.2111 |
| Bakery | 951 | 11.102 |
| Beverages | 891 | 10.4016 |
| American | 833 | 9.7245 |
| Shawarma | 775 | 9.0474 |
| Pizza | 767 | 8.954 |
| Seafood | 656 | 7.6582 |
| Juices | 455 | 5.3117 |
| Pasta | 330 | 3.8524 |
| Healthy | 328 | 3.8291 |
| Salads | 326 | 3.8057 |

### Expedition Type Combinations

| value | count | pct_of_total |
| --- | --- | --- |
| delivery | pickup | 6481 | 75.6596 |
| delivery | 2079 | 24.2704 |
| (empty) | 6 | 0.07 |

## Promotions And Incentives

| metric | value |
| --- | --- |
| Restaurants with promotions | 8551 |
| Total promotion records | 12503 |
| Restaurants with incentives | 8551 |
| Total incentive records | 12503 |
| Top-level primary promotion missing despite promotions list | 0 |
| Primary promotion not found inside promotions list | 0 |

### Top Promotion Names

| value | count | pct_of_total |
| --- | --- | --- |
| Free delivery (Spend 15 SAR) | 8509 | 99.3346 |
| 20% off on selected items | 2421 | 28.2629 |
| 30% off on selected items | 647 | 7.5531 |
| 25% off on selected items | 241 | 2.8134 |
| 50% off on selected items | 171 | 1.9963 |
| 35% off on selected items | 170 | 1.9846 |
| 40% off on selected items | 136 | 1.5877 |
| Free delivery (Spend 20 SAR) | 42 | 0.4903 |
| 20% Off Your Order (Spend 15 SAR) | 25 | 0.2919 |
| 45% off on selected items | 20 | 0.2335 |
| 15% off on selected items | 16 | 0.1868 |
| 20% Off Your Order (Spend 50 SAR) | 14 | 0.1634 |
| 60% off on selected items | 12 | 0.1401 |
| 39% off on selected items | 9 | 0.1051 |
| 10% off on selected items | 6 | 0.07 |
| 25% Off Your Order (Spend 15 SAR) | 6 | 0.07 |
| 25% Off Your Order (Spend 50 SAR) | 4 | 0.0467 |
| 35% Off Your Order (Spend 15 SAR) | 4 | 0.0467 |
| 30% Off Your Order (Spend 15 SAR) | 4 | 0.0467 |
| 15% Off Your Order (Spend 15 SAR) | 3 | 0.035 |

### Top Promotion Types

| value | count | pct_of_total |
| --- | --- | --- |
| FREE_DELIVERY | 8551 | 99.8249 |
| MENU_ITEM_DISCOUNT | 3860 | 45.0619 |
| ORDER_PERCENTAGE_CUTBACK | 87 | 1.0156 |
| FIXED_ORDER_CUTBACK | 5 | 0.0584 |

## Products

| metric | value |
| --- | --- |
| Restaurants with products | 5757 (67.21%) |
| Total products | 18871 |
| Products with promotions | 9873 (52.32%) |
| Products with badges | 18871 (100.00%) |
| Products with tags | 7444 (39.45%) |
| Products missing image | 54 (0.29%) |
| Products missing name | 0 (0.00%) |
| Products missing product_id | 15271 (80.92%) |

| field | count | zeros | min | p25 | median | p75 | p95 | max | mean | stddev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| product_price | 18871 | 0 | 1.0 | 18.0 | 30.0 | 49.0 | 140.0 | 619.0 | 44.7503 | 47.6483 |
| product_discounted_price | 9873 | 0 | 0.8 | 15.2 | 25.6 | 40.0 | 112.8 | 495.2 | 36.9279 | 38.1352 |
| product_discount_pct | 9873 | 0 | 5.0 | 20.0 | 20.0 | 20.0 | 35.0 | 65.0 | 22.7481 | 6.3754 |

### Top Product Sources

| value | count | pct_of_total |
| --- | --- | --- |
| best_seller | 11427 | 60.5532 |
| promotion | 7444 | 39.4468 |

### Top Product Names

| product_name | count |
| --- | --- |
| French Fries | 79 |
| Pepsi | 72 |
| Fries | 47 |
| Iced V60 | 43 |
| Chicken Fries | 42 |
| Gathering Box | 37 |
| Butter Chicken | 35 |
| Arabic Shawarma | 32 |
| Cookies | 32 |
| Vegetable Pizza | 30 |
| Chicken Burger | 29 |
| Vegetable Pizza - Small | 28 |
| Vegetable Mutabbak | 27 |
| Chicken Tikka Masala | 27 |
| Hummus | 27 |
| Unlimited Crunch | 26 |
| Chicken Pie | 24 |
| Chocolate Pudding | 24 |
| Ice V60 | 24 |
| Chicken Pasta | 22 |

## Restaurant Menus

| metric | value |
| --- | --- |
| Restaurants with menus | 8548 (99.79%) |
| Total menu sections | 72478 |
| Total menu items | 430811 |
| Menu items with quick add | 276304 (64.14%) |
| Menu items with descriptions | 411934 (95.62%) |
| Menu items with images | 426983 (99.11%) |
| Menu items with allergens | 116806 (27.11%) |
| Menu items with dietary_info | 276392 (64.16%) |
| Menu items with tags | 61180 (14.20%) |
| Menu items with mandatory choices | 1334 (0.31%) |

| field | count | zeros | min | p25 | median | p75 | p95 | max | mean | stddev |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| menu_section_count_per_restaurant | 8566 | 18 | 0.0 | 6.0 | 8.0 | 11.0 | 16.0 | 38.0 | 8.4611 | 4.1402 |
| menu_item_count_per_restaurant | 8566 | 18 | 0.0 | 25.0 | 42.0 | 66.0 | 117.0 | 575.0 | 50.2931 | 37.8563 |
| menu_items_per_section | 72478 | 9 | 0.0 | 3.0 | 4.0 | 7.0 | 16.0 | 185.0 | 5.944 | 5.6073 |
| menu_item_price | 430811 | 2329 | 0.0 | 11.0 | 20.0 | 36.0 | 105.0 | 7350.0 | 32.7324 | 51.1213 |
| menu_item_discounted_price | 430811 | 2329 | 0.0 | 11.0 | 20.0 | 35.0 | 99.0 | 7350.0 | 31.5958 | 48.2317 |
| menu_item_list_price | 430811 | 18 | 0.0 | 11.0 | 20.91 | 36.0 | 105.0 | 7350.0 | 32.9457 | 51.1373 |
| menu_item_discount_pct | 430811 | 393057 | 0.0 | 0.0 | 0.0 | 0.0 | 20.0 | 65.0 | 2.0475 | 6.9474 |
| menu_item_calories | 430811 | 154653 | 0.0 | 0.0 | 128.0 | 436.0 | 1250.0 | 45698.0 | 332.5892 | 674.3194 |

### Top Section Names

| section_name | count |
| --- | --- |
| Bestsellers | 7874 |
| Beverages | 2786 |
| Special discounts | 1985 |
| Desserts | 1821 |
| Top 3 Discounts 🔥 | 1611 |
| Sandwiches | 1427 |
| Sauces | 1351 |
| Drinks | 1276 |
| Appetizers | 1227 |
| Salads | 947 |
| Cold Beverages | 878 |
| Value Meals | 836 |
| Hot Beverages | 831 |
| Side Dishes | 751 |
| Pizza | 730 |
| Main Dishes | 675 |
| Side Orders | 637 |
| Boxes | 576 |
| Offers | 483 |
| Pasta | 483 |

### Top Menu Item Names

| item_name | count |
| --- | --- |
| Water | 3396 |
| Pepsi | 2840 |
| 7 Up | 1614 |
| French Fries | 1368 |
| Cappuccino | 1026 |
| Diet Pepsi | 902 |
| Hummus | 896 |
| Flat White | 880 |
| Espresso | 798 |
| Green Salad | 787 |
| Latte | 755 |
| Americano | 732 |
| Orange Juice | 731 |
| Hot Chocolate | 726 |
| Cortado | 717 |
| Spanish Latte | 657 |
| Chicken Burger | 624 |
| Fries | 595 |
| Vegetable Pizza | 579 |
| Garlic Sauce | 578 |

### Menu Item Types

| value | count | pct_of_total |
| --- | --- | --- |
| VARIATION | 375828 | 87.2373 |
| PRODUCT | 54983 | 12.7627 |

## Geography

| metric | value |
| --- | --- |
| Latitude min | 17.5619 |
| Latitude max | 31.680844 |
| Longitude min | 36.464348 |
| Longitude max | 50.131243 |
| Unique exact coordinates | 7647 |
| Duplicate exact-coordinate rows | 919 |

### Top Rounded Coordinate Clusters (3 dp)

| rounded_coordinate_3dp | restaurant_count | pct_of_restaurants |
| --- | --- | --- |
| 27.524,41.671 | 79 | 0.9223 |
| 21.592,39.167 | 71 | 0.8289 |
| 21.592,39.152 | 56 | 0.6537 |
| 24.589,46.670 | 30 | 0.3502 |
| 21.633,39.156 | 29 | 0.3385 |
| 21.620,39.216 | 25 | 0.2919 |
| 21.594,39.156 | 20 | 0.2335 |
| 24.488,39.649 | 19 | 0.2218 |
| 24.587,46.668 | 19 | 0.2218 |
| 21.632,39.156 | 18 | 0.2101 |
| 21.628,39.111 | 18 | 0.2101 |
| 21.593,39.149 | 18 | 0.2101 |
| 21.619,39.192 | 14 | 0.1634 |
| 28.400,36.530 | 14 | 0.1634 |
| 24.449,39.525 | 13 | 0.1518 |
| 24.427,39.597 | 13 | 0.1518 |
| 28.405,36.527 | 13 | 0.1518 |
| 21.573,39.129 | 12 | 0.1401 |
| 21.587,39.231 | 12 | 0.1401 |
| 24.488,39.709 | 12 | 0.1401 |

## Chain Highlights

### Top Chains By Location Count

| chain_name | restaurant_count | mean_rating_rated_only | total_rate_count |
| --- | --- | --- | --- |
| Dunkin | 25 | 4.032 | 4821 |
| Al Tazaj | 24 | 4.0625 | 33143 |
| Al Baik | 22 | 4.1864 | 26082 |
| Kudu | 22 | 3.9682 | 15655 |
| Herfy | 21 | 3.9 | 10118 |
| KFC | 21 | 3.6 | 20083 |
| Domino's Pizza | 20 | 4.14 | 2900 |
| Baskin Robbins | 19 | 4.2579 | 722 |
| KYAN | 18 | 4.3667 | 2053 |
| Shawarmer | 18 | 4.1167 | 10813 |
| Maestro Pizza | 16 | 4.1562 | 4014 |
| Hardee's | 15 | 3.8667 | 9734 |
| MAD Pizza | 15 | 4.2133 | 797 |
| Subway | 15 | 4.0933 | 4647 |
| Hashi Basha | 14 | 4.3071 | 6207 |
| Little Caesar's pizza | 14 | 4.4357 | 1435 |
| Pizza Hut | 14 | 3.9857 | 3245 |
| Starbucks | 14 | 4.2786 | 5446 |
| tivo sandwich | 14 | 3.7857 | 712 |
| Enabah | 13 | 4.3769 | 2496 |

### Most Reviewed Chains

| chain_name | restaurant_count | mean_rating_rated_only | total_rate_count |
| --- | --- | --- | --- |
| Al Tazaj | 24 | 4.0625 | 33143 |
| Al Baik | 22 | 4.1864 | 26082 |
| McDonald's KSA | 13 | 3.9154 | 20792 |
| KFC | 21 | 3.6 | 20083 |
| Deep Fries | 6 | 4.2333 | 19825 |
| Kudu | 22 | 3.9682 | 15655 |
| Shawerma Classic | 6 | 3.9 | 15165 |
| Namq Caffee | 8 | 4.1625 | 13804 |
| Al Romansiah | 12 | 4.45 | 13237 |
| McDonald's | 11 | 3.9818 | 12661 |
| Shawarmer | 18 | 4.1167 | 10813 |
| Modawar | 10 | 4.46 | 10766 |
| Herfy | 21 | 3.9 | 10118 |
| Hardee's | 15 | 3.8667 | 9734 |
| Shawayet Alkhaleej | 6 | 4.4 | 9112 |
| Shawaya House | 5 | 4.06 | 8415 |
| Wahmy Burger | 5 | 3.72 | 7533 |
| ASL ALBURGER | 8 | 4.2125 | 7001 |
| Zanjbeel | 2 | 4.0 | 6445 |
| Khaliat Khalid | 13 | 4.5385 | 6280 |

### Highest Rated Chains With At Least 5 Locations

| chain_name | restaurant_count | mean_rating_rated_only | total_rate_count |
| --- | --- | --- | --- |
| TOZEEN | 5 | 4.7 | 12 |
| Labkah | 9 | 4.6667 | 1965 |
| Kyok | 7 | 4.6571 | 891 |
| Ladorf | 6 | 4.6333 | 17 |
| Aseel Nabulsieh Kunafa | 7 | 4.6286 | 1366 |
| HINT | 6 | 4.6167 | 679 |
| OAKBERRY | 6 | 4.6167 | 800 |
| Hala sol | 8 | 4.6 | 807 |
| Tawa | 12 | 4.5917 | 912 |
| KANAF | 8 | 4.5875 | 3311 |
| Dawar Al Saada | 5 | 4.58 | 2286 |
| Kunafa Al Taweel | 5 | 4.58 | 215 |
| Qoutof and Hala | 5 | 4.58 | 116 |
| Zan sweet | 9 | 4.575 | 14 |
| Kottouf Sweets | 7 | 4.5714 | 113 |
| Badie | 10 | 4.57 | 1123 |
| Wind | 6 | 4.5667 | 881 |
| PocoDor | 10 | 4.56 | 884 |
| Sheera Lateen | 5 | 4.56 | 211 |
| Signature | 13 | 4.5462 | 4101 |

## Data Quality Checks

| check | count | pct_of_base |
| --- | --- | --- |
| duplicate_restaurant_ids | 0 | 0.0 |
| duplicate_external_ids | 0 | 0.0 |
| delivery_fee_gt_original_fee | 0 | 0.0 |
| time_min_gt_time_max | 0 | 0.0 |
| invalid_price_range_rank_total | 0 | 0.0 |
| rating_without_reviews | 0 | 0.0 |
| reviews_without_rating | 0 | 0.0 |
| promotion_count_mismatch_vs_incentives | 0 | 0.0 |
| missing_primary_promotion_despite_promotions | 0 | 0.0 |
| primary_promotion_not_found_in_promotions | 0 | 0.0 |
| scheduled_support_mismatch_top_vs_menu | 0 | 0.0 |
| pickup_support_mismatch_top_vs_menu | 22 | 0.2568 |
| status_open_but_menu_unavailable | 22 | 0.2568 |
| duplicate_exact_coordinates | 919 | 10.7285 |
| duplicate_product_ids | 664 | 3.5186 |
| duplicate_product_skus | 664 | 3.5186 |
| product_discounted_price_gt_price | 0 | 0.0 |
| product_discount_pct_without_discounted_price | 0 | 0.0 |
| duplicate_menu_item_ids | 55932 | 12.983 |
| menu_item_discounted_price_gt_list_price | 0 | 0.0 |
| menu_item_discount_pct_without_actual_discount | 0 | 0.0 |
| menu_item_price_gt_list_price | 1 | 0.0002 |

## Output Files

| file | description |
| --- | --- |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/reports/summary_report.md | Compact autogenerated EDA summary report. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/metadata/summary.json | Compact machine-readable summary. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/restaurants_flattened.csv | One row per restaurant with flattened restaurant and menu metadata. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_level_completeness.csv | Presence, null, and empty counts for every top-level field. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/numeric_summary.csv | Distribution summary for derived numeric restaurant features. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/categorical_counts.csv | Exhaustive categorical value counts for restaurant, promotion, product, and menu dimensions. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/data_quality_checks.csv | Duplicate and consistency checks. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/chain_summary.csv | Chain-level rollup metrics. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_coordinate_clusters.csv | Top rounded geographic clusters. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_restaurants_by_menu_items.csv | Restaurants with the largest menus. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_restaurants_by_products.csv | Restaurants with the most product cards. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_restaurants_by_rate_count.csv | Most-reviewed restaurants. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_menu_section_names.csv | Most common menu section names. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_menu_item_names.csv | Most repeated menu item names. |
| /Users/qq-nux/Documents/GitHub/Data-Analyst-Portfolio/analysis/hungerstation/tables/top_product_names.csv | Most repeated product names. |
