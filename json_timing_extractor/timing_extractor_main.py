import json
import json_timing_extractor

def main():
    with open('/home/chem3000/Programs/prjxray/database/artix7/tile_type_INT_L.json', 'r') as INT_L:
        data = json.load(INT_L)