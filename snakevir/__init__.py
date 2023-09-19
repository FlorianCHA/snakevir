from pathlib import Path
__version__ = Path(__file__).parent.resolve().joinpath("VERSION").open("r").readline().strip()

__doc__ = """
This is a worflow that analyses some metagenomics data
"""
