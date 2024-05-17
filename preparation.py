from typing import List
import os

import sunpy.map
from aiapy.calibrate import normalize_exposure, register, update_pointing
from astropy.io.fits import CompImageHDU
from sunpy.map import Map
from sunpy.coordinates import propagate_with_solar_surface

PATH_TO_NOT_PREPARATED_A94 = "D:\\WangNotPreparated\\A94"
PATH_TO_NOT_PREPARATED_A131 = "D:\\WangNotPreparated\\A131"
PATH_TO_NOT_PREPARATED_A171 = "D:\\WangNotPreparated\\A171"
PATH_TO_NOT_PREPARATED_A193 = "D:\\WangNotPreparated\\A193"
PATH_TO_NOT_PREPARATED_A211 = "D:\\WangNotPreparated\\A211"
PATH_TO_NOT_PREPARATED_A304 = "D:\\WangNotPreparated\\A304"
PATH_TO_NOT_PREPARATED_A335 = "D:\\WangNotPreparated\\A335"

PATH_TO_PREPARATED_A94 = "D:\\WangPreparated\\A94"
PATH_TO_PREPARATED_A131 = "D:\\WangPreparated\\A131"
PATH_TO_PREPARATED_A171 = "D:\\WangPreparated\\A171"
PATH_TO_PREPARATED_A193 = "D:\\WangPreparated\\A193"
PATH_TO_PREPARATED_A211 = "D:\\WangPreparated\\A211"
PATH_TO_PREPARATED_A304 = "D:\\WangPreparated\\A304"
PATH_TO_PREPARATED_A335 = "D:\\WangPreparated\\A335"

def get_paths_to_maps_of_directory(directory: str) -> List[str]:
    filelist = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if "image" in file:
                filelist.append(os.path.join(root,file))
    return filelist

def get_paths_to_save(root:str, paths: List[str]) -> List[str]:
    paths_to_save = list()
    for path in paths:
        parts_of_path = path.split('\\')
        filename = parts_of_path[len(parts_of_path) - 1]
        path_to_save = os.path.join(root, filename)
        paths_to_save.append(path_to_save)
    return paths_to_save

def preparate_map_to_15lvl(map):
    map = update_pointing(map)
    map = register(map)
    map = normalize_exposure(map)
    return map

def preparate_map_seq_to_15lvl(map_seq):
    preparated_seq = list()
    i = 0
    for m in map_seq:
        i += 1
        preparated_map = preparate_map_to_15lvl(m)
        preparated_seq.append(preparated_map)
        print(f"Preporated = {i}/{len(map_seq)}")
    return preparated_seq

def derotate_map(map_to_derotate, reference_map):
    out_wcs = reference_map.wcs

    with propagate_with_solar_surface():
        reprojected_map = map_to_derotate.reproject_to(out_wcs)

    reprojected_map = Map(reprojected_map.data, map_to_derotate.meta)
    return reprojected_map

def derotate_maps(map_seq, reference_map):
    derotated_maps = list()

    i = 0
    for map_to_derotate in map_seq:
        i += 1
        derotated_map = derotate_map(map_to_derotate, reference_map)
        derotated_maps.append(derotated_map)
        print(f"Derotated = {i}/{len(map_seq)}")

    return derotated_maps

def preparate_reference_map(path_to_first_map: str):
    first_map = sunpy.map.Map(path_to_first_map)
    reference_map = preparate_map_to_15lvl(first_map)
    return reference_map

def preparate_range_files(paths_to_not_preporated_maps: List[str],
                          paths_to_save_preporated_maps: List[str],
                          reference_map):
    map_seq = Map(paths_to_not_preporated_maps, sequence=True)
    preparated_seq = preparate_map_seq_to_15lvl(map_seq)
    derotated_map_seq = derotate_maps(preparated_seq, reference_map)
    for i, derotated_map in enumerate(derotated_map_seq):
        path_to_save_derotated_map = paths_to_save_preporated_maps[i]
        if os.path.exists(path_to_save_derotated_map):
            os.remove(path_to_save_derotated_map)
        derotated_map.save(path_to_save_derotated_map, hdu_type=CompImageHDU)


def preparate_files(path_to_not_preparated: List[str],
                    path_to_preparated: List[str],
                    number_of_maps_need_to_preparate: int):
    paths_to_not_preparated_maps = get_paths_to_maps_of_directory(path_to_not_preparated)
    paths_to_save_preparated_maps_sequence = get_paths_to_save(path_to_preparated, paths_to_not_preparated_maps)

    reference_map = preparate_reference_map(paths_to_not_preparated_maps[0])

    if not number_of_maps_need_to_preparate == -1:
        paths_to_not_preparated_maps = paths_to_not_preparated_maps[0: number_of_maps_need_to_preparate]
        paths_to_save_preparated_maps_sequence = paths_to_save_preparated_maps_sequence[0: number_of_maps_need_to_preparate]

    size_of_range_preparate = 10
    number_of_ranges = int(number_of_maps_need_to_preparate / size_of_range_preparate)

    starts_indexes = [size_of_range_preparate * i for i in range(number_of_ranges)]
    finish_indexes = [size_of_range_preparate * (i+1) for i in range(number_of_ranges)]
    for i in range(number_of_ranges):
        start_index = starts_indexes[i]
        finish_index = finish_indexes[i]
        print(f"Обработка диапозона: {start_index} <-> {finish_index}")

        range_paths_of_not_preparated = paths_to_not_preparated_maps[start_index: finish_index]
        range_paths_of_preparated = paths_to_save_preparated_maps_sequence[start_index: finish_index]
        print(range_paths_of_not_preparated)
        preparate_range_files(range_paths_of_not_preparated,
                              range_paths_of_preparated,
                              reference_map)


def preparate_maps_of_channel_A94(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A94, PATH_TO_PREPARATED_A94, number_of_map)

def preparate_maps_of_channel_A131(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A131, PATH_TO_PREPARATED_A131, number_of_map)

def preparate_maps_of_channel_A171(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A171, PATH_TO_PREPARATED_A171, number_of_map)

def preparate_maps_of_channel_A193(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A193, PATH_TO_PREPARATED_A193, number_of_map)

def preparate_maps_of_channel_A211(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A211, PATH_TO_PREPARATED_A211, number_of_map)

def preparate_maps_of_channel_A304(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A304, PATH_TO_PREPARATED_A304, number_of_map)

def preparate_maps_of_channel_A335(number_of_map = -1):
    preparate_files(PATH_TO_NOT_PREPARATED_A335, PATH_TO_PREPARATED_A335, number_of_map)

if __name__ == "__main__":
    preparate_maps_of_channel_A335(300)
