from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]   # …/pythonProject2
if str(ROOT) not in sys.path:                # дубли не нужн
    sys.path.insert(0, str(ROOT))
