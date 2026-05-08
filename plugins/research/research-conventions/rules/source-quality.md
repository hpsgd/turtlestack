# Source quality framework

## Source tiers

Every source cited in research output must be classified by tier. The tier determines how much weight the evidence carries.

| Tier | Type | Examples | Trust level |
|---|---|---|---|
| T1 — Regulatory/Legal | Government bodies, regulators, court records | ACCC decisions, Auditor-General reports, procurement registers, company filings, AustLII | Highest — treat as factual |
| T2 — Independent Analysis | Analysts, journalists, industry publications | Gartner, IDC, iTnews, CRN, AFR, industry journals | High — professional editorial standards |
| T3 — Market Signal | Job boards, review sites, tech community, financial databases | SEEK/LinkedIn jobs, G2/Capterra reviews, StackOverflow, GitHub, Crunchbase | Moderate — useful signal, verify context |
| T4 — Customer/User Voice | End-user reviews, community forums, meeting minutes | App store reviews, local news, community groups, FOI responses | Moderate — genuine but potentially unrepresentative |
| T5 — Subject's Own Materials | Company website, press releases, marketing collateral, case studies | Corporate blog, branded case studies, investor presentations | Lowest — treat as claims to validate, not facts |

## Confidence rubric (0-4)

Confidence measures confidence in the assessment, not whether a finding is positive or negative. A high confidence score on a concern means you're very confident the concern is real.

This is the rubric the `confidence` field in the report-conventions frontmatter refers to.

| Rating | Label | Definition | Evidence standard |
|---|---|---|---|
| 0 | No confidence | Insufficient data to form a view | No reliable sources; contradictory signals |
| 1 | Low | Directional sense only. Gut feel territory | 1-2 indirect signals. Label as "gut feel" |
| 2 | Moderate | Reasonable view with gaps | 3+ corroborating sources from 2+ tiers. At least 1 T1-T3 source |
| 3 | High | Would confidently present to a board | Multiple validated T1-T3 sources. Disconfirming search attempted |
| 4 | Very high | Near-certain, cross-validated | Extensive T1-T2 anchored validation. Withstands board-level scrutiny |

T5-only sourcing caps confidence at 1 regardless of how compelling the claim sounds.

## Validation rules

1. **No claim at confidence 2+ without a T1-T3 source.** Subject-only sourcing (T5) caps confidence at 1.
1. **Triangulate.** Any claim in the final output should be supported by at least 2 sources from different tiers. One-source claims must be labelled `[single source]`.
1. **Challenge every superlative.** "Market-leading", "only company that...", "end-to-end" — these are marketing language. Find independent evidence or downgrade to hedged language ("claims to be...").
1. **Seek disconfirming evidence.** For every positive claim, actively search for contradicting data. Note failed searches ("searched for X, found no contradicting evidence").
1. **Tag source tier.** Every citation gets a tier tag so source quality is visible at a glance.
1. **Recency matters.** Prefer sources from the last 12 months. Flag anything older than 24 months as potentially stale.

## Source tier classification pitfalls

| Looks like | Actually is | Example |
|---|---|---|
| T2 (independent) | T5 (self-published) | Industry directories where companies submit their own profiles |
| T1 (government) | T3 (commercial aggregator) | .com sites aggregating government data — trace back to actual government source for T1 |
| Strong negative signal | Self-selecting sample | ProductReview.com.au, Trustpilot — people go there specifically to complain |
| Strong positive signal | Potentially incentivised | Very high app ratings — check for discount/reward programs for reviews |

## Claim validation checklist

Before finalising any research dimension:

- Are any findings supported only by T5 (subject's own) sources?
- Has at least one disconfirming search been attempted?
- Are superlatives backed by independent evidence?
- Does the source tier mix justify the confidence level?
- Are single-source claims labelled as such?
