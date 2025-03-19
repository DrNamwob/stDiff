import numpy as np
from sklearn.metrics.pairwise import euclidean_distances

def compute_spatial_affinity_matrix(spatial_coords, k=10):
    """
    Computes an affinity matrix based on spatial coordinates using a Gaussian kernel.

    Parameters:
        spatial_coords (ndarray): Array of shape (n_cells, 2) with x, y coordinates.
        k (int): Number of nearest neighbors to determine the adaptive kernel width.

    Returns:
        affinity_matrix (ndarray): Symmetric affinity matrix of shape (n_cells, n_cells).
    """
    # Step 1: Compute pairwise Euclidean distances
    distances = euclidean_distances(spatial_coords, spatial_coords)
    
    # Step 2: Determine adaptive sigma for each cell
    sorted_distances = np.sort(distances, axis=1)
    sigmas = np.mean(sorted_distances[:, 1:k+1], axis=1)  # Exclude distance to self
    
    # Step 3: Compute Gaussian kernel affinities
    affinity_matrix = np.exp(-distances**2 / (2 * sigmas[:, None]**2))
    
    return affinity_matrix

# Example usage
# Assuming spatial coordinates are in adata.obsm['X_spatial']
spatial_coords = adata.obsm['X_spatial']  # Shape (n_cells, 2)
affinity_matrix = compute_spatial_affinity_matrix(spatial_coords, k=10)
