#!/usr/bin/env python
"""
Test script to verify role-based access control in the CRM system.
This script tests that users with different roles can only access appropriate pages.
"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import authenticate
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm_eridan.settings')
django.setup()

from users.models import CustomUser

def test_role_access():
    """Test role-based access control for different user roles."""

    # Define test users and their expected access
    test_users = {
        'admin_test': {
            'role': 'admin',
            'expected_access': ['client_requests', 'repair_requests', 'client_base', 'kanban', 'chat'],
            'unexpected_access': []
        },
        'manager_test': {
            'role': 'manager',
            'expected_access': ['client_requests', 'repair_requests', 'client_base', 'kanban', 'chat'],
            'unexpected_access': []
        },
        'chief_test': {
            'role': 'chief',
            'expected_access': ['client_requests', 'repair_requests', 'client_base', 'kanban', 'chat'],
            'unexpected_access': []
        },
        'design_chief_test': {
            'role': 'design_chief',
            'expected_access': ['client_requests', 'client_base', 'kanban', 'chat'],
            'unexpected_access': ['repair_requests']
        },
        'production_chief_test': {
            'role': 'production_chief',
            'expected_access': ['client_requests', 'repair_requests', 'client_base', 'kanban', 'chat'],
            'unexpected_access': []
        },
        'executor_test': {
            'role': 'executor',
            'expected_access': ['client_base', 'kanban', 'chat'],
            'unexpected_access': ['client_requests', 'repair_requests']
        }
    }

    # URLs to test
    test_urls = {
        'client_requests': '/client_requests/',
        'repair_requests': '/repair_requests/',
        'client_base': '/client_base/',
        'kanban': '/kanban/',
        'chat': '/chat/',
        'home': '/',
    }

    print("🧪 Testing Role-Based Access Control")
    print("=" * 50)

    all_tests_passed = True

    for username, user_config in test_users.items():
        print(f"\n👤 Testing user: {username} (role: {user_config['role']})")
        print("-" * 40)

        # Create test client and login
        client = Client()
        login_success = client.login(username=username, password='test123')

        if not login_success:
            print(f"❌ Login failed for {username}")
            all_tests_passed = False
            continue

        print(f"✅ Login successful for {username}")

        # Test expected access
        for url_name in user_config['expected_access']:
            if url_name in test_urls:
                url = test_urls[url_name]
                response = client.get(url)
                if response.status_code == 200:
                    print(f"✅ {url_name}: Access granted (200)")
                else:
                    print(f"❌ {url_name}: Access denied ({response.status_code}) - Expected access")
                    all_tests_passed = False

        # Test unexpected access (should be denied)
        for url_name in user_config['unexpected_access']:
            if url_name in test_urls:
                url = test_urls[url_name]
                response = client.get(url)
                if response.status_code == 403:
                    print(f"✅ {url_name}: Access correctly denied (403)")
                elif response.status_code == 200:
                    print(f"❌ {url_name}: Access granted (200) - Should be denied")
                    all_tests_passed = False
                else:
                    print(f"⚠️  {url_name}: Unexpected response ({response.status_code})")

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All role-based access control tests PASSED!")
    else:
        print("❌ Some role-based access control tests FAILED!")

    return all_tests_passed

def test_decorators():
    """Test that decorators work correctly."""
    print("\n🛡️  Testing Role-Based Decorators")
    print("=" * 50)

    from users.decorators import admin_required, manager_required, executor_required
    from django.http import HttpRequest
    from django.contrib.auth.models import AnonymousUser

    # Create mock request
    request = HttpRequest()
    request.method = 'GET'

    # Test with different users
    test_cases = [
        ('admin_test', admin_required, True),
        ('manager_test', admin_required, False),
        ('executor_test', admin_required, False),
        ('manager_test', manager_required, True),
        ('executor_test', manager_required, False),
        ('executor_test', executor_required, True),
        ('manager_test', executor_required, False),
    ]

    all_decorator_tests_passed = True

    for username, decorator, should_pass in test_cases:
        try:
            user = CustomUser.objects.get(username=username)
            request.user = user

            # Test the decorator
            decorated_func = decorator(lambda r: "success")
            result = decorated_func(request)

            if should_pass and result == "success":
                print(f"✅ {username} with {decorator.__name__}: Access granted")
            elif not should_pass and hasattr(result, 'status_code') and result.status_code == 403:
                print(f"✅ {username} with {decorator.__name__}: Access correctly denied")
            else:
                print(f"❌ {username} with {decorator.__name__}: Unexpected result")
                all_decorator_tests_passed = False

        except Exception as e:
            print(f"❌ Error testing {username} with {decorator.__name__}: {e}")
            all_decorator_tests_passed = False

    if all_decorator_tests_passed:
        print("🎉 All decorator tests PASSED!")
    else:
        print("❌ Some decorator tests FAILED!")

    return all_decorator_tests_passed

if __name__ == '__main__':
    print("🚀 Starting CRM Role-Based Access Control Tests")
    print("Server should be running at http://127.0.0.1:8000/")
    print()

    # Run tests
    access_tests_passed = test_role_access()
    decorator_tests_passed = test_decorators()

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Role-Based Access Tests: {'✅ PASSED' if access_tests_passed else '❌ FAILED'}")
    print(f"Decorator Tests: {'✅ PASSED' if decorator_tests_passed else '❌ FAILED'}")

    if access_tests_passed and decorator_tests_passed:
        print("\n🎉 ALL TESTS PASSED! Role-based access control is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ SOME TESTS FAILED! Please check the implementation.")
        sys.exit(1)
