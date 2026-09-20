# Repository Documentation & State Architecture

**Document Role**: Meta-Specification for Repository Documentation Conventions  
**Status**: ACTIVE STANDARD  
**Last Updated**: 2026-09-19  

---

## 🏛️ 1. Purpose & Core Philosophy

Computational science projects often suffer from **temporal conflation**: different documents claim to describe the model or results at different points in time, with no clear hierarchy of authority. When an agent or human joins the project, conflicting descriptions create stale-documentation bugs and unverified claims.

This repository enforces a **two-dimensional information architecture** that strictly decouples **Current State** from **Historical Record**, and separates **Technical Truth** (code, configuration, data) from **Scientific Interpretation**.

```
                           THE DOCUMENTATION ARCHITECTURE

         OPERATIONAL LAYER                 CURRENT STATE LAYER
       ┌────────────────────┐            ┌─────────────────────┐
       │     HANDOFF.md     │───────────►│  CURRENT_STATE.md   │
       │  "Read this first" │            │   "Where we are"    │
       └────────────────────┘            └──────────┬──────────┘
                                                    │
                 ┌──────────────────────────────────┴──────────────────┐
                 ▼                                                     ▼
       ┌────────────────────┐                                ┌───────────────────┐
       │      PLAN.md       │                                │   baseline.yaml   │
       │   "Where we go"    │                                │  "What executes"  │
       └────────────────────┘                                └───────────────────┘

                           HISTORICAL & SCIENTIFIC LAYER
       ┌────────────────────┐    ┌─────────────────────┐    ┌───────────────────┐
       │    DECISIONS.md    │    │     snapshots/      │    │     reports/      │
       │ "Why we decided it"│    │"What we believed at"│    │"What was formally"│
       │   (Append-Only)    │    │ (Commit Time-Capsule│    │    established    │
       └────────────────────┘    └─────────────────────┘    └───────────────────┘
```

---

## 🧭 2. Two-Dimensional Document Classification

### A. Current-State Documents (Living & Synchronized)
1. **[`HANDOFF.md`](../HANDOFF.md)**:
   - **Audience**: Incoming humans, coding agents, and review agents starting a new session.
   - **Role**: Compact (1–2 page) operational summary of the project state at the current git `HEAD`.
   - **Rule**: Must be updated whenever the active phase, milestone status, or next action changes.
2. **[`docs/CURRENT_STATE.md`](../docs/CURRENT_STATE.md)**:
   - **Audience**: Researchers, agents implementing models, and scientific reviewers.
   - **Role**: Detailed, canonical description of the active model, geometry, boundary conditions, loading, materials, empirical results, and characterized limitations.
   - **Rule**: The living single-point-of-truth for scientific interpretation. Updated whenever the scientific state changes.
3. **[`PLAN.md`](../PLAN.md)**:
   - **Audience**: All project contributors.
   - **Role**: Forward-looking master research roadmap, computational gates, and phase definitions.
   - **Rule**: Defines where we are going; does not redefine current implementation details.

### B. Historical & Scientific Records (Permanent, Append-Only, or Milestone Records)
4. **[`docs/DECISIONS.md`](../docs/DECISIONS.md)**:
   - **Role**: Append-only scientific and architectural decision log.
   - **Rule**: Never rewritten. When a prior decision is revised, a new decision is appended that explicitly supersedes the old one (e.g. `D004` supersedes `D002`).
5. **[`docs/snapshots/*.md`](../docs/snapshots/)**:
   - **Role**: Truly immutable historical snapshots capturing the exact research and model state at a specific milestone commit (e.g., `2026-09-19-phase4-freeze.md`).
   - **Rule**: Tied to a specific git commit SHA; never modified after creation.
6. **[`reports/*.md`](../reports/)**:
   - **Role**: Formal project and milestone scientific reports (e.g., [`phase4_fea_benchmark_report.md`](../reports/phase4_fea_benchmark_report.md)).
   - **Rule**: Records what each completed milestone investigation formally established. Normally stable upon phase completion, but correctable (for errata or precision fixes) with revision history preserved by Git. Does not serve as the living operational handoff.
7. **[`reports/archive/*.md`](../reports/archive/)**:
   - **Role**: Preserved legacy documentation (e.g., [`phase4_walkthrough_legacy.md`](../reports/archive/phase4_walkthrough_legacy.md)).
   - **Rule**: Clearly marked with an archival banner indicating that it has been superseded.

---

## ⚖️ 3. Hierarchy of Authority

When documents or data disagree, resolution is governed strictly by the following hierarchy:

```
Level 1: TECHNICAL TRUTH (Code, Executable Configs, Binary Data, & JSON Metrics)
         • models/*/baseline.yaml
         • data/metadata/*.json
         • results/*/*.json, *.csv
         • simulations/*/*.npz
         ▼
Level 2: CURRENT SCIENTIFIC INTERPRETATION
         • docs/CURRENT_STATE.md
         ▼
Level 3: OPERATIONAL HANDOFF & ROADMAP
         • HANDOFF.md
         • PLAN.md
         ▼
Level 4: HISTORICAL RECORD & SCIENTIFIC ARCHIVE
         • docs/snapshots/*.md (Truly immutable historical snapshots)
         • docs/DECISIONS.md (Append-only rationale log)
         • reports/*.md (Formal milestone records, correctable via Git)
```

- **Technical Fact Invariant**: Never re-declare or hardcode the same technical scalar (e.g. element count, canonical SHA-256 hash, energy value) in multiple competing places. Level 1 defines it; Level 2 interprets it; Level 3 documents may summarize Level 1 technical values for orientation, but must never become an independent authoritative source for those values.

---

## 📜 4. The Eight Core Documentation Rules

1. **Rule 1: One Technical Authority**  
   Code, configuration, and data artifacts are authoritative for technical facts. Current-state documents interpret and summarize them for orientation; they do not independently invent or redefine them.
2. **Rule 2: `HANDOFF.md` is Always Current**  
   Every new session or agent starts by reading `HANDOFF.md`. If the phase or next action changes, `HANDOFF.md` must be updated in the same commit.
3. **Rule 3: `docs/CURRENT_STATE.md` is Living**  
   Update it whenever the model geometry, materials, boundary conditions, or empirical conclusions change.
4. **Rule 4: Decisions are Append-Only**  
   Never edit past decisions in `docs/DECISIONS.md` to make past choices look cleaner. A revised decision gets a new entry (`D00X`) that explicitly supersedes the earlier entry.
5. **Rule 5: Snapshots are Immutable**  
   Every major milestone freeze generates a new file in `docs/snapshots/` bearing the date, milestone name, and exact git commit SHA. Once committed, a snapshot is frozen.
6. **Rule 6: Reports are Milestone Records, Not Operational Handoffs**  
   A scientific report formally records what a milestone investigation established. While normally stable upon phase completion, it remains correctable (e.g. for errata or precision adjustments) with revision history preserved by Git, but does not serve as the living operational handoff.
7. **Rule 7: Agents Must Independently Verify**  
   `HANDOFF.md` provides orientation, not proof. Review agents must independently inspect the code, execute tests, and verify JSON/NPZ data artifacts before approving work.
8. **Rule 8: Milestone Commits Update the State System**  
   Every milestone transition commit must be self-contained, updating `HANDOFF.md`, `docs/CURRENT_STATE.md`, logging any new decisions in `docs/DECISIONS.md`, and generating a snapshot in `docs/snapshots/`.
