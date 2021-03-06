from cts_core import camera as cam
import numpy as np
import astropy.units as u
from ctapipe.instrument.camera import CameraGeometry
from ctapipe.instrument.camera import _find_neighbor_pixels as find_neighbor_pixels


def find_pixel_positions(camera_config_file, source_x=0.*u.mm, source_y=0.*u.mm):
    camera = cam.Camera(_config_file=camera_config_file)

    x, y = [], []

    for pixel in camera.Pixels:

        x.append(pixel.center[0])
        y.append(pixel.center[1])

    r = np.array([x, y]) * u.mm
    r[0] = r[0] - source_x
    r[1] = r[1] - source_y

    return r


def generate_geometry_from_camera(camera, source_x=0.*u.mm, source_y=0.*u.mm):
    """
    Generate the SST-1M geometry from the CTS configuration
    :param cts: a CTS instance
    :param available_board:  which board per sector are available (dict)
    :return: the geometry for visualisation and the list of "good" pixels
    """
    pix_x = []
    pix_y = []
    pix_id = []

    for pix in camera.Pixels:
        pix_x.append(pix.center[0])
        pix_y.append(pix.center[1])
        pix_id.append(pix.ID)

    neighbors_pix = find_neighbor_pixels(pix_x, pix_y, 30.)
    geom = CameraGeometry(0, pix_id, pix_x * u.mm - source_x, pix_y * u.mm - source_y, np.ones(1296) * 400., pix_type='hexagonal',
                          neighbors=neighbors_pix)

    return geom


def compute_patch_matrix(camera):

    n_pixels = len(camera.Pixels)
    n_patches = len(camera.Patches)
    patch_matrix = np.zeros((n_patches, n_pixels), dtype=int)

    for patch in camera.Patches:

        for pixel in patch.pixelsID:

            patch_matrix[patch.ID, pixel] = 1

    return patch_matrix


def compute_cluster_matrix_7(camera):

    n_clusters = len(camera.Clusters_7)
    cluster_matrix = np.zeros((n_clusters, n_clusters), dtype=int)

    for cluster in camera.Clusters_7:

        for patch in cluster.patchesID:
            cluster_matrix[cluster.ID, patch] = 1

    return cluster_matrix


def compute_cluster_matrix_19(camera):

    n_clusters = len(camera.Clusters_19)
    cluster_matrix = np.zeros((n_clusters, n_clusters), dtype=int)

    for cluster in camera.Clusters_19:

        for patch in cluster.patchesID:
            cluster_matrix[cluster.ID, patch] = 1

    return cluster_matrix
