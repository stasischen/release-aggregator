# DeepSeek Prompt

Use `deepseek-v4-flash` for first-pass inventory, then escalate to `deepseek-v4-pro` before any
decision that changes dictionary UI semantics.

Repo: `/Users/ywchen/Dev/lingo/lingo-frontend-web`

Task: Inventory the dictionary candidate / homograph UI gap.

Check:

- Existing service APIs: `DictionaryService`, `DictionaryResolver`, `DictionaryMappingCandidate`,
  `DictionaryAtomLookup`, and `mapping_v2` tests.
- Product UI consumers: dictionary hub, immersive overlay, video dictionary panel, ULV support panels.
- The smallest UI slice that exposes multiple candidates without changing runtime contract shape.
- Test updates needed for candidate lists, same-POS senses, cross-POS homographs, and no-context fallback.

Constraints:

- Do not remove or bypass `mapping_v2` origin cache.
- Do not change dictionary runtime contract shape.
- Do not collapse domain-specific adapter semantics into one generic adapter.
- Output risks and recommended implementation order.

