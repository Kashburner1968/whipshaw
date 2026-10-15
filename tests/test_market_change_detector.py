import unittest
from market_change_detector import compare

class ChangeDetectorTests(unittest.TestCase):
    def test_change_with_provenance(self):
        a = {"metrics": {"spy_price": {"value": 772, "units": "USD", "observed_at": "2026-10-15T13:00:00-04:00", "source_url": "https://example.org/quote"}}}
        b = {"metrics": {"spy_price": {"value": 770.27, "units": "USD", "observed_at": "2026-10-15T14:00:00-04:00", "source_url": "https://example.org/quote"}}}
        result = compare(a, b)
        self.assertEqual(result["finding_count"], 1)
        self.assertAlmostEqual(result["findings"][0]["delta"], -1.73)
    def test_missing_source_not_reported(self):
        a = {"metrics": {"spy_price": {"value": 772, "units": "USD", "observed_at": "a"}}}
        b = {"metrics": {"spy_price": {"value": 770, "units": "USD", "observed_at": "b"}}}
        self.assertEqual(compare(a, b)["finding_count"], 0)
    def test_unchanged_timestamp_not_reported(self):
        point = {"value": 770, "units": "USD", "observed_at": "2026-10-15T14:00:00-04:00", "source_url": "https://example.org"}
        self.assertEqual(compare({"metrics": {"spy_price": point}}, {"metrics": {"spy_price": point}})["finding_count"], 0)

if __name__ == "__main__":
    unittest.main()
