# Expected Review: Bad Example

## Findings

### Error

1. **contract** `examples/bad-repo/orchestrator.instructions.md`
   - **Class:** confirmed
   - **Issue:** The orchestrator relies on an unstated state file and does not declare its expected outputs.
   - **Evidence:** The instructions say to read "the usual state file" and never identify a concrete output artifact or completion contract.
   - **Why it matters:** Downstream collaborators cannot verify what the orchestrator consumes or produces.
   - **Suggested fix:** Add an explicit contract that names the state file, declared outputs, and completion signals.

### Warning

1. **pattern** `examples/bad-repo/orchestrator.instructions.md`
   - **Class:** confirmed
   - **Issue:** One orchestrator owns acquisition, execution, retry handling, debugging, reporting, and cleanup.
   - **Evidence:** The opening paragraph assigns nearly the entire system lifecycle to a single unit.
   - **Why it matters:** Over-centralization makes failures harder to isolate and turns handoffs into implicit behavior.
   - **Suggested fix:** Split the unit into narrower responsibilities such as coordination, execution, reporting, and cleanup.
