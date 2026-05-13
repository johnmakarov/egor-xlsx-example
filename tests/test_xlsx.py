from pathlib import Path
import pandas as pd


class XLSXTester:
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.df = pd.read_excel(self.file_path)

    def get_values_from_column(self, column_name: str) -> list:
        if column_name not in self.df.columns:
            raise ValueError(f"Колонка '{column_name}' не найдена в файле.")
        return self.df[column_name].to_list()

    def get_value_from_column(self, column_name: str, index: int = 0):
        if column_name not in self.df.columns:
            raise ValueError(f"Колонка '{column_name}' не найдена в файле.")
        if index >= len(self.df) or index < -len(self.df):
            raise IndexError(f"Индекс {index} вне диапазона.")
        return self.df[column_name].iloc[index]


class TestExpenses:
    def test_download_xlsx_with_data(self, page, base_url, download_file_from):
        page.goto(base_url)

        page.get_by_test_id("input-description").fill("кофе")
        page.get_by_test_id("input-amount").fill("350")
        page.get_by_test_id("btn-add").click()

        page.get_by_test_id("input-description").fill("обед")
        page.get_by_test_id("input-amount").fill("890")
        page.get_by_test_id("btn-add").click()

        page.wait_for_selector("[data-testid='expense-item-2']")

        file_path = download_file_from("[data-testid='btn-download']")
        tester = XLSXTester(file_path)

        descriptions = tester.get_values_from_column("Description")
        amounts = tester.get_values_from_column("Amount")

        assert "кофе" in descriptions
        assert "обед" in descriptions
        assert 350.0 in amounts
        assert 890.0 in amounts


    def test_xlsx_headers(self, page, base_url, download_file_from):
        page.goto(base_url)

        page.get_by_test_id("input-description").fill("тест")
        page.get_by_test_id("input-amount").fill("100")
        page.get_by_test_id("btn-add").click()

        file_path = download_file_from("[data-testid='btn-download']")
        tester = XLSXTester(file_path)

        assert "Description" in tester.df.columns
        assert "Amount" in tester.df.columns
        assert "Date" in tester.df.columns
