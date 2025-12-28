"""Entry point script to run the application with correct Python path."""

import sys
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Now import and run main
if __name__ == "__main__":
    from main import main
    import asyncio

    asyncio.run(main())
