# Scienti Name Fields - Whitespace Issue

## Problem Description

Author names imported from Scienti JSON contain unwanted whitespace:
- Trailing spaces in surname fields (`TXT_PRIM_APELL`, `TXT_SEG_APELL`)
- Double spaces in full name field (`TXT_TOTAL_NAMES`)

### Example from Scienti JSON

```python
{
    "TXT_NAMES_RH": "Luz Elena",
    "TXT_PRIM_APELL": "Acevedo ",     # trailing space
    "TXT_SEG_APELL": "Lopera",
    "TXT_TOTAL_NAMES": "Luz Elena Acevedo  Lopera"  # double space
}
```

### Impact

This affects the display of author names on the ImpactU platform:
- URL: https://impactu.colav.co/person/0001547304/research/products
- Visible as extra spacing in author name display

## Solution

The fix needs to be applied in the **colav/Kahi_plugins** repository, specifically in:

**File:** `Kahi_scienti_person/kahi_scienti_person/Kahi_scienti_person.py`

### Issue Analysis

In the file `Kahi_scienti_person/kahi_scienti_person/Kahi_scienti_person.py` (colav/Kahi_plugins repository):

The code already applies `.strip()` in some locations (lines 97, 102, 108) but is **missing `.strip()`** in other critical sections where `TXT_PRIM_APELL` and `TXT_SEG_APELL` are used directly with `title_case()`.

### Required Changes

Note: Line numbers are approximate and based on analysis of the main branch as of December 2024. Please verify exact line numbers when applying the fix.

#### Location 1: Around lines 356-362
**Current code:**
```python
if "TXT_PRIM_APELL" in author.keys():
    entry["last_names"].append(
        title_case(author["TXT_PRIM_APELL"]))
if "TXT_SEG_APELL" in author.keys():
    if author["TXT_SEG_APELL"] is not None:
        entry["last_names"].append(
            title_case(author["TXT_SEG_APELL"]))
```

**Fixed code:**
```python
if "TXT_PRIM_APELL" in author.keys():
    entry["last_names"].append(
        title_case(author["TXT_PRIM_APELL"].strip()))
if "TXT_SEG_APELL" in author.keys():
    if author["TXT_SEG_APELL"] is not None:
        entry["last_names"].append(
            title_case(author["TXT_SEG_APELL"].strip()))
```

#### Location 2: Around lines 736-742
**Current code:**
```python
if "TXT_PRIM_APELL" in author.keys():
    entry["last_names"].append(
        title_case(author["TXT_PRIM_APELL"]))
if "TXT_SEG_APELL" in author.keys():
    if author["TXT_SEG_APELL"] is not None:
        entry["last_names"].append(
            title_case(author["TXT_SEG_APELL"]))
```

**Fixed code:**
```python
if "TXT_PRIM_APELL" in author.keys():
    entry["last_names"].append(
        title_case(author["TXT_PRIM_APELL"].strip()))
if "TXT_SEG_APELL" in author.keys():
    if author["TXT_SEG_APELL"] is not None:
        entry["last_names"].append(
            title_case(author["TXT_SEG_APELL"].strip()))
```

## Related Files

The following workflow files reference scienti processing:
- `workflows/impactu/kahi_impactu.yml`
- `workflows/impactu/kahi_impactu_dev.yml`
- `workflows/impactu/kahi_impactu_dev_12_08_2024.yml`
- `workflows/impactu/kahi_impactu_dev_20_12_2024.yml`

## Status

- Issue identified in: `colav/impactu` repository
- Fix required in: `colav/Kahi_plugins` repository
- Affects: Scienti person data processing pipeline
