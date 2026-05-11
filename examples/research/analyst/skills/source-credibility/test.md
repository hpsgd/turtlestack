# Test: source-credibility skill

Scenario: A journalist wants to assess whether the Australian Strategic Policy Institute (ASPI) is a reliable source to cite in a piece on defence procurement.

## Prompt

/analyst:source-credibility Australian Strategic Policy Institute (ASPI)

## Criteria

- [ ] PASS: Skill writes a file to disk at `<pwd>/source-credibility/<source-slug>.md` (see ARTIFACTS WRITTEN — at least one .md file under `source-credibility/` exists)
- [ ] PASS: The written file opens with YAML frontmatter (title, date, author=source-credibility, category=OSINT, subject, source_type) per report-conventions
- [ ] PASS: Chat response includes the absolute path to the written report (verbatim, copyable)
- [ ] PASS: Skill identifies the source type (think tank / research organisation) and applies the appropriate credibility framework
- [ ] PASS: Ownership and funding section covers who funds ASPI, transparency of disclosure, and any implications for systematic bias
- [ ] PASS: Editorial standards section assesses whether ASPI has a corrections policy, peer review, and named accountable authors
- [ ] PASS: Track record section draws on specific examples (corrections, retractions, or a strong reliability record) — not a generic statement
- [ ] PASS: Declared mission vs output pattern is assessed — does ASPI's stated purpose match what it publishes?
- [ ] PASS: Credibility assessment table is produced with ratings across ownership transparency, editorial accountability, accuracy track record, and bias transparency
- [ ] PASS: Output distinguishes between bias (systematic pattern) and error (specific inaccuracy) — treats them as separate dimensions
- [ ] PASS: "Appropriate use" section states what ASPI is and isn't reliable for — credibility is not treated as binary
- [ ] PASS: Skill does not assess whether ASPI's conclusions are correct — only whether the source is credible

## Output expectations

- [ ] PASS: Output identifies ASPI as a think tank / policy research institute (not a peer-reviewed academic journal, not a journalist publication, not a government body) and applies the think-tank credibility framework
- [ ] PASS: Output's ownership and funding section names ASPI's funding sources transparently — Australian Department of Defence (founding sponsor), foreign government grants (US State Department, UK FCDO), corporate donors (defence industry primes including Lockheed Martin, BAE, Northrop Grumman) — with the disclosure source cited
- [ ] PASS: Output addresses the systematic-bias implication of defence-industry funding — does NOT conclude ASPI is "biased therefore unreliable" but does flag that defence-procurement-favourable conclusions warrant cross-check, while non-defence research is less likely to be commercially conflicted
- [ ] PASS: Output's editorial standards section assesses — corrections policy (what's published when ASPI gets something wrong?), peer review (do reports go through external review?), named accountable authors (yes, typically named with credentials)
- [ ] PASS: Output's track record draws on specific examples — well-known reports / specific corrections / past controversies (e.g. ASPI's reporting on Xinjiang detention has been both lauded for breaking the story AND criticised for methodology by some academics) — both views presented
- [ ] PASS: Output's mission-vs-output assessment compares ASPI's stated mission ("contribute to nation's security policy through independent research") against the pattern of what gets published — most output is defence / China-focused, consistent with the mission and funding
- [ ] PASS: Output's credibility assessment table rates dimensions independently — ownership transparency (HIGH — donors public), editorial accountability (MEDIUM-HIGH — named authors, but no formal peer review), accuracy track record (HIGH on factual primary research, MEDIUM on policy framing), bias transparency (MEDIUM — disclosure exists but readers may miss the funding context)
- [ ] PASS: Output distinguishes BIAS (systematic pattern toward certain conclusions) from ERROR (specific factual inaccuracies) — these are separate dimensions; ASPI may have predictable framing without making errors
- [ ] PASS: Output's "appropriate use" section is concrete — ASPI is reliable for primary research on China military / cyber capability, defence procurement debates, ICT supply chain analysis; less reliable as the SOLE source for defence policy choices; cross-check against ASPI's critics for a balanced view
- [ ] PASS: Output does NOT conclude "ASPI is correct/incorrect" on substantive defence policy questions — only assesses the source's reliability mechanisms
