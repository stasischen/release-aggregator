# Dual-Layer POS Contract for Korean (KO-DICT-03)

## 1. Overview
This contract defines the two Part-of-Speech (POS) layers for the Lingourmet Korean dictionary. 
- **Layer 1: Teaching POS (`pos`)** - Optimized for language education and engine rules.
- **Layer 2: Universal POS (`upos`)** - Optimized for cross-language compatibility and automated pipeline processing.

## 2. Canonical Mapping Table

| Teaching POS (`pos`) | Description | UPOS | Mapping Strategy |
| :--- | :--- | :--- | :--- |
| `N` | Noun | `NOUN` | Standard |
| `V` | Verb | `VERB` | Standard |
| `ADJ` | Adjective | `ADJ` | Standard |
| `ADV` | Adverb | `ADV` | Standard |
| `PRON` | Pronoun | `PRON` | Standard |
| `DET` | Determiner | `DET` | Maps from legacy `M` |
| `NUM` | Number | `NUM` | Standard |
| `XNUM` | Digits | `NUM` | Specialized for digits |
| `COUNT` | Counter | `NOUN` | Korean Counters (units) |
| `PROP` | Proper Noun | `PROP` | Names, Places |
| `P` | Particle | `ADP` | Josa (Postposition) |
| `E` | Ending | `PART` | Eomi (Suffix) |
| `COP` | Copula | `COP` | Specialized for '이다' |
| `VX` | Auxiliary Verb | `VERB` | Secondary verbs |
| `INTJ` | Interjection | `INTJ` | Exclamations, Greetings |
| `PHRASE` | Phrase | `PHRASE` | Multi-word atoms |
| `PUNCT` | Punctuation | `PUNCT` | Symbols |
| `SPACE` | Space | `SPACE` | Layout |
| `UNK` | Unknown | `X` | Fallback |

## 3. Implementation Rules

### 3.1 Schema Enforcement
Every dictionary atom JSON MUST include both `pos` and `upos` fields as defined in `core-schema/schemas/dictionary_core.schema.json`.

### 3.2 Directory Structure
In `content-ko`, atoms are organzied into subdirectories matching their **Teaching POS** name:
- `dictionary/atoms/N/`
- `dictionary/atoms/V/`
- etc.

### 3.3 Resolver Consistency
The `atom_id` remains stable using the Teaching POS: `ko:<pos>:<lemma>`.
Example: `ko:v:가다` (pos=V, upos=VERB).

## 4. Sample Atom Payload

```json
{
  "atom_id": "ko:v:가다",
  "lemma_id": "가다",
  "fs_safe_id": "ko__v__가다",
  "pos": "V",
  "upos": "VERB",
  "surface_forms": ["가다"],
  "senses": [
    {
      "definition_ref": "base",
      "labels": []
    }
  ],
  "source_refs": ["A1-01"]
}
```
