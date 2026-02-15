# Reversible Decomposition: The Mapping Table Strategy

**Goal**: Ensure language content can be atomized while preserving the ability to perfectly reconstruct original text using a flat mapping system.

## 1. The V5 Standard: Mapping Table
Instead of complex nested JSON structures, V5 uses a **Flat Mapping Table** (CSV or JSON) to define how a surface form is decomposed.

### Example: "000원이에요"
In `mapping.json`:
```json
"000원이에요": "ko_XNUM_000+ko_N_원+ko_VCP_이다+ko_E_에요"
```

### Components:
1.  **Surface Key**: The exact text as it appears in the source (e.g., `000원이에요`).
2.  **Atom IDs**: The components connected by `+`.
    - `ko_XNUM_000`: Number Atom
    - `ko_N_원`: Unit Atom
    - `ko_VCP_이다`: Copula (Grammar/Particle)
    - `ko_E_에요`: Ending (Grammar/Particle)

## 2. Reconstruction Logic
Reconstruction is performed by looking up the Surface form in the Mapping Table.
`Original Text = MappingKey`
The `+` separated values provide the linguistic breakdown for the UI/Player to show definitions, while the **Key** provides the exact display string.

## 3. Benefits of Mapping-based Reversibility
- **Simplicity**: No need for complex "segment" objects in dialogue files. Dialogue files stay clean with just text.
- **Global Consistency**: One mapping entry fixes the decomposition for that word across the entire course.
- **App-Side Logic**: The frontend simply does a string-match against the mapping table to "light up" the atoms.

## 4. Implementation SOP
1.  **Ingestion**: `import_lllo_raw.py` parses source text and updates the global `mapping.json`.
2.  **Validation**: `audit_reconstruction.py` verifies that every mapped surface matches the reconstruction logic of the engine.
3.  **Atomization**: Extract individual atoms into `.json` files for long-form definitions.
