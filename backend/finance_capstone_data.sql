DROP TABLE IF EXISTS investment_decisions CASCADE;
DROP TABLE IF EXISTS asset_risk_logs CASCADE;
DROP TABLE IF EXISTS market_indicators CASCADE;
DROP TABLE IF EXISTS portfolio_holdings CASCADE;
DROP TABLE IF EXISTS portfolios CASCADE;
CREATE TABLE portfolios (
            portfolio_id INTEGER PRIMARY KEY,
            portfolio_name TEXT,
            portfolio_manager TEXT,
            risk_category TEXT,
            total_value BIGINT,
            benchmark_index TEXT
        );
CREATE TABLE portfolio_holdings (
            holding_id INTEGER PRIMARY KEY,
            portfolio_id INTEGER,
            asset_name TEXT,
            asset_type TEXT,
            sector TEXT,
            allocation_percentage NUMERIC(6,2),
            market_value BIGINT,
            last_updated DATE
        );
CREATE TABLE asset_risk_logs (
            risk_id INTEGER PRIMARY KEY,
            asset_name TEXT,
            risk_type TEXT,
            risk_score INTEGER,
            risk_level TEXT,
            risk_description TEXT,
            assessment_date DATE,
            escalation_flag BOOLEAN
        );
CREATE TABLE market_indicators (
            indicator_id INTEGER PRIMARY KEY,
            indicator_name TEXT,
            region TEXT,
            indicator_value NUMERIC(6,2),
            measurement_date DATE,
            trend_direction TEXT
        );
CREATE TABLE investment_decisions (
            decision_id INTEGER PRIMARY KEY,
            portfolio_id INTEGER,
            asset_name TEXT,
            decision_type TEXT,
            decision_reason TEXT,
            risk_assessment_reference INTEGER,
            decision_date DATE,
            approval_status TEXT
        );
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (1, 'Global Growth Portfolio 1', 'David Chen', 'Moderate', 30301755, 'NASDAQ 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (2, 'Global Growth Portfolio 2', 'Emma Wilson', 'Moderate', 24907543, 'S&P 500');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (3, 'Global Growth Portfolio 3', 'David Chen', 'Moderate', 29388944, 'NASDAQ 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (4, 'Global Growth Portfolio 4', 'Daniel Kim', 'Low', 40897317, 'MSCI World');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (5, 'Global Growth Portfolio 5', 'Emma Wilson', 'Moderate', 23442540, 'FTSE 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (6, 'Global Growth Portfolio 6', 'Alice Morgan', 'Moderate', 47938413, 'NASDAQ 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (7, 'Global Growth Portfolio 7', 'David Chen', 'High', 39492391, 'NASDAQ 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (8, 'Global Growth Portfolio 8', 'Alice Morgan', 'Moderate', 45649568, 'MSCI World');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (9, 'Global Growth Portfolio 9', 'Alice Morgan', 'Moderate', 24499723, 'NASDAQ 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (10, 'Global Growth Portfolio 10', 'Emma Wilson', 'High', 24333844, 'MSCI World');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (11, 'Global Growth Portfolio 11', 'Alice Morgan', 'High', 23700832, 'S&P 500');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (12, 'Global Growth Portfolio 12', 'David Chen', 'High', 28666881, 'FTSE 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (13, 'Global Growth Portfolio 13', 'Alice Morgan', 'High', 49019905, 'MSCI World');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (14, 'Global Growth Portfolio 14', 'Sophia Martinez', 'High', 49757080, 'FTSE 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (15, 'Global Growth Portfolio 15', 'Daniel Kim', 'Moderate', 22042023, 'NASDAQ 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (16, 'Global Growth Portfolio 16', 'Emma Wilson', 'Moderate', 48271763, 'MSCI World');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (17, 'Global Growth Portfolio 17', 'Emma Wilson', 'High', 23375780, 'FTSE 100');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (18, 'Global Growth Portfolio 18', 'Daniel Kim', 'High', 7656792, 'S&P 500');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (19, 'Global Growth Portfolio 19', 'David Chen', 'Moderate', 6012950, 'MSCI World');
INSERT INTO portfolios 
(portfolio_id, portfolio_name, portfolio_manager, risk_category, total_value, benchmark_index)
VALUES (20, 'Global Growth Portfolio 20', 'David Chen', 'High', 12709125, 'S&P 500');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (1, 11, 'Amazon', 'ETF', 'Energy', 3.82, 1829339, '2024-04-19');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (2, 13, 'US Treasury Bonds', 'Equity', 'Consumer', 2.9, 1927810, '2024-05-18');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (3, 2, 'JPMorgan', 'Equity', 'Technology', 2.41, 3102680, '2024-09-05');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (4, 14, 'Google', 'Bond', 'Energy', 6.87, 4783931, '2024-01-28');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (5, 6, 'Microsoft', 'Bond', 'Technology', 11.89, 3726361, '2024-09-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (6, 6, 'Gold ETF', 'ETF', 'Energy', 22.82, 333133, '2024-08-26');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (7, 18, 'Google', 'Bond', 'Energy', 15.79, 1857538, '2024-11-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (8, 18, 'Amazon', 'Commodity', 'Healthcare', 11.9, 4654525, '2024-10-21');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (9, 11, 'Microsoft', 'Equity', 'Finance', 10.4, 303431, '2024-09-17');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (10, 12, 'Amazon', 'ETF', 'Energy', 18.62, 2885028, '2024-06-17');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (11, 20, 'Gold ETF', 'Commodity', 'Consumer', 12.66, 4039859, '2024-11-28');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (12, 12, 'Microsoft', 'Commodity', 'Consumer', 14.07, 2864526, '2025-01-27');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (13, 11, 'Microsoft', 'Bond', 'Healthcare', 16.95, 1320250, '2024-11-22');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (14, 17, 'Oil Futures', 'Equity', 'Finance', 13.3, 1678912, '2024-07-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (15, 6, 'Oil Futures', 'Bond', 'Technology', 11.57, 3893052, '2024-03-22');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (16, 6, 'Gold ETF', 'Equity', 'Consumer', 16.28, 3146499, '2024-12-12');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (17, 7, 'Apple Inc', 'ETF', 'Finance', 23.39, 1269133, '2024-01-11');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (18, 7, 'Nvidia', 'Bond', 'Technology', 7.14, 2935469, '2025-01-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (19, 6, 'Apple Inc', 'Equity', 'Consumer', 20.41, 4303544, '2024-10-16');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (20, 4, 'Amazon', 'ETF', 'Healthcare', 3.42, 3563886, '2024-01-24');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (21, 16, 'Google', 'Bond', 'Consumer', 19.11, 4262234, '2024-04-24');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (22, 10, 'Tesla', 'Bond', 'Consumer', 19.25, 207614, '2024-03-20');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (23, 13, 'Nvidia', 'Bond', 'Consumer', 5.83, 3984410, '2024-09-13');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (24, 4, 'Apple Inc', 'Commodity', 'Healthcare', 10.79, 4383647, '2024-01-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (25, 14, 'Oil Futures', 'Bond', 'Technology', 23.25, 3623337, '2024-10-01');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (26, 18, 'Google', 'Commodity', 'Consumer', 11.45, 2729452, '2024-02-01');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (27, 18, 'Gold ETF', 'Equity', 'Healthcare', 5.56, 2911634, '2024-01-16');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (28, 12, 'Nvidia', 'Commodity', 'Consumer', 17.02, 4173472, '2025-01-08');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (29, 11, 'Tesla', 'Equity', 'Finance', 3.99, 2457715, '2024-03-21');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (30, 14, 'Nvidia', 'Commodity', 'Consumer', 21.18, 2563146, '2024-03-30');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (31, 15, 'Tesla', 'Commodity', 'Healthcare', 11.51, 3557435, '2024-02-23');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (32, 14, 'Oil Futures', 'ETF', 'Consumer', 20.4, 1497051, '2024-05-25');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (33, 2, 'Tesla', 'Commodity', 'Technology', 5.31, 1350913, '2024-09-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (34, 7, 'Nvidia', 'Commodity', 'Healthcare', 22.35, 3835535, '2024-11-11');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (35, 17, 'Microsoft', 'ETF', 'Consumer', 1.35, 1357569, '2024-06-14');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (36, 9, 'Gold ETF', 'Commodity', 'Finance', 2.35, 2766375, '2024-05-11');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (37, 13, 'Amazon', 'Bond', 'Healthcare', 23.12, 4471733, '2025-01-02');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (38, 9, 'Nvidia', 'Equity', 'Energy', 7.81, 3894804, '2024-07-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (39, 14, 'JPMorgan', 'ETF', 'Technology', 21.0, 1066400, '2024-10-29');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (40, 9, 'JPMorgan', 'Commodity', 'Energy', 24.88, 1248504, '2024-02-02');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (41, 8, 'Oil Futures', 'Commodity', 'Consumer', 3.16, 307251, '2025-01-17');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (42, 16, 'JPMorgan', 'Commodity', 'Finance', 17.55, 2741903, '2024-03-29');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (43, 8, 'US Treasury Bonds', 'Commodity', 'Consumer', 19.56, 1845594, '2024-09-27');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (44, 19, 'Nvidia', 'Equity', 'Technology', 20.75, 4034419, '2024-04-07');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (45, 10, 'Google', 'Equity', 'Energy', 11.94, 293966, '2024-11-18');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (46, 9, 'Tesla', 'Equity', 'Healthcare', 6.52, 215681, '2024-01-08');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (47, 10, 'Amazon', 'Equity', 'Consumer', 23.55, 2451764, '2025-02-15');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (48, 13, 'Google', 'Bond', 'Healthcare', 22.44, 2827008, '2024-02-20');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (49, 1, 'Nvidia', 'Equity', 'Energy', 20.3, 235506, '2024-06-16');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (50, 4, 'Microsoft', 'Bond', 'Consumer', 22.04, 1219319, '2024-11-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (51, 15, 'Nvidia', 'ETF', 'Finance', 23.8, 2642440, '2024-04-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (52, 14, 'Gold ETF', 'ETF', 'Finance', 1.36, 75347, '2024-05-28');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (53, 15, 'Google', 'ETF', 'Consumer', 6.22, 4038475, '2024-09-19');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (54, 8, 'US Treasury Bonds', 'Commodity', 'Technology', 7.72, 4172514, '2025-02-01');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (55, 16, 'Microsoft', 'ETF', 'Energy', 23.08, 2786765, '2024-12-31');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (56, 4, 'JPMorgan', 'Commodity', 'Consumer', 9.24, 516523, '2024-11-26');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (57, 9, 'Google', 'Commodity', 'Technology', 7.63, 364791, '2025-02-07');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (58, 8, 'Tesla', 'Equity', 'Healthcare', 11.07, 882390, '2025-02-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (59, 14, 'Microsoft', 'Equity', 'Consumer', 15.52, 1873736, '2024-10-14');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (60, 10, 'Amazon', 'Equity', 'Consumer', 24.23, 3931199, '2025-01-31');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (61, 11, 'Amazon', 'Commodity', 'Finance', 9.33, 1270090, '2024-08-15');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (62, 20, 'Tesla', 'ETF', 'Technology', 5.1, 2535020, '2024-09-27');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (63, 15, 'Google', 'ETF', 'Finance', 2.7, 2123772, '2024-03-13');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (64, 3, 'US Treasury Bonds', 'Commodity', 'Energy', 2.14, 1726452, '2024-06-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (65, 4, 'Oil Futures', 'Equity', 'Technology', 24.1, 2328933, '2024-05-25');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (66, 18, 'Amazon', 'Bond', 'Energy', 2.89, 2336870, '2024-11-28');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (67, 1, 'Amazon', 'Equity', 'Technology', 23.92, 4846242, '2025-03-01');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (68, 7, 'Oil Futures', 'ETF', 'Consumer', 22.38, 3463975, '2025-01-12');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (69, 18, 'Nvidia', 'Equity', 'Consumer', 7.28, 2891753, '2024-09-08');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (70, 12, 'Gold ETF', 'Commodity', 'Healthcare', 24.55, 686101, '2024-09-09');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (71, 13, 'US Treasury Bonds', 'Equity', 'Healthcare', 16.17, 576577, '2024-06-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (72, 10, 'JPMorgan', 'Commodity', 'Healthcare', 23.63, 998004, '2025-01-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (73, 8, 'Tesla', 'Equity', 'Healthcare', 5.11, 4983580, '2024-05-29');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (74, 5, 'Tesla', 'ETF', 'Energy', 12.3, 3939958, '2024-02-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (75, 12, 'Tesla', 'Equity', 'Finance', 9.54, 1136242, '2024-12-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (76, 2, 'US Treasury Bonds', 'Commodity', 'Energy', 23.24, 4214085, '2024-06-11');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (77, 18, 'Microsoft', 'Equity', 'Technology', 22.46, 407278, '2024-01-11');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (78, 11, 'US Treasury Bonds', 'Bond', 'Finance', 4.09, 4936220, '2024-02-15');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (79, 1, 'Nvidia', 'Commodity', 'Consumer', 8.3, 2285632, '2024-01-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (80, 11, 'US Treasury Bonds', 'Equity', 'Technology', 16.06, 1227535, '2024-03-22');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (81, 18, 'Apple Inc', 'ETF', 'Consumer', 4.73, 1924288, '2024-01-23');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (82, 11, 'Amazon', 'ETF', 'Finance', 18.97, 4606156, '2024-02-13');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (83, 11, 'Nvidia', 'Commodity', 'Technology', 14.67, 247570, '2024-10-29');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (84, 14, 'Google', 'Equity', 'Finance', 2.8, 4790254, '2024-09-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (85, 8, 'Tesla', 'Commodity', 'Energy', 2.42, 2381357, '2024-11-25');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (86, 20, 'Google', 'Equity', 'Consumer', 5.2, 1583286, '2024-08-16');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (87, 11, 'Microsoft', 'Equity', 'Technology', 16.33, 3047276, '2024-01-24');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (88, 9, 'Gold ETF', 'Bond', 'Healthcare', 19.35, 2417583, '2024-06-30');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (89, 17, 'Nvidia', 'Commodity', 'Energy', 22.22, 3110441, '2024-01-25');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (90, 18, 'US Treasury Bonds', 'ETF', 'Consumer', 17.51, 1634506, '2024-07-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (91, 18, 'Tesla', 'Equity', 'Consumer', 18.13, 1287938, '2024-01-16');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (92, 2, 'Google', 'ETF', 'Healthcare', 19.06, 534071, '2024-04-18');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (93, 5, 'Gold ETF', 'Commodity', 'Technology', 2.46, 2608129, '2024-09-21');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (94, 12, 'JPMorgan', 'ETF', 'Finance', 11.58, 1926991, '2024-04-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (95, 14, 'JPMorgan', 'Commodity', 'Healthcare', 4.54, 3960006, '2024-02-25');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (96, 18, 'Amazon', 'Equity', 'Technology', 23.14, 3565142, '2025-01-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (97, 20, 'US Treasury Bonds', 'Equity', 'Technology', 5.65, 4829460, '2024-08-14');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (98, 15, 'Microsoft', 'Bond', 'Energy', 8.23, 629943, '2024-07-20');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (99, 8, 'Apple Inc', 'Bond', 'Healthcare', 5.56, 1482317, '2024-10-14');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (100, 9, 'Nvidia', 'Bond', 'Energy', 23.63, 4087067, '2024-03-30');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (101, 13, 'Gold ETF', 'Equity', 'Consumer', 22.86, 2955323, '2024-04-25');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (102, 11, 'JPMorgan', 'Equity', 'Technology', 13.49, 3939272, '2024-11-30');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (103, 12, 'Oil Futures', 'Bond', 'Finance', 3.15, 3753669, '2024-03-30');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (104, 17, 'Oil Futures', 'Commodity', 'Energy', 12.79, 1239091, '2024-09-29');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (105, 7, 'Apple Inc', 'Bond', 'Energy', 24.66, 1834573, '2025-02-27');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (106, 12, 'Microsoft', 'ETF', 'Energy', 12.53, 87128, '2025-01-23');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (107, 16, 'Google', 'Bond', 'Healthcare', 21.52, 143784, '2024-12-30');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (108, 14, 'Oil Futures', 'ETF', 'Energy', 15.81, 3428690, '2025-01-09');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (109, 4, 'Tesla', 'ETF', 'Healthcare', 20.93, 4407738, '2025-01-18');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (110, 1, 'Oil Futures', 'Commodity', 'Consumer', 19.54, 1643844, '2024-11-06');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (111, 14, 'JPMorgan', 'ETF', 'Consumer', 10.17, 139329, '2024-08-13');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (112, 9, 'Amazon', 'Equity', 'Consumer', 16.87, 995316, '2024-04-04');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (113, 16, 'US Treasury Bonds', 'ETF', 'Finance', 17.48, 786695, '2024-04-13');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (114, 1, 'Amazon', 'Commodity', 'Energy', 12.05, 4279143, '2024-08-10');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (115, 20, 'Nvidia', 'Commodity', 'Consumer', 13.93, 3259572, '2024-03-31');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (116, 9, 'US Treasury Bonds', 'Bond', 'Consumer', 3.52, 2125764, '2024-03-26');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (117, 7, 'Google', 'ETF', 'Finance', 6.31, 2198239, '2024-09-18');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (118, 3, 'Microsoft', 'ETF', 'Healthcare', 19.52, 2883652, '2024-05-22');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (119, 2, 'Gold ETF', 'Commodity', 'Healthcare', 20.82, 361249, '2024-01-14');
INSERT INTO portfolio_holdings 
(holding_id, portfolio_id, asset_name, asset_type, sector, allocation_percentage, market_value, last_updated)
VALUES (120, 11, 'Google', 'Equity', 'Energy', 20.18, 4143457, '2024-08-18');
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (1, 'US Treasury Bonds', 'Market Volatility', 31, 'Medium', 'Market Volatility identified for US Treasury Bonds due to market conditions.', '2024-04-05', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (2, 'Oil Futures', 'Liquidity Risk', 61, 'Medium', 'Liquidity Risk identified for Oil Futures due to market conditions.', '2024-12-28', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (3, 'JPMorgan', 'Regulatory Risk', 20, 'Low', 'Regulatory Risk identified for JPMorgan due to market conditions.', '2024-04-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (4, 'Amazon', 'Credit Risk', 56, 'Medium', 'Credit Risk identified for Amazon due to market conditions.', '2024-09-15', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (5, 'Microsoft', 'Liquidity Risk', 27, 'Low', 'Liquidity Risk identified for Microsoft due to market conditions.', '2024-06-28', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (6, 'Apple Inc', 'Credit Risk', 52, 'Medium', 'Credit Risk identified for Apple Inc due to market conditions.', '2025-01-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (7, 'US Treasury Bonds', 'Liquidity Risk', 3, 'Low', 'Liquidity Risk identified for US Treasury Bonds due to market conditions.', '2024-05-04', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (8, 'Gold ETF', 'Geopolitical Risk', 60, 'Medium', 'Geopolitical Risk identified for Gold ETF due to market conditions.', '2024-03-15', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (9, 'Oil Futures', 'Geopolitical Risk', 95, 'High', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-12-01', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (10, 'Nvidia', 'Market Volatility', 25, 'Low', 'Market Volatility identified for Nvidia due to market conditions.', '2024-10-02', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (11, 'Apple Inc', 'Regulatory Risk', 17, 'Low', 'Regulatory Risk identified for Apple Inc due to market conditions.', '2025-02-07', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (12, 'Microsoft', 'Credit Risk', 36, 'Medium', 'Credit Risk identified for Microsoft due to market conditions.', '2024-06-19', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (13, 'Oil Futures', 'Regulatory Risk', 67, 'Medium', 'Regulatory Risk identified for Oil Futures due to market conditions.', '2024-01-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (14, 'Tesla', 'Credit Risk', 60, 'Medium', 'Credit Risk identified for Tesla due to market conditions.', '2024-10-13', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (15, 'Nvidia', 'Regulatory Risk', 91, 'High', 'Regulatory Risk identified for Nvidia due to market conditions.', '2024-02-28', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (16, 'Tesla', 'Geopolitical Risk', 0, 'Low', 'Geopolitical Risk identified for Tesla due to market conditions.', '2024-11-05', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (17, 'Google', 'Geopolitical Risk', 71, 'High', 'Geopolitical Risk identified for Google due to market conditions.', '2024-12-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (18, 'Gold ETF', 'Market Volatility', 17, 'Low', 'Market Volatility identified for Gold ETF due to market conditions.', '2024-09-05', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (19, 'JPMorgan', 'Credit Risk', 1, 'Low', 'Credit Risk identified for JPMorgan due to market conditions.', '2024-10-21', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (20, 'Nvidia', 'Regulatory Risk', 11, 'Low', 'Regulatory Risk identified for Nvidia due to market conditions.', '2024-08-25', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (21, 'Google', 'Geopolitical Risk', 51, 'Medium', 'Geopolitical Risk identified for Google due to market conditions.', '2024-11-19', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (22, 'JPMorgan', 'Liquidity Risk', 88, 'High', 'Liquidity Risk identified for JPMorgan due to market conditions.', '2024-12-02', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (23, 'Microsoft', 'Market Volatility', 99, 'High', 'Market Volatility identified for Microsoft due to market conditions.', '2024-07-05', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (24, 'JPMorgan', 'Geopolitical Risk', 2, 'Low', 'Geopolitical Risk identified for JPMorgan due to market conditions.', '2024-07-19', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (25, 'Nvidia', 'Market Volatility', 21, 'Low', 'Market Volatility identified for Nvidia due to market conditions.', '2024-05-03', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (26, 'JPMorgan', 'Market Volatility', 74, 'High', 'Market Volatility identified for JPMorgan due to market conditions.', '2024-03-03', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (27, 'Gold ETF', 'Credit Risk', 2, 'Low', 'Credit Risk identified for Gold ETF due to market conditions.', '2025-01-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (28, 'Apple Inc', 'Regulatory Risk', 91, 'High', 'Regulatory Risk identified for Apple Inc due to market conditions.', '2025-02-11', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (29, 'JPMorgan', 'Regulatory Risk', 38, 'Medium', 'Regulatory Risk identified for JPMorgan due to market conditions.', '2024-11-26', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (30, 'Amazon', 'Liquidity Risk', 40, 'Medium', 'Liquidity Risk identified for Amazon due to market conditions.', '2024-07-16', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (31, 'Oil Futures', 'Regulatory Risk', 71, 'High', 'Regulatory Risk identified for Oil Futures due to market conditions.', '2024-03-02', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (32, 'Microsoft', 'Liquidity Risk', 46, 'Medium', 'Liquidity Risk identified for Microsoft due to market conditions.', '2024-02-08', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (33, 'US Treasury Bonds', 'Regulatory Risk', 59, 'Medium', 'Regulatory Risk identified for US Treasury Bonds due to market conditions.', '2024-03-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (34, 'Nvidia', 'Market Volatility', 95, 'High', 'Market Volatility identified for Nvidia due to market conditions.', '2024-07-20', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (35, 'Nvidia', 'Liquidity Risk', 17, 'Low', 'Liquidity Risk identified for Nvidia due to market conditions.', '2024-10-18', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (36, 'Amazon', 'Market Volatility', 59, 'Medium', 'Market Volatility identified for Amazon due to market conditions.', '2024-10-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (37, 'Oil Futures', 'Geopolitical Risk', 7, 'Low', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-05-20', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (38, 'Nvidia', 'Regulatory Risk', 94, 'High', 'Regulatory Risk identified for Nvidia due to market conditions.', '2024-01-21', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (39, 'Tesla', 'Credit Risk', 43, 'Medium', 'Credit Risk identified for Tesla due to market conditions.', '2024-06-25', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (40, 'Microsoft', 'Market Volatility', 30, 'Medium', 'Market Volatility identified for Microsoft due to market conditions.', '2024-09-05', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (41, 'Oil Futures', 'Regulatory Risk', 1, 'Low', 'Regulatory Risk identified for Oil Futures due to market conditions.', '2024-12-18', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (42, 'Apple Inc', 'Liquidity Risk', 27, 'Low', 'Liquidity Risk identified for Apple Inc due to market conditions.', '2025-02-08', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (43, 'Google', 'Market Volatility', 67, 'Medium', 'Market Volatility identified for Google due to market conditions.', '2024-05-06', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (44, 'Nvidia', 'Market Volatility', 73, 'High', 'Market Volatility identified for Nvidia due to market conditions.', '2024-09-05', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (45, 'JPMorgan', 'Geopolitical Risk', 87, 'High', 'Geopolitical Risk identified for JPMorgan due to market conditions.', '2024-11-18', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (46, 'Google', 'Market Volatility', 94, 'High', 'Market Volatility identified for Google due to market conditions.', '2025-02-07', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (47, 'Tesla', 'Regulatory Risk', 84, 'High', 'Regulatory Risk identified for Tesla due to market conditions.', '2024-10-23', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (48, 'JPMorgan', 'Credit Risk', 62, 'Medium', 'Credit Risk identified for JPMorgan due to market conditions.', '2024-04-12', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (49, 'Amazon', 'Market Volatility', 30, 'Medium', 'Market Volatility identified for Amazon due to market conditions.', '2024-11-08', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (50, 'Microsoft', 'Geopolitical Risk', 90, 'High', 'Geopolitical Risk identified for Microsoft due to market conditions.', '2025-02-28', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (51, 'Apple Inc', 'Geopolitical Risk', 44, 'Medium', 'Geopolitical Risk identified for Apple Inc due to market conditions.', '2024-11-07', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (52, 'Apple Inc', 'Regulatory Risk', 88, 'High', 'Regulatory Risk identified for Apple Inc due to market conditions.', '2024-12-31', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (53, 'Gold ETF', 'Regulatory Risk', 73, 'High', 'Regulatory Risk identified for Gold ETF due to market conditions.', '2024-09-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (54, 'Oil Futures', 'Market Volatility', 94, 'High', 'Market Volatility identified for Oil Futures due to market conditions.', '2024-11-04', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (55, 'Tesla', 'Liquidity Risk', 69, 'Medium', 'Liquidity Risk identified for Tesla due to market conditions.', '2024-06-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (56, 'Google', 'Market Volatility', 19, 'Low', 'Market Volatility identified for Google due to market conditions.', '2024-07-06', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (57, 'Gold ETF', 'Credit Risk', 30, 'Medium', 'Credit Risk identified for Gold ETF due to market conditions.', '2024-08-17', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (58, 'JPMorgan', 'Geopolitical Risk', 40, 'Medium', 'Geopolitical Risk identified for JPMorgan due to market conditions.', '2024-11-16', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (59, 'Google', 'Geopolitical Risk', 85, 'High', 'Geopolitical Risk identified for Google due to market conditions.', '2024-07-30', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (60, 'Gold ETF', 'Market Volatility', 29, 'Low', 'Market Volatility identified for Gold ETF due to market conditions.', '2024-07-21', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (61, 'Tesla', 'Market Volatility', 44, 'Medium', 'Market Volatility identified for Tesla due to market conditions.', '2024-07-11', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (62, 'Google', 'Market Volatility', 90, 'High', 'Market Volatility identified for Google due to market conditions.', '2024-05-21', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (63, 'Tesla', 'Liquidity Risk', 34, 'Medium', 'Liquidity Risk identified for Tesla due to market conditions.', '2024-06-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (64, 'Google', 'Market Volatility', 97, 'High', 'Market Volatility identified for Google due to market conditions.', '2024-03-29', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (65, 'Gold ETF', 'Liquidity Risk', 37, 'Medium', 'Liquidity Risk identified for Gold ETF due to market conditions.', '2024-07-21', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (66, 'Tesla', 'Geopolitical Risk', 75, 'High', 'Geopolitical Risk identified for Tesla due to market conditions.', '2024-07-31', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (67, 'Gold ETF', 'Regulatory Risk', 41, 'Medium', 'Regulatory Risk identified for Gold ETF due to market conditions.', '2024-01-26', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (68, 'US Treasury Bonds', 'Geopolitical Risk', 39, 'Medium', 'Geopolitical Risk identified for US Treasury Bonds due to market conditions.', '2024-03-17', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (69, 'Gold ETF', 'Market Volatility', 55, 'Medium', 'Market Volatility identified for Gold ETF due to market conditions.', '2024-02-29', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (70, 'Microsoft', 'Market Volatility', 12, 'Low', 'Market Volatility identified for Microsoft due to market conditions.', '2024-04-26', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (71, 'US Treasury Bonds', 'Credit Risk', 79, 'High', 'Credit Risk identified for US Treasury Bonds due to market conditions.', '2024-06-13', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (72, 'Nvidia', 'Regulatory Risk', 39, 'Medium', 'Regulatory Risk identified for Nvidia due to market conditions.', '2024-06-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (73, 'Apple Inc', 'Market Volatility', 36, 'Medium', 'Market Volatility identified for Apple Inc due to market conditions.', '2025-01-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (74, 'Nvidia', 'Regulatory Risk', 17, 'Low', 'Regulatory Risk identified for Nvidia due to market conditions.', '2024-10-10', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (75, 'JPMorgan', 'Regulatory Risk', 51, 'Medium', 'Regulatory Risk identified for JPMorgan due to market conditions.', '2024-09-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (76, 'US Treasury Bonds', 'Liquidity Risk', 21, 'Low', 'Liquidity Risk identified for US Treasury Bonds due to market conditions.', '2025-01-05', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (77, 'Apple Inc', 'Credit Risk', 54, 'Medium', 'Credit Risk identified for Apple Inc due to market conditions.', '2024-03-16', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (78, 'Nvidia', 'Geopolitical Risk', 55, 'Medium', 'Geopolitical Risk identified for Nvidia due to market conditions.', '2024-07-16', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (79, 'JPMorgan', 'Market Volatility', 14, 'Low', 'Market Volatility identified for JPMorgan due to market conditions.', '2025-01-26', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (80, 'US Treasury Bonds', 'Regulatory Risk', 0, 'Low', 'Regulatory Risk identified for US Treasury Bonds due to market conditions.', '2024-09-11', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (81, 'Oil Futures', 'Geopolitical Risk', 82, 'High', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-01-08', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (82, 'Amazon', 'Credit Risk', 48, 'Medium', 'Credit Risk identified for Amazon due to market conditions.', '2024-12-22', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (83, 'Amazon', 'Credit Risk', 27, 'Low', 'Credit Risk identified for Amazon due to market conditions.', '2024-12-10', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (84, 'Google', 'Liquidity Risk', 35, 'Medium', 'Liquidity Risk identified for Google due to market conditions.', '2024-05-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (85, 'Nvidia', 'Market Volatility', 45, 'Medium', 'Market Volatility identified for Nvidia due to market conditions.', '2025-01-08', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (86, 'US Treasury Bonds', 'Liquidity Risk', 37, 'Medium', 'Liquidity Risk identified for US Treasury Bonds due to market conditions.', '2024-06-19', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (87, 'Amazon', 'Market Volatility', 73, 'High', 'Market Volatility identified for Amazon due to market conditions.', '2024-04-29', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (88, 'Amazon', 'Liquidity Risk', 14, 'Low', 'Liquidity Risk identified for Amazon due to market conditions.', '2024-09-08', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (89, 'Tesla', 'Geopolitical Risk', 81, 'High', 'Geopolitical Risk identified for Tesla due to market conditions.', '2024-01-25', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (90, 'Amazon', 'Regulatory Risk', 34, 'Medium', 'Regulatory Risk identified for Amazon due to market conditions.', '2024-06-11', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (91, 'Tesla', 'Geopolitical Risk', 13, 'Low', 'Geopolitical Risk identified for Tesla due to market conditions.', '2024-12-18', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (92, 'Tesla', 'Liquidity Risk', 97, 'High', 'Liquidity Risk identified for Tesla due to market conditions.', '2024-06-28', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (93, 'Google', 'Market Volatility', 13, 'Low', 'Market Volatility identified for Google due to market conditions.', '2025-01-23', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (94, 'Oil Futures', 'Liquidity Risk', 68, 'Medium', 'Liquidity Risk identified for Oil Futures due to market conditions.', '2024-11-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (95, 'JPMorgan', 'Credit Risk', 54, 'Medium', 'Credit Risk identified for JPMorgan due to market conditions.', '2024-01-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (96, 'JPMorgan', 'Market Volatility', 86, 'High', 'Market Volatility identified for JPMorgan due to market conditions.', '2025-01-08', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (97, 'Google', 'Liquidity Risk', 14, 'Low', 'Liquidity Risk identified for Google due to market conditions.', '2024-03-08', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (98, 'Gold ETF', 'Credit Risk', 57, 'Medium', 'Credit Risk identified for Gold ETF due to market conditions.', '2025-02-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (99, 'JPMorgan', 'Geopolitical Risk', 79, 'High', 'Geopolitical Risk identified for JPMorgan due to market conditions.', '2024-05-21', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (100, 'Oil Futures', 'Market Volatility', 5, 'Low', 'Market Volatility identified for Oil Futures due to market conditions.', '2024-11-02', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (101, 'Oil Futures', 'Credit Risk', 89, 'High', 'Credit Risk identified for Oil Futures due to market conditions.', '2024-10-28', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (102, 'Microsoft', 'Regulatory Risk', 45, 'Medium', 'Regulatory Risk identified for Microsoft due to market conditions.', '2024-10-01', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (103, 'Oil Futures', 'Market Volatility', 27, 'Low', 'Market Volatility identified for Oil Futures due to market conditions.', '2024-07-02', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (104, 'Tesla', 'Geopolitical Risk', 30, 'Medium', 'Geopolitical Risk identified for Tesla due to market conditions.', '2025-01-09', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (105, 'Google', 'Regulatory Risk', 98, 'High', 'Regulatory Risk identified for Google due to market conditions.', '2025-01-06', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (106, 'JPMorgan', 'Geopolitical Risk', 87, 'High', 'Geopolitical Risk identified for JPMorgan due to market conditions.', '2024-09-30', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (107, 'Tesla', 'Geopolitical Risk', 77, 'High', 'Geopolitical Risk identified for Tesla due to market conditions.', '2024-11-21', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (108, 'Google', 'Geopolitical Risk', 23, 'Low', 'Geopolitical Risk identified for Google due to market conditions.', '2024-06-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (109, 'Gold ETF', 'Liquidity Risk', 73, 'High', 'Liquidity Risk identified for Gold ETF due to market conditions.', '2024-11-25', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (110, 'Nvidia', 'Market Volatility', 91, 'High', 'Market Volatility identified for Nvidia due to market conditions.', '2024-03-17', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (111, 'Google', 'Geopolitical Risk', 36, 'Medium', 'Geopolitical Risk identified for Google due to market conditions.', '2025-02-12', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (112, 'Tesla', 'Regulatory Risk', 98, 'High', 'Regulatory Risk identified for Tesla due to market conditions.', '2024-11-16', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (113, 'Apple Inc', 'Regulatory Risk', 68, 'Medium', 'Regulatory Risk identified for Apple Inc due to market conditions.', '2024-10-28', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (114, 'Nvidia', 'Geopolitical Risk', 60, 'Medium', 'Geopolitical Risk identified for Nvidia due to market conditions.', '2024-06-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (115, 'Google', 'Market Volatility', 86, 'High', 'Market Volatility identified for Google due to market conditions.', '2024-10-15', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (116, 'Oil Futures', 'Geopolitical Risk', 9, 'Low', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-06-17', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (117, 'Nvidia', 'Geopolitical Risk', 3, 'Low', 'Geopolitical Risk identified for Nvidia due to market conditions.', '2024-10-18', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (118, 'JPMorgan', 'Regulatory Risk', 45, 'Medium', 'Regulatory Risk identified for JPMorgan due to market conditions.', '2024-12-10', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (119, 'Google', 'Credit Risk', 64, 'Medium', 'Credit Risk identified for Google due to market conditions.', '2025-01-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (120, 'Amazon', 'Regulatory Risk', 41, 'Medium', 'Regulatory Risk identified for Amazon due to market conditions.', '2024-04-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (121, 'Gold ETF', 'Liquidity Risk', 99, 'High', 'Liquidity Risk identified for Gold ETF due to market conditions.', '2025-01-29', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (122, 'Microsoft', 'Liquidity Risk', 28, 'Low', 'Liquidity Risk identified for Microsoft due to market conditions.', '2024-09-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (123, 'Microsoft', 'Liquidity Risk', 99, 'High', 'Liquidity Risk identified for Microsoft due to market conditions.', '2025-02-24', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (124, 'Apple Inc', 'Geopolitical Risk', 80, 'High', 'Geopolitical Risk identified for Apple Inc due to market conditions.', '2024-01-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (125, 'US Treasury Bonds', 'Credit Risk', 51, 'Medium', 'Credit Risk identified for US Treasury Bonds due to market conditions.', '2025-02-28', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (126, 'Apple Inc', 'Geopolitical Risk', 35, 'Medium', 'Geopolitical Risk identified for Apple Inc due to market conditions.', '2024-02-29', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (127, 'Oil Futures', 'Geopolitical Risk', 59, 'Medium', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-09-07', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (128, 'Oil Futures', 'Market Volatility', 14, 'Low', 'Market Volatility identified for Oil Futures due to market conditions.', '2024-10-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (129, 'Nvidia', 'Liquidity Risk', 22, 'Low', 'Liquidity Risk identified for Nvidia due to market conditions.', '2024-06-02', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (130, 'Nvidia', 'Market Volatility', 39, 'Medium', 'Market Volatility identified for Nvidia due to market conditions.', '2024-09-16', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (131, 'Oil Futures', 'Geopolitical Risk', 55, 'Medium', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-08-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (132, 'Microsoft', 'Market Volatility', 43, 'Medium', 'Market Volatility identified for Microsoft due to market conditions.', '2024-01-26', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (133, 'Amazon', 'Liquidity Risk', 27, 'Low', 'Liquidity Risk identified for Amazon due to market conditions.', '2024-03-30', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (134, 'Nvidia', 'Credit Risk', 71, 'High', 'Credit Risk identified for Nvidia due to market conditions.', '2024-06-10', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (135, 'Nvidia', 'Regulatory Risk', 87, 'High', 'Regulatory Risk identified for Nvidia due to market conditions.', '2025-02-09', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (136, 'Google', 'Liquidity Risk', 19, 'Low', 'Liquidity Risk identified for Google due to market conditions.', '2024-11-27', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (137, 'Microsoft', 'Credit Risk', 48, 'Medium', 'Credit Risk identified for Microsoft due to market conditions.', '2024-06-23', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (138, 'Tesla', 'Geopolitical Risk', 14, 'Low', 'Geopolitical Risk identified for Tesla due to market conditions.', '2024-02-24', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (139, 'Tesla', 'Market Volatility', 29, 'Low', 'Market Volatility identified for Tesla due to market conditions.', '2024-10-07', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (140, 'JPMorgan', 'Regulatory Risk', 78, 'High', 'Regulatory Risk identified for JPMorgan due to market conditions.', '2025-02-02', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (141, 'Apple Inc', 'Credit Risk', 83, 'High', 'Credit Risk identified for Apple Inc due to market conditions.', '2025-01-22', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (142, 'Oil Futures', 'Regulatory Risk', 31, 'Medium', 'Regulatory Risk identified for Oil Futures due to market conditions.', '2024-11-22', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (143, 'Amazon', 'Market Volatility', 12, 'Low', 'Market Volatility identified for Amazon due to market conditions.', '2024-02-06', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (144, 'Microsoft', 'Liquidity Risk', 80, 'High', 'Liquidity Risk identified for Microsoft due to market conditions.', '2024-05-06', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (145, 'Microsoft', 'Regulatory Risk', 20, 'Low', 'Regulatory Risk identified for Microsoft due to market conditions.', '2024-07-17', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (146, 'Tesla', 'Liquidity Risk', 3, 'Low', 'Liquidity Risk identified for Tesla due to market conditions.', '2024-04-29', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (147, 'Nvidia', 'Liquidity Risk', 84, 'High', 'Liquidity Risk identified for Nvidia due to market conditions.', '2024-08-16', TRUE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (148, 'Google', 'Geopolitical Risk', 49, 'Medium', 'Geopolitical Risk identified for Google due to market conditions.', '2024-09-13', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (149, 'Apple Inc', 'Regulatory Risk', 13, 'Low', 'Regulatory Risk identified for Apple Inc due to market conditions.', '2025-02-07', FALSE);
INSERT INTO asset_risk_logs 
(risk_id, asset_name, risk_type, risk_score, risk_level, risk_description, assessment_date, escalation_flag)
VALUES (150, 'Oil Futures', 'Geopolitical Risk', 24, 'Low', 'Geopolitical Risk identified for Oil Futures due to market conditions.', '2024-10-26', FALSE);
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (1, 'Interest Rate', 'Asia', 4.91, '2024-03-10', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (2, 'Interest Rate', 'US', 9.45, '2024-02-09', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (3, 'Unemployment Rate', 'US', 4.67, '2024-05-30', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (4, 'Consumer Confidence Index', 'Global', 9.21, '2024-04-04', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (5, 'Inflation Rate', 'Europe', 4.67, '2024-06-01', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (6, 'Interest Rate', 'Global', 8.14, '2024-04-30', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (7, 'GDP Growth', 'Europe', 6.46, '2024-04-10', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (8, 'Inflation Rate', 'Global', 6.94, '2024-08-16', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (9, 'Consumer Confidence Index', 'Europe', 6.87, '2024-07-12', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (10, 'Inflation Rate', 'Global', 5.62, '2024-02-08', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (11, 'GDP Growth', 'Global', 8.81, '2024-01-04', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (12, 'Unemployment Rate', 'Europe', 4.34, '2025-01-28', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (13, 'Unemployment Rate', 'US', 6.48, '2024-04-23', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (14, 'GDP Growth', 'Europe', 6.85, '2024-08-21', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (15, 'Interest Rate', 'Global', 9.49, '2024-08-23', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (16, 'Unemployment Rate', 'Global', 1.16, '2024-10-13', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (17, 'GDP Growth', 'Asia', 7.14, '2025-01-09', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (18, 'Interest Rate', 'Global', 2.06, '2024-10-25', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (19, 'Interest Rate', 'Europe', 5.71, '2024-03-12', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (20, 'GDP Growth', 'Asia', 5.16, '2024-06-10', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (21, 'Unemployment Rate', 'US', 4.0, '2024-06-17', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (22, 'Unemployment Rate', 'US', 7.28, '2024-03-25', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (23, 'GDP Growth', 'Europe', 9.36, '2024-09-30', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (24, 'GDP Growth', 'Asia', 8.62, '2024-05-10', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (25, 'Consumer Confidence Index', 'Global', 9.02, '2024-12-15', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (26, 'Interest Rate', 'US', 7.63, '2024-12-26', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (27, 'Interest Rate', 'Asia', 9.61, '2024-11-18', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (28, 'Inflation Rate', 'Europe', 5.42, '2024-02-18', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (29, 'Inflation Rate', 'US', 8.66, '2024-01-14', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (30, 'Consumer Confidence Index', 'Asia', 1.53, '2024-10-23', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (31, 'GDP Growth', 'US', 6.16, '2024-07-04', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (32, 'Interest Rate', 'Global', 2.03, '2025-01-03', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (33, 'Consumer Confidence Index', 'US', 8.39, '2025-01-13', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (34, 'Inflation Rate', 'Global', 7.54, '2024-02-28', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (35, 'Interest Rate', 'Europe', 7.31, '2024-05-24', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (36, 'Unemployment Rate', 'Europe', 4.78, '2024-12-24', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (37, 'Consumer Confidence Index', 'Europe', 5.63, '2025-02-02', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (38, 'Unemployment Rate', 'Europe', 3.5, '2024-10-06', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (39, 'Inflation Rate', 'US', 5.35, '2024-05-13', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (40, 'Inflation Rate', 'Europe', 6.93, '2024-11-01', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (41, 'Consumer Confidence Index', 'Global', 8.12, '2024-07-04', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (42, 'Inflation Rate', 'Europe', 5.13, '2024-04-20', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (43, 'GDP Growth', 'Asia', 4.36, '2024-02-10', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (44, 'Inflation Rate', 'US', 9.2, '2024-05-14', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (45, 'GDP Growth', 'Global', 6.13, '2024-01-09', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (46, 'Interest Rate', 'Europe', 5.77, '2024-02-03', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (47, 'Consumer Confidence Index', 'Asia', 3.08, '2025-01-16', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (48, 'GDP Growth', 'Europe', 7.79, '2024-09-14', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (49, 'GDP Growth', 'US', 4.82, '2025-02-19', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (50, 'Unemployment Rate', 'Europe', 7.24, '2024-06-30', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (51, 'Interest Rate', 'US', 3.17, '2025-01-20', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (52, 'Inflation Rate', 'Asia', 1.76, '2025-01-12', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (53, 'Unemployment Rate', 'Global', 3.3, '2024-04-01', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (54, 'Interest Rate', 'Asia', 3.89, '2024-04-22', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (55, 'Unemployment Rate', 'Asia', 5.66, '2024-05-03', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (56, 'Consumer Confidence Index', 'Asia', 5.2, '2024-02-21', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (57, 'GDP Growth', 'Europe', 7.9, '2024-06-24', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (58, 'GDP Growth', 'Asia', 3.14, '2024-04-21', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (59, 'Inflation Rate', 'Global', 5.16, '2024-05-18', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (60, 'Interest Rate', 'Global', 5.13, '2024-01-18', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (61, 'Consumer Confidence Index', 'US', 4.01, '2025-02-20', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (62, 'Unemployment Rate', 'Global', 9.66, '2024-10-17', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (63, 'Inflation Rate', 'Asia', 9.82, '2024-07-12', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (64, 'Consumer Confidence Index', 'Europe', 2.95, '2024-07-18', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (65, 'GDP Growth', 'Global', 6.69, '2024-10-10', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (66, 'Inflation Rate', 'Global', 6.13, '2024-04-10', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (67, 'Unemployment Rate', 'US', 4.55, '2024-02-04', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (68, 'Consumer Confidence Index', 'Global', 8.82, '2024-09-14', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (69, 'Inflation Rate', 'Global', 6.57, '2024-07-15', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (70, 'Inflation Rate', 'Global', 5.47, '2024-06-15', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (71, 'GDP Growth', 'Europe', 3.86, '2024-08-02', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (72, 'Unemployment Rate', 'Asia', 6.94, '2024-10-31', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (73, 'GDP Growth', 'Global', 4.43, '2025-01-31', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (74, 'Interest Rate', 'Global', 4.16, '2024-02-26', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (75, 'Consumer Confidence Index', 'Global', 9.98, '2025-01-29', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (76, 'Inflation Rate', 'Europe', 3.58, '2024-04-02', 'Decreasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (77, 'Consumer Confidence Index', 'Global', 4.1, '2024-01-14', 'Stable');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (78, 'Interest Rate', 'Europe', 9.75, '2024-12-27', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (79, 'Consumer Confidence Index', 'Europe', 5.0, '2024-09-24', 'Increasing');
INSERT INTO market_indicators
(indicator_id, indicator_name, region, indicator_value, measurement_date, trend_direction)
VALUES (80, 'Interest Rate', 'Global', 2.37, '2024-11-03', 'Increasing');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (1, 13, 'Amazon', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 92, '2024-10-01', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (2, 15, 'JPMorgan', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 121, '2024-03-16', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (3, 14, 'Tesla', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 49, '2024-09-26', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (4, 16, 'US Treasury Bonds', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 54, '2024-09-20', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (5, 14, 'US Treasury Bonds', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 21, '2024-04-18', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (6, 14, 'Oil Futures', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 32, '2024-10-04', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (7, 12, 'Amazon', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 42, '2024-12-18', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (8, 15, 'Google', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 138, '2024-03-25', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (9, 10, 'Google', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 90, '2024-05-10', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (10, 14, 'Tesla', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 15, '2024-08-03', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (11, 13, 'Amazon', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 88, '2024-11-23', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (12, 20, 'Amazon', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 50, '2024-01-05', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (13, 9, 'Oil Futures', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 119, '2024-04-26', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (14, 12, 'Tesla', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 147, '2025-01-14', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (15, 14, 'Amazon', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 10, '2024-02-10', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (16, 12, 'Google', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 108, '2024-09-12', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (17, 8, 'Amazon', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 39, '2024-08-26', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (18, 5, 'Apple Inc', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 128, '2024-10-24', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (19, 7, 'Tesla', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 134, '2024-01-09', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (20, 5, 'US Treasury Bonds', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 79, '2024-02-03', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (21, 5, 'Amazon', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 77, '2024-03-07', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (22, 5, 'Nvidia', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 126, '2024-05-21', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (23, 18, 'JPMorgan', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 115, '2024-05-01', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (24, 12, 'JPMorgan', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 125, '2024-03-08', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (25, 10, 'Oil Futures', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 68, '2024-01-11', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (26, 14, 'Apple Inc', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 129, '2024-11-24', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (27, 6, 'JPMorgan', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 101, '2024-01-23', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (28, 7, 'Google', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 130, '2024-05-12', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (29, 9, 'JPMorgan', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 71, '2024-11-26', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (30, 8, 'Oil Futures', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 90, '2024-06-22', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (31, 12, 'Tesla', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 7, '2025-02-23', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (32, 8, 'Gold ETF', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 96, '2025-02-27', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (33, 17, 'Apple Inc', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 56, '2024-08-20', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (34, 2, 'Gold ETF', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 22, '2024-05-01', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (35, 2, 'Google', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 4, '2025-01-29', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (36, 12, 'Apple Inc', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 108, '2025-02-12', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (37, 17, 'Microsoft', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 6, '2025-01-15', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (38, 12, 'Oil Futures', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 94, '2024-08-10', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (39, 13, 'Oil Futures', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 149, '2024-07-29', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (40, 20, 'Microsoft', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 99, '2024-03-02', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (41, 8, 'Google', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 87, '2024-08-24', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (42, 20, 'JPMorgan', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 64, '2024-01-27', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (43, 20, 'Tesla', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 96, '2024-10-17', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (44, 14, 'Microsoft', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 44, '2024-08-29', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (45, 15, 'Amazon', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 38, '2024-07-04', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (46, 18, 'Google', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 2, '2024-03-22', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (47, 19, 'Amazon', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 144, '2024-01-28', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (48, 11, 'Tesla', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 76, '2024-01-31', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (49, 19, 'Tesla', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 22, '2025-02-02', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (50, 20, 'JPMorgan', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 38, '2024-10-16', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (51, 16, 'Gold ETF', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 35, '2024-01-27', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (52, 6, 'JPMorgan', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 132, '2024-02-12', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (53, 1, 'US Treasury Bonds', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 24, '2024-11-01', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (54, 5, 'Google', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 7, '2025-02-02', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (55, 19, 'US Treasury Bonds', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 105, '2024-06-04', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (56, 3, 'Oil Futures', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 118, '2024-04-13', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (57, 19, 'Nvidia', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 91, '2024-02-20', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (58, 2, 'Microsoft', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 32, '2025-01-08', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (59, 15, 'Tesla', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 12, '2024-12-29', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (60, 6, 'Oil Futures', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 115, '2024-04-07', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (61, 7, 'US Treasury Bonds', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 23, '2024-01-18', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (62, 11, 'Oil Futures', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 26, '2024-02-22', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (63, 2, 'Apple Inc', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 112, '2024-06-29', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (64, 19, 'Nvidia', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 94, '2024-01-27', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (65, 19, 'Oil Futures', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 70, '2024-10-07', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (66, 1, 'Google', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 122, '2024-03-19', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (67, 12, 'JPMorgan', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 32, '2024-10-10', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (68, 1, 'Gold ETF', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 96, '2024-06-14', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (69, 8, 'Oil Futures', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 69, '2024-07-10', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (70, 10, 'US Treasury Bonds', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 77, '2024-03-23', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (71, 4, 'Tesla', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 11, '2024-10-06', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (72, 18, 'Nvidia', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 92, '2024-09-27', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (73, 12, 'Google', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 101, '2024-06-21', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (74, 5, 'Microsoft', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 11, '2024-08-10', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (75, 20, 'JPMorgan', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 31, '2024-05-20', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (76, 8, 'JPMorgan', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 19, '2024-02-02', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (77, 14, 'Tesla', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 98, '2024-09-01', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (78, 15, 'Nvidia', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 122, '2024-02-11', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (79, 9, 'US Treasury Bonds', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 22, '2024-12-07', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (80, 8, 'Apple Inc', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 63, '2024-02-28', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (81, 3, 'Tesla', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 122, '2025-02-12', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (82, 12, 'Microsoft', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 40, '2024-12-21', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (83, 16, 'Microsoft', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 51, '2024-08-31', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (84, 16, 'Oil Futures', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 104, '2024-11-13', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (85, 11, 'Google', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 61, '2024-05-14', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (86, 10, 'Microsoft', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 4, '2024-04-21', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (87, 18, 'Oil Futures', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 109, '2025-01-12', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (88, 20, 'Google', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 9, '2024-07-02', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (89, 18, 'Nvidia', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 61, '2024-04-30', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (90, 13, 'Apple Inc', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 108, '2024-07-06', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (91, 1, 'JPMorgan', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 67, '2024-05-27', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (92, 8, 'Tesla', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 132, '2024-07-01', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (93, 9, 'Gold ETF', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 113, '2024-01-17', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (94, 11, 'Google', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 30, '2024-03-03', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (95, 19, 'Tesla', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 133, '2024-09-28', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (96, 12, 'JPMorgan', 'HOLD', 'Decision based on market trend and portfolio diversification strategy.', 84, '2024-01-27', 'Pending');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (97, 2, 'JPMorgan', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 146, '2024-01-28', 'Rejected');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (98, 12, 'Google', 'SELL', 'Decision based on market trend and portfolio diversification strategy.', 62, '2024-12-07', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (99, 7, 'Apple Inc', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 140, '2024-03-03', 'Approved');
INSERT INTO investment_decisions
(decision_id, portfolio_id, asset_name, decision_type, decision_reason, risk_assessment_reference, decision_date, approval_status)
VALUES (100, 16, 'US Treasury Bonds', 'BUY', 'Decision based on market trend and portfolio diversification strategy.', 62, '2024-10-19', 'Pending');
