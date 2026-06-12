# Planning fallacy and reference-class forecasting

Bottoms-up estimates made under stakeholder pressure are systematically optimistic. This is the [planning fallacy](https://en.wikipedia.org/wiki/Planning_fallacy) (Kahneman and Tversky): people forecast a task by imagining how it will go, and the imagined path almost never includes the delays, rework, and surprises that actually happen. The bias survives experience — teams that were late last time still under-estimate the next time.

## The correction: reference-class forecasting

Instead of estimating from the inside ("here are our tasks, here's how long each takes"), estimate from the outside. Find a reference class of similar past efforts, look at how long they actually took, and place the current effort in that distribution. This is [reference-class forecasting](https://en.wikipedia.org/wiki/Reference_class_forecasting) (Kahneman and Lovallo; operationalised by Flyvbjerg on large projects).

The move is concrete:

1. **Name the reference class** — past initiatives genuinely comparable to this one, not cherry-picked successes.
2. **Pull the actuals** — what those efforts actually cost in time, not what they were estimated to cost.
3. **Place this effort in the distribution** — typical, optimistic tail, or pessimistic tail, with a reason.
4. **Adjust the inside estimate toward the outside view** — if the bottoms-up number sits below the reference-class median, that gap is the planning-fallacy correction.

## When this applies

- Any commitment made under pressure — a roadmap date, a delivery forecast, a release window, a quarterly plan.
- The delivery manager applies it directly via reference-class forecasting on delivery commitments.
- The coordinator and CTO see it during scoping: when a bottoms-up estimate is being turned into a commitment, the reference class is the check on it.

## Anti-patterns

- **Treating the inside estimate as the answer.** A detailed task breakdown feels rigorous, but detail does not remove the bias — it hides it behind precision.
- **Padding instead of forecasting.** Adding a flat "buffer" is not reference-class forecasting. The buffer has no evidence behind it; the reference class does.
- **No reference class because "this is different."** Almost every effort feels unique from the inside. The outside view is the point precisely because the inside view always argues for uniqueness.
