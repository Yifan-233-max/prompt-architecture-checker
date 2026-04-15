# Sample Parse Summary

## Repository Structure

- Primary artifact: `examples/sample-orchestrator.contract.json`
- Identified role: `ui-test-orchestrator` (`orchestrator`)
- Purpose: Coordinates CPC acquisition, UI execution, reporting, and release

## Likely Entrypoint

- `ui-test-orchestrator`

## Key Relationships

1. `ui-test-orchestrator` -> `cpc-connector` after `ACQUIRE`
2. `ui-test-orchestrator` -> `report-generator` after `EXECUTE`

## State And Artifact Signals

- reads `config/resource-pool.json`
- reads `/memories/session/test-state-session-N.md`
- writes `/memories/session/test-state-session-N.md`
- writes `reports/test-run.html`
- produces `evidence/session-N/`

## Evidence

- `handoffs` defines the `cpc-connector` and `report-generator` flow edges
- `completion` defines `Report file exists` and `Session resources released`

## Uncertainties

- failure-path cleanup is implied by the completion list, but it is not modeled as a separate explicit flow edge
