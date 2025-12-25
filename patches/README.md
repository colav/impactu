# Patches for Kahi Plugins

This directory contains patches for the [kahi_plugins](https://github.com/colav/kahi_plugins) repository.

## fix-dspace-affiliation-none-error.patch

### Issue
Fixes [ETL] error procesando dspace - TypeError: 'NoneType' object is not subscriptable

### Description
The `process_affiliation` function in `Kahi_dspace_works/kahi_dspace_works/utils.py` was attempting to access properties of `aff_rec` without checking if it was `None`. This occurred when a repository's affiliation (ROR ID) was not found in the database.

According to the requirement: "si la afiliación no tiene id no se le puede asignar afiliación al autor del producto" (if the affiliation doesn't have an id, the affiliation cannot be assigned to the product's author).

### Changes
1. **utils.py**: Modified `process_affiliation()` to return `None` when the affiliation is not found in the database, instead of crashing.
2. **Kahi_dspace_works.py**: Added a check in the `run()` method to skip processing repositories when the affiliation is not found, logging a warning message.

**Note**: The fix maintains consistency with the existing codebase style (uses `print()` for logging as the rest of the codebase does). The existing typo `dsapce_db` in the original code is preserved to keep changes minimal.

### How to Apply
```bash
cd /path/to/kahi_plugins
git apply /path/to/this/fix-dspace-affiliation-none-error.patch
```

### Testing
After applying the patch, the ETL process will:
- Continue processing when a repository's affiliation is not found in the database
- Log a warning message indicating which repository was skipped
- Not crash with a TypeError

### Files Modified
- `Kahi_dspace_works/kahi_dspace_works/utils.py`
- `Kahi_dspace_works/kahi_dspace_works/Kahi_dspace_works.py`
