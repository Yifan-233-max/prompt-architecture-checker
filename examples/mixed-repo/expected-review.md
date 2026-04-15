# Expected Review: Mixed Example

## Findings

### Warning

1. **flow** `examples/mixed-repo/contracts/release-workflow.contract.json`
   - **Class:** high-risk-signal
   - **Issue:** The publish handoff is declared, but the workflow has no expected output or completion signal for that stage.
   - **Evidence:** The handoff names `publish-agent`, but the contract does not define an `expectedOutput` or any completion criteria.
   - **Why it matters:** Reviewers can see the path exists but cannot verify what successful publishing should return.
   - **Suggested fix:** Add an expected publish artifact or status output and declare the evidence that marks the workflow complete.

### Info

1. **contract** `examples/mixed-repo/contracts/release-workflow.contract.json`
   - **Class:** reviewability-gap
   - **Issue:** The workflow declares shared state reads and writes but does not explain the shape of that state.
   - **Evidence:** The contract references `memories/release-state.md` for both reads and writes without any field-level expectations.
   - **Why it matters:** Hidden structure inside shared state increases coupling and makes future reviews less reliable.
   - **Suggested fix:** Describe the state fields or split the shared state into narrower artifacts with clearer ownership.
