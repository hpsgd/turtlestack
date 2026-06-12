# Test: audit-scaling-framework grounds the choice in the coordination problem

Scenario: Leadership is considering adopting SAFe across three teams. The coach must name the coordination problem first, test whether the need can be reduced by restructuring rather than coordinated, map the candidate frameworks to the problem, apply the deliberate-rejection test, and keep the recommendation advisory — resisting "adopt the industry default".

## Prompt

Use the agile-coach `audit-scaling-framework` skill to advise on a scaling decision. Context: there are three teams (billing, checkout, and accounts). Leadership wants to "adopt SAFe like everyone else." The actual pain is that the three teams keep blocking each other on a shared payments service, and a single shippable increment usually needs coordinated work across all three because the teams are split by component (billing-layer, checkout-layer, accounts-layer) rather than by feature. Produce the scaling assessment in the skill's standard format. Write the output to `docs/coaching/` in the current working directory.

Proceed without asking — produce the assessment.

## Criteria

- [ ] PASS: Names the coordination problem concretely first (teams blocking each other on the shared payments service; component-split teams forcing cross-team work to ship) — does not start from the framework
- [ ] PASS: Tests whether the coordination need can be reduced by restructuring into feature teams rather than coordinated by a framework — the reduce-the-need-first move
- [ ] PASS: Maps the candidate frameworks (LeSS, Nexus, Scrum@Scale, SAFe) to this specific problem with where each fits and its caution, rather than a generic framework summary
- [ ] PASS: Applies the deliberate-rejection test — picking no framework is a legitimate outcome; with only three teams, lightweight coordination may suffice and SAFe is likely overkill
- [ ] PASS: Pushes back on "adopt SAFe because everyone uses it" — naming that the industry-default rationale optimises for looking standard, not for solving the actual problem
- [ ] PASS: Connects the recommendation to team topology — the component-team split is the real driver, and reorganising into feature teams may remove the dependency entirely
- [ ] PASS: Keeps the recommendation advisory — adopting a scaling framework is an org-structural decision for the coordinator and leads
- [ ] PARTIAL: If a framework is recommended at all, prefers the lightest that fits rather than the heaviest

## Output expectations

- [ ] PASS: Output is a structured scaling assessment stating the coordination problem, whether it can be reduced, a candidate-fit table, and an advisory recommendation
- [ ] PASS: The recommendation leads with reduce-the-need (restructure toward feature teams) before any framework, given the component-split root cause
- [ ] PASS: The candidate-fit table covers LeSS, Nexus, Scrum@Scale, and SAFe with a fit verdict and rationale tied to three teams blocking on a shared service
- [ ] PASS: Output explicitly rejects "adopt SAFe by default" and explains why the industry-default rationale is the weakest one
- [ ] PASS: Output frames the decision as advisory to the coordinator/leads, not a call the coach makes
- [ ] PARTIAL: If suggesting any framework, output prefers the lightest that fits (e.g. LeSS over SAFe for three teams) and flags SAFe as overkill here
