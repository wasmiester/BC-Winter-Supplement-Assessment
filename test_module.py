import unittest
from unittest.mock import patch, MagicMock
import json
from main import calculate_winter_supplement, new_client  # Replace 'main' with your module name


class TestCalculateWinterSupplement(unittest.TestCase):

    def test_single_eligible_no_children(self):
        input_data = {
            "id": "test1",
            "familyUnitInPayForDecember": True,
            "familyComposition": "single",
            "numberOfChildren": 0
        }
        expected_output = {
            "id": "test1",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 0.0,
            "supplementAmount": 60.0
        }
        self.assertEqual(calculate_winter_supplement(input_data), expected_output)
        print("Test: test_single_eligible_no_children - OK")

    def test_couple_eligible_no_children(self):
        input_data = {
            "id": "test2",
            "familyUnitInPayForDecember": True,
            "familyComposition": "couple",
            "numberOfChildren": 0
        }
        expected_output = {
            "id": "test2",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 0.0,
            "supplementAmount": 120.0
        }
        self.assertEqual(calculate_winter_supplement(input_data), expected_output)
        print("Test: test_couple_eligible_no_children - OK")

    def test_single_eligible_with_children(self):
        input_data = {
            "id": "test3",
            "familyUnitInPayForDecember": True,
            "familyComposition": "single",
            "numberOfChildren": 2
        }
        expected_output = {
            "id": "test3",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 40.0,
            "supplementAmount": 100.0
        }
        self.assertEqual(calculate_winter_supplement(input_data), expected_output)
        print("Test: test_single_eligible_with_children - OK")

    def test_couple_eligible_with_children(self):
        input_data = {
            "id": "test4",
            "familyUnitInPayForDecember": True,
            "familyComposition": "couple",
            "numberOfChildren": 3
        }
        expected_output = {
            "id": "test4",
            "isEligible": True,
            "baseAmount": 120.0,
            "childrenAmount": 60.0,
            "supplementAmount": 180.0
        }
        self.assertEqual(calculate_winter_supplement(input_data), expected_output)
        print("Test: test_couple_eligible_with_children - OK")

    def test_not_eligible(self):
        input_data = {
            "id": "test5",
            "familyUnitInPayForDecember": False,
            "familyComposition": "single",
            "numberOfChildren": 1
        }
        expected_output = {
            "id": "test5",
            "isEligible": False,
            "baseAmount": 0.0,
            "childrenAmount": 0.0,
            "supplementAmount": 0.0
        }
        self.assertEqual(calculate_winter_supplement(input_data), expected_output)
        print("Test: test_not_eligible - OK")

    def test_invalid_family_composition(self):
        input_data = {
            "id": "test6",
            "familyUnitInPayForDecember": True,
            "familyComposition": "invalid_type",
            "numberOfChildren": 2
        }
        expected_output = {
            "id": "test6",
            "isEligible": True,
            "baseAmount": 0.0,
            "childrenAmount": 40.0,
            "supplementAmount": 40.0
        }
        self.assertEqual(calculate_winter_supplement(input_data), expected_output)
        print("Test: test_invalid_family_composition - OK")


class TestMQTTClient(unittest.TestCase):

    @patch('main.mqtt.Client')
    def test_mqtt_integration(self, MockMQTTClient):
        # Mock client instance
        mock_client = MagicMock()
        MockMQTTClient.return_value = mock_client
        client = new_client("mock_topic_id")
        mock_message = MagicMock()
        mock_message.payload.decode.return_value = json.dumps({
            "id": "test5",
            "familyUnitInPayForDecember": True,
            "familyComposition": "single",
            "numberOfChildren": 1
        })
        client.on_message(mock_client, None, mock_message)

        expected_output = {
            "id": "test5",
            "isEligible": True,
            "baseAmount": 60.0,
            "childrenAmount": 20.0,
            "supplementAmount": 80.0
        }
        mock_client.publish.assert_called_once_with(
            "BRE/calculateWinterSupplementOutput/mock_topic_id",
            json.dumps(expected_output)
        )
        print("Test: test_mqtt_integration - OK")


if __name__ == '__main__':
    unittest.main()
