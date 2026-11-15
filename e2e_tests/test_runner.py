"""
e2e_tests/test_runner.py
Test suite aggregator and runner for CornLearn LMS E2E tests.
Can be executed directly via:
    python e2e_tests/test_runner.py
or through Django management command:
    python manage.py test e2e_tests
"""

import os
import sys
import time
import unittest

# Ensure SkyLearn directory is on PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

try:
    import django
    django.setup()
    from django.test.runner import DiscoverRunner
except ImportError as exc:
    print(f"Warning: Django could not be imported ({exc}). Running in discovery mode only.")


def run_e2e_test_suite():
    """
    Discovers and executes all E2E test suites across Tiers 1-4,
    branding audits, form contracts, and responsive tokens.
    """
    print("=" * 80)
    print(" CornLearn LMS — Comprehensive E2E Test Suite Aggregator")
    print("=" * 80)
    start_time = time.time()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    modules_to_test = [
        "e2e_tests.test_branding_audit",
        "e2e_tests.test_form_contracts",
        "e2e_tests.test_responsive_tokens",
        "e2e_tests.test_tier1_features",
        "e2e_tests.test_tier2_boundaries",
        "e2e_tests.test_tier3_pairwise",
        "e2e_tests.test_tier4_journeys",
    ]

    for mod_name in modules_to_test:
        try:
            mod_suite = loader.loadTestsFromName(mod_name)
            suite.addTests(mod_suite)
            count = mod_suite.countTestCases()
            print(f"  [DISCOVERED] {mod_name:<36} : {count:>3} tests")
        except Exception as exc:
            print(f"  [ERROR LOADING] {mod_name}: {exc}")

    total_tests = suite.countTestCases()
    print("-" * 80)
    print(f" Total Tests Discovered: {total_tests}")
    print("-" * 80)

    # Use Django DiscoverRunner if Django is available
    if "django" in sys.modules:
        runner = DiscoverRunner(verbosity=2, interactive=False, keepdb=False)
        old_config = runner.setup_databases()
        try:
            result = unittest.TextTestRunner(verbosity=2).run(suite)
        finally:
            runner.teardown_databases(old_config)
    else:
        result = unittest.TextTestRunner(verbosity=2).run(suite)

    elapsed = time.time() - start_time
    print("=" * 80)
    print(" E2E Test Suite Execution Summary")
    print("=" * 80)
    print(f" Tests Run  : {result.testsRun}")
    print(f" Failures   : {len(result.failures)}")
    print(f" Errors     : {len(result.errors)}")
    print(f" Skipped    : {len(result.skipped)}")
    print(f" Time Taken : {elapsed:.2f} seconds")

    if result.wasSuccessful():
        print("\n [STATUS: PASS] All CornLearn E2E tests passed successfully!")
        print("=" * 80)
        return 0
    else:
        print("\n [STATUS: FAIL] Failures or errors detected in E2E tests.")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    exit_code = run_e2e_test_suite()
    sys.exit(exit_code)
