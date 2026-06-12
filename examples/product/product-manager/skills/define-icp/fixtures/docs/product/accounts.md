# Account data — reconciliation product

Two account sets pulled for ICP derivation: best-fit (strong retention/expansion/health) and worst-fit
(churned or lost). Behavioural fields drawn from product telemetry.

## Best-fit accounts

| Account | Industry | Size (FTE) | Geo | Tech stack | Trigger to adopt | Week-1 activation | Usage pattern | Retention / NPS |
|---------|----------|-----------|-----|-----------|------------------|-------------------|---------------|-----------------|
| Northwind Logistics | Logistics | 220 | AU | Xero + Stripe | New finance hire overhauling process | Connected bank feed + invited 3 users in 2 days | Daily reconciliation, 5 active users | 3 yrs, NPS 9, expanded |
| Harbour Freight Co | Wholesale | 180 | AU | Xero + Shopify | Audit flagged manual errors | Connected feed day 1, 4 users week 1 | Weekly close, 4 users | 2 yrs, NPS 10, expanded |
| Meridian Trades | Construction | 140 | NZ | MYOB + Stripe | Scaling past spreadsheet capacity | Feed + 2 users in week 1 | Daily, 3 users | 2 yrs, NPS 8 |
| Coastal Distribution | Distribution | 260 | AU | Xero + Stripe | Replacing a churned competitor | Feed + 5 users in 3 days | Daily, 6 users | 18 mo, NPS 9, expanded |

Best-fit cluster: AU/NZ wholesale/logistics/distribution/construction, 140-260 FTE, on Xero/MYOB + a payments
stack, adopting on a concrete trigger (new hire, audit, scaling, competitor switch). Behaviourally: connected
a data source AND invited 2+ users within week one, then used it at least weekly.

## Worst-fit accounts (churned or lost)

| Account | Industry | Size (FTE) | Geo | Tech stack | Trigger to adopt | Week-1 activation | Usage pattern | Outcome |
|---------|----------|-----------|-----|-----------|------------------|-------------------|---------------|---------|
| Acme Consulting | Professional services | 200 | AU | QuickBooks only | "Exploring tools" (no concrete trigger) | Never connected a data source | Admin logged in twice, then dark | Churned at 60 days |
| Pixel Studio | Creative agency | 25 | UK | Spreadsheets | Curiosity | Connected feed but never invited anyone | Solo, sporadic | Churned at 90 days |
| Globex Retail | Retail | 230 | AU | Xero + Stripe | New hire | Only admin activated; no second user | Single user, weekly | Churned at 4 mo ("couldn't get team on") |
| Initech SMB | Software | 18 | US | Spreadsheets | Found us via ad | No bank feed; manual CSV once | Logged in 3 times | Lost / downgraded |

Worst-fit signals: no concrete adoption trigger ("exploring"/"curiosity"); right-sized right-vertical
accounts (Globex: 230 FTE AU retail on Xero+Stripe — looks like a best-fit firmographically) that still
churned because only the admin activated and no second user was invited. Very small agencies/solo (Pixel,
Initech) and QuickBooks-only / spreadsheet-only stacks under-fit. The decisive separator is behavioural:
best-fit accounts connected a data source AND invited a second user in week one; worst-fit did not — even
when the firmographics matched.
