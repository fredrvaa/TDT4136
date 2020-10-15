import argparse

from map_obj import MapObj
from visualizer import Visualizer

parser = argparse.ArgumentParser()
parser.add_argument("--cell_size", type=int, default=16)
args = parser.parse_args()

Visualizer(cell_size = args.cell_size)
