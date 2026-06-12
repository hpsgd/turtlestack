# Test: facilitate-sprint-review reframes a demo into a working session

Scenario: A coach is asked to fix a sprint review that has become a polished slideshow to management. The skill must reframe it as a working session that inspects the increment against the DoD and adapts the backlog, draw out passive stakeholders, watch for the HIPPO effect, and keep the product manager owning the backlog.

## Prompt

Use the agile-coach `facilitate-sprint-review` skill to coach the "billing" team's sprint review. Context: the review has turned into a 30-slide presentation to the head of product, who does most of the talking; other stakeholders sit silent and nod; the team often shows screenshots rather than running software, and the backlog never actually changes as a result. Write the review coaching output to `docs/coaching/` in the current working directory. Respond in the skill's standard format.

Proceed without asking — coach the review and produce the output.

## Criteria

- [ ] PASS: Reframes the review as a collaborative working session that inspects the increment and adapts the backlog — explicitly not a demo or status update to management
- [ ] PASS: States that only Definition-of-Done-complete work should be presented and flags the screenshot-instead-of-running-software problem
- [ ] PASS: Names the HIPPO effect (the head of product dominating) and gives a concrete move to counter it so quiet stakeholders contribute
- [ ] PASS: Keeps the product manager / product owner owning the backlog conversation — the coach facilitates the working-session craft, does not take over the backlog
- [ ] PASS: Defines review success as the backlog visibly changing (items added, reordered, dropped), not as applause or a clean presentation
- [ ] PASS: Gives at least one concrete facilitation move to convert passive stakeholders into participants (hand driving to a stakeholder, direct named prompts, dot voting on next priorities)
- [ ] PARTIAL: Keeps the review distinct from sprint planning — inspecting/adapting the backlog is the review's job, not deciding the next sprint's scope

## Output expectations

- [ ] PASS: Output is a structured review-coaching artifact with a framing note (working session vs demo), the increment inspection against DoD, backlog adaptation, and coaching notes
- [ ] PASS: Output records whether items not meeting the DoD were presented and flags that for coach-definition-of-done
- [ ] PASS: Output names the HIPPO/dominance issue with the specific stakeholder (head of product) and a mitigation
- [ ] PASS: Output frames the measure of success as backlog change, and assigns backlog ownership to the product manager, not the coach
- [ ] PARTIAL: Output offers concrete drift-correction moves (hand driving to a stakeholder, replace "any questions?" with a direct named prompt) rather than a generic "make it collaborative"
