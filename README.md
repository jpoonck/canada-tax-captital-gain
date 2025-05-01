# Trading Analysis Project

This project is designed to calculate capital gains, losses, and tax implications for a series of trades with data sorcering from a IBKR CSV file. The project uses pandas for data manipulation and numpy for numerical computations.

## Setup

1. Install dependencies:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

Place your IBKR trading data in the `data/` directory and run the scripts in the `src/` directory to perform analysis and summary.

## Command Line Arguments

The script accepts a command-line argument to specify the path to the trades activity CSV file:

* `--file`: Path to the trades activity CSV file. Defaults to `./data/test.csv`.
* `--output`: Path to save the output report CSV file. Defaults to `./tmp/trades_tax_report.csv`
* `--rate`: Exchange rate to convert report to target currency. Defaults to 1.3698.

Example:

```sh
py main.py --file ./data/my_trades.csv --rate 1.3698
```
