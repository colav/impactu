# Fix Ready for kahi_plugins Repository

## Status: ✅ Code Changes Completed

The fix for the dspace affiliation None error has been successfully created and committed in a local clone of the kahi_plugins repository.

## Branch Information

- **Repository**: https://github.com/colav/kahi_plugins
- **Branch**: `fix-dspace-affiliation-none-error`
- **Commit**: `0ea7662`
- **Location**: `/home/runner/work/impactu/kahi_plugins`

## Changes Made

### 1. `Kahi_dspace_works/kahi_dspace_works/utils.py`

Added None check after database query:

```python
def process_affiliation(ror_id, db):
    """
    Returns
    -------
    dict | None
        affiliation processed or None if affiliation is not found in database.
    """
    aff_rec = db["affiliations"].find_one({"external_ids.id": ror_id})
    if aff_rec is None:  # ← NEW: Return None if not found
        return None
    aff = {}
    aff["id"] = aff_rec["_id"]
    # ... rest of function
```

### 2. `Kahi_dspace_works/kahi_dspace_works/Kahi_dspace_works.py`

Added check to skip repositories with None affiliation:

```python
affiliation = process_affiliation(repository["institution_id"], self.db)
if affiliation is None:  # ← NEW: Skip if affiliation not found
    print(f"WARNING: Affiliation not found for repository {repository['institution_id']}. Skipping repository {repository['collection_name']}.")
    continue
base_url = repository["repository_url"]
```

## Next Steps

The code is ready but could not be pushed to GitHub due to authentication constraints. To complete the PR:

### Option 1: Manual Push from This Environment

If you have access to this environment, run:

```bash
cd /home/runner/work/impactu/kahi_plugins
git push origin fix-dspace-affiliation-none-error
```

Then create a PR on GitHub from that branch.

### Option 2: Apply Patch Manually

Get the patch from the local repository:

```bash
cd /home/runner/work/impactu/kahi_plugins
git format-patch -1 HEAD --stdout > fix-dspace-affiliation-none-error.patch
```

Then apply it to your local kahi_plugins repo:

```bash
cd /your/local/kahi_plugins
git checkout -b fix-dspace-affiliation-none-error
git am < fix-dspace-affiliation-none-error.patch
git push origin fix-dspace-affiliation-none-error
```

### Option 3: Manual Code Changes

Simply apply the two small code changes shown above manually to:
1. `Kahi_dspace_works/kahi_dspace_works/utils.py` (line 73-74)
2. `Kahi_dspace_works/kahi_dspace_works/Kahi_dspace_works.py` (line 148-152)

## Verification

- ✅ Python syntax validated
- ✅ Changes are minimal (8 additions, 2 deletions)
- ✅ Follows existing code style
- ✅ Prevents TypeError when affiliation not found
- ✅ ETL continues processing other repositories
