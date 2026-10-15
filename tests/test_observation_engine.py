import unittest
from datetime import date
from observation_engine import build_observations

class TestObservations(unittest.TestCase):
    def test_opposing_flows_are_not_institutional_claims(self):
        p = {"is_live": False, "metrics": {"fund_flows": {
            "equity_net_flow_usd_millions": -100, "bond_net_flow_usd_millions": 200,
            "observation_period_end": "2026-10-07", "source_url": "https://example.org"}}}
        result = build_observations(p, date(2026, 10, 15))
        self.assertEqual(result["source_period_age_days"], 8)
        self.assertEqual(result["observations"][0]["absolute_flow_difference_usd_millions"], 300)
        self.assertIn("Does not establish", result["observations"][0]["interpretation_limit"])
    def test_missing_values_never_become_signals(self):
        result = build_observations({"metrics": {}}, date(2026, 10, 15))
        self.assertEqual([x["id"] for x in result["observations"]], ["missing_market_structure_data"])
    def test_zero_is_not_negative(self):
        p = {"metrics": {"fund_flows": {
            "equity_net_flow_usd_millions": 0, "bond_net_flow_usd_millions": 50,
            "observation_period_end": "2026-10-07", "source_url": "https://example.org"}}}
        result = build_observations(p, date(2026, 10, 15))
        self.assertFalse(any(x["id"] == "opposing_equity_bond_flows" for x in result["observations"]))

if __name__ == "__main__":
    unittest.main()
