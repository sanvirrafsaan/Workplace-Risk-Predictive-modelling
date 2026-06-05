"""Quick smoke test: imports + read one data file."""

from pathlib import Path

import matplotlib
import numpy
import openpyxl
import pandas
import sklearn

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def main() -> None:
    print(f"Python packages OK (pandas {pandas.__version__}, sklearn {sklearn.__version__})")

    sample = sorted(DATA.glob("*_ohs_field_visit.xlsx"))
    if not sample:
        raise SystemExit("No OHS field visit files found in data/")
    path = sample[-1]
    df = pandas.read_excel(path, nrows=5)
    print(f"Read {path.name}: {len(df.columns)} columns, sample shape {df.shape}")

    optional = []
    for name in ("lightgbm", "shap", "seaborn"):
        try:
            __import__(name)
            optional.append(name)
        except (ImportError, OSError) as exc:
            print(f"Optional {name} unavailable: {exc.__class__.__name__}")
    if optional:
        print(f"Optional OK: {', '.join(optional)}")

    matplotlib.use("Agg")
    print("Environment ready.")

if __name__ == "__main__":
    main()
