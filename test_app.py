"""
Test script for MaskDNS application
Run with: python test_app.py
"""
import os
import sqlite3
import requests
from app import app, init_db, clean_domain, validate_url

def test_database_init():
    """Test database initialization"""
    print("Testing database initialization...")
    init_db()
    if os.path.exists('domains.db'):
        print("✓ Database file created")
        return True
    print("✗ Database file not found")
    return False

def test_database_schema():
    """Test database schema"""
    print("\nTesting database schema...")
    conn = sqlite3.connect('domains.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='domain_mappings'")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        print("✓ domain_mappings table exists")
        return True
    print("✗ domain_mappings table not found")
    return False

def test_clean_domain():
    """Test domain cleaning function"""
    print("\nTesting clean_domain function...")
    tests = [
        ("http://example.com", "example.com"),
        ("https://example.com", "example.com"),
        ("example.com/path", "example.com"),
        ("EXAMPLE.COM", "example.com"),
        ("  example.com  ", "example.com"),
    ]
    
    passed = 0
    for input_val, expected in tests:
        result = clean_domain(input_val)
        if result == expected:
            print(f"  ✓ {input_val} → {result}")
            passed += 1
        else:
            print(f"  ✗ {input_val} → {result} (expected {expected})")
    
    print(f"Passed {passed}/{len(tests)} tests")
    return passed == len(tests)

def test_validate_url():
    """Test URL validation function"""
    print("\nTesting validate_url function...")
    tests = [
        ("https://example.com", True),
        ("http://example.com", True),
        ("ftp://example.com", False),
        ("example.com", False),
        ("not-a-url", False),
    ]
    
    passed = 0
    for url, expected in tests:
        result = validate_url(url)
        if result == expected:
            print(f"  ✓ {url} → {result}")
            passed += 1
        else:
            print(f"  ✗ {url} → {result} (expected {expected})")
    
    print(f"Passed {passed}/{len(tests)} tests")
    return passed == len(tests)

def test_app_routes():
    """Test Flask routes"""
    print("\nTesting Flask routes...")
    app.config['TESTING'] = True
    client = app.test_client()
    
    tests = [
        ('/', 200, "Landing page"),
        ('/admin/login', 200, "Admin login page"),
        ('/admin', 302, "Admin redirect (not logged in)"),
        ('/nonexistent', 404, "404 handler"),
    ]
    
    passed = 0
    for route, expected_status, description in tests:
        response = client.get(route)
        if response.status_code == expected_status:
            print(f"  ✓ {route} → {response.status_code} ({description})")
            passed += 1
        else:
            print(f"  ✗ {route} → {response.status_code} (expected {expected_status}, {description})")
    
    print(f"Passed {passed}/{len(tests)} tests")
    return passed == len(tests)

def test_crud_operations():
    """Test CRUD operations"""
    print("\nTesting CRUD operations...")
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Login
    with client.session_transaction() as sess:
        sess['admin_logged_in'] = True
    
    # Create mapping
    response = client.post('/admin/add', data={
        'custom_domain': 'test.example.com',
        'target_url': 'https://example.com'
    }, follow_redirects=True)
    
    if response.status_code == 200:
        print("  ✓ Create mapping successful")
    else:
        print(f"  ✗ Create mapping failed ({response.status_code})")
        return False
    
    # Verify mapping exists
    conn = sqlite3.connect('domains.db')
    conn.row_factory = sqlite3.Row
    mapping = conn.execute('SELECT * FROM domain_mappings WHERE custom_domain = ?', 
                          ('test.example.com',)).fetchone()
    conn.close()
    
    if mapping:
        print("  ✓ Mapping found in database")
        mapping_id = mapping['id']
    else:
        print("  ✗ Mapping not found in database")
        return False
    
    # Toggle mapping
    response = client.post(f'/admin/toggle/{mapping_id}', follow_redirects=True)
    if response.status_code == 200:
        print("  ✓ Toggle mapping successful")
    else:
        print(f"  ✗ Toggle mapping failed ({response.status_code})")
    
    # Delete mapping
    response = client.post(f'/admin/delete/{mapping_id}', follow_redirects=True)
    if response.status_code == 200:
        print("  ✓ Delete mapping successful")
    else:
        print(f"  ✗ Delete mapping failed ({response.status_code})")
    
    return True

def cleanup():
    """Cleanup test database"""
    print("\nCleaning up test database...")
    if os.path.exists('domains.db'):
        os.remove('domains.db')
        print("✓ Test database removed")

def main():
    """Run all tests"""
    print("=" * 60)
    print("MaskDNS Test Suite")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Database Initialization", test_database_init()))
    results.append(("Database Schema", test_database_schema()))
    results.append(("Clean Domain Function", test_clean_domain()))
    results.append(("Validate URL Function", test_validate_url()))
    results.append(("Flask Routes", test_app_routes()))
    results.append(("CRUD Operations", test_crud_operations()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
    
    # Cleanup
    cleanup()
    
    return passed == total

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
