# Shared Boundary Proposal

- Unified the NURBS stitching draft and weld proposal under one identity model.
- Changed the recommendation to one weld namespace per solid, with local use tables on geometry.
- Retained per-boundary nodes as an alternative with explicit node counts and trade-offs.
- A use can select a whole trim loop or an ordered segment chain; counterparts need not have matching segmentation.
- Added concrete five-curve-to-one-boundary and multiple-join examples.
- Kept displacement, tessellation, and geometric correspondence algorithms outside the proposal.
- Reframed shared 3D edge curves as an optional extension. Removed the unsupported exporter crack attribution.
- Updated trim packaging, T-NURCC stitching, and naming cross-references for consistency.
- Made exporter validity explicit: spatial and length agreement within source tolerance, with no matching granularity requirement.
- Validation: `just book` and `git diff --check` passed; local links on the six design pages resolve. The build retains the mdbook-admonish version warning.

## First Implementer Feedback

- Proposed a shared start and direction after reversal; no new direction attribute. This replaces the previous allowance for arbitrary closed-loop seams.
- Did not adopt a universal anti-parallel rule or equal-parameter sample pairing. Those would conflict with non-manifold uses and differing parameterizations.
- Kept mixed selectors, with adjacency on one effective retained boundary component and no duplicate portions.
- Defined the incident region for hole and legacy outside trims.
- Required matching geometric range endpoints without requiring equal local parameter values or segment breaks.
- Recorded the reported single-segment and self-seam observations as implementer evidence, not independently reproduced measurements.
- Validation: `just book`, `git diff --check`, local link checks, and the partial-range example arithmetic passed. The existing preprocessor version warning remains. No renderer tests were run.

## Integration with Published Implementation Notes

- Integrated the notes from master commit `33b1e36` with the local contract revisions.
- Consolidated the reported measurements and coverage limits into one evidence table.
- Removed superseded inline suggestions, including the claim that opposite directions alone permit direct sample pairing.
- Preserved the reported fixture counts, closed-boundary failures, partial ranges, single-segment defaults, and self-seam evidence.
