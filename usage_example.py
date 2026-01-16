"""
Integration example showing how to use the fixed authenticate_cvlac function.

This demonstrates how existing code can be updated to use the fixed version
that ensures proper browser cleanup.
"""

def example_usage():
    """Example of how to use the fixed authenticate_cvlac function."""
    
    # Before: using the original function (leaves browsers open)
    # from autofillcvlac.core import authenticate_cvlac
    
    # After: using the fixed function (proper browser cleanup)
    from cvlac_auth_fix import authenticate_cvlac_fixed as authenticate_cvlac
    
    # Same parameters as before
    result = authenticate_cvlac(
        nacionalidad='Colombiana',
        nombres='Research User',
        documento_identificacion='12345678',
        password='secure_password123',
        headless=True  # Run in headless mode
    )
    
    # Check result
    if result['status'] == 'success':
        print("✓ Authentication successful")
        print(f"Session active: {result['session_active']}")
    else:
        print(f"✗ Authentication failed: {result['message']}")
    
    return result

def example_with_foreign_nationality():
    """Example for users with foreign nationality."""
    
    from cvlac_auth_fix import authenticate_cvlac_fixed
    
    result = authenticate_cvlac_fixed(
        nacionalidad='Extranjero - otra',
        nombres='Foreign Researcher',
        documento_identificacion='987654321',
        password='password123',
        pais_nacimiento='Estados Unidos',  # Required for foreign nationality
        headless=True
    )
    
    return result

if __name__ == '__main__':
    print("CVLaC Authentication Fix - Usage Examples")
    print("=" * 50)
    
    print("\n1. Basic usage example:")
    try:
        result1 = example_usage()
        print(f"Result: {result1}")
    except Exception as e:
        print(f"Expected error (no helium): {e}")
    
    print("\n2. Foreign nationality example:")
    try:
        result2 = example_with_foreign_nationality()
        print(f"Result: {result2}")
    except Exception as e:
        print(f"Expected error (no helium): {e}")
    
    print("\n3. Error handling example:")
    from cvlac_auth_fix import authenticate_cvlac_fixed
    
    # Missing required field
    result3 = authenticate_cvlac_fixed('', 'Name', '123', 'pass')
    print(f"Validation error: {result3}")
    
    # Missing pais_nacimiento for foreign user
    result4 = authenticate_cvlac_fixed('Extranjero - otra', 'Name', '123', 'pass')
    print(f"Foreign nationality error: {result4}")
    
    print("\n✓ All examples completed successfully!")
    print("\nNote: The function requires the 'helium' package for actual browser automation.")
    print("In this environment, it demonstrates the error handling and validation logic.")