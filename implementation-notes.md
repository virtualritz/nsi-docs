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

## Closed Anchor Cost Feedback

- Kept required direction and matching open endpoints.
- Made the shared source vertex the preferred closed anchor, with renderer fallback even when that vertex exists. A known vertex alone does not supply its surface parameter.
- Applied the fallback to both single-segment and multi-segment closed uses. Optional range rotation remains available.
- Recorded the follow-up results as implementer reports; no independent renderer validation or universal claim for the Newell-vector method.
- Updated NURBS and T-NURCC cross-references to remove mandatory matching closed starts.
- Validation: the book build and diff checks passed. The updated shared-boundary prose passes the sentence-length check; the build retains its preprocessor version warning.

## Renderable NURBS Curves and Point Welds

- Retired the geometry-bearing edge proposal; kept its URL as a short pointer to the replacement pages.
- Added a draft nurbs-curves reference with batched geometry, curve attributes, and P/Pw naming.
- Proposed separate point-use arrays in the existing weld namespace, with endpoint and interior-parameter examples.
- Required declared curve joins to remain joined under displacement; left junction construction and appearance to the renderer.
- Used AIR's documented NuCurves geometry as a precedent; did not assert unverified RenderDotC behavior.
