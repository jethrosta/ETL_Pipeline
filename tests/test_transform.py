import unittest
import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data

class TestTransform(unittest.TestCase):

    def test_transform_to_DataFrame(self):
        data = [
            {"Product Title": "Test Product", "Price": "$100", "Rating": "4.5", "Colors": "10 Colors", "Gender": "Unisex"}
        ]
        df = transform_to_DataFrame(data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 1)

    def test_transform_data(self):
        data = pd.DataFrame({
            "Product Title": ["Test Product", "Unknown Product"],
            "Price": ["$100", "Price not found"],
            "Rating": ["4.5", "Not Rated"],
            "Colors": ["10 Colors", "5 Colors"],
            "Gender": ["Men", "Unisex"]
        })
        transformed_data = transform_data(data, exchange_rate=16000)
        self.assertEqual(len(transformed_data), 1)  # Should remove the unknown product
        self.assertEqual(transformed_data["Price"].values[0], 1600000.0)  # Price in rupiah
        self.assertEqual(transformed_data["Rating"].values[0], 4.5)  # Rating should be cleaned
        self.assertEqual(transformed_data["Colors"].values[0], 10)
        self.assertEqual(transformed_data["Gender"].values[0], "Men")

if __name__ == '__main__':
    unittest.main()
