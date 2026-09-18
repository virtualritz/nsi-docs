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
