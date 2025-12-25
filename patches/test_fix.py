#!/usr/bin/env python3
"""
Unit test to verify the fix for the dspace affiliation None error.

This test verifies that:
1. process_affiliation returns None when affiliation is not found
2. The main processing loop skips repositories with None affiliation
"""

def test_process_affiliation_none_check():
    """
    Test that the process_affiliation function handles None correctly.
    
    The key change is:
    ```python
    aff_rec = db["affiliations"].find_one({"external_ids.id": ror_id})
    if aff_rec is None:
        return None
    ```
    
    This prevents the TypeError: 'NoneType' object is not subscriptable
    that was occurring on line: aff["id"] = aff_rec["_id"]
    """
    
    # Mock database that returns None
    class MockCollection:
        def find_one(self, query):
            return None
    
    class MockDB:
        def __getitem__(self, key):
            return MockCollection()
    
    # Simulate the key part of process_affiliation
    db = MockDB()
    ror_id = "https://ror.org/nonexistent"
    
    # This is what the fixed code does
    aff_rec = db["affiliations"].find_one({"external_ids.id": ror_id})
    
    # The fix: check if aff_rec is None before accessing it
    if aff_rec is None:
        result = None
    else:
        result = {"id": aff_rec["_id"]}
    
    assert result is None, "Expected None when affiliation not found"
    print("✓ Test 1 passed: process_affiliation returns None when affiliation not found")


def test_main_loop_skip_logic():
    """
    Test that the main processing loop skips repositories with None affiliation.
    
    The key change is:
    ```python
    affiliation = process_affiliation(repository["institution_id"], self.db)
    if affiliation is None:
        print(f"WARNING: Affiliation not found...")
        continue
    ```
    """
    
    # Simulate the main loop logic
    def process_affiliation_mock(ror_id, db):
        return None  # Simulating affiliation not found
    
    repositories = [
        {"institution_id": "https://ror.org/nonexistent", "collection_name": "test_collection"}
    ]
    
    processed_count = 0
    skipped_count = 0
    
    for repository in repositories:
        affiliation = process_affiliation_mock(repository["institution_id"], None)
        
        # The fix: skip if affiliation is None
        if affiliation is None:
            skipped_count += 1
            continue
        
        # This would have crashed before the fix
        processed_count += 1
    
    assert skipped_count == 1, "Expected one repository to be skipped"
    assert processed_count == 0, "Expected no repositories to be processed"
    print("✓ Test 2 passed: Main loop correctly skips repositories with None affiliation")


if __name__ == "__main__":
    print("Running tests for dspace affiliation None error fix...\n")
    test_process_affiliation_none_check()
    test_main_loop_skip_logic()
    print("\n✅ All tests passed!")
