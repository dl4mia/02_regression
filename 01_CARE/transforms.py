import numpy as np
from typing import Tuple


def normalize(
    image: np.ndarray,
    mean: float = 0.0,
    std: float = 1.0,
) -> np.ndarray:
    """
    Normalize an image with given mean and standard deviation.

    Parameters
    ----------
    image : np.ndarray
        Array containing single image or patch, 2D or 3D.
    mean : float, optional
        Mean value for normalization, by default 0.0.
    std : float, optional
        Standard deviation value for normalization, by default 1.0.

    Returns
    -------
    np.ndarray
        Normalized array.
    """
    return (image - mean) / std


def denormalize(
    image: np.ndarray,
    mean: float = 0.0,
    std: float = 1.0,
) -> np.ndarray:
    """
    Denormalize an image with given mean and standard deviation.

    Parameters
    ----------
    image : np.ndarray
        Array containing single image or patch, 2D or 3D.
    mean : float, optional
        Mean value for normalization, by default 0.0.
    std : float, optional
        Standard deviation value for normalization, by default 1.0.

    Returns
    -------
    np.ndarray
        Denormalized array.
    """
    return image * std + mean


def _flip_and_rotate(
    image: np.ndarray, rotate_state: int, flip_state: int
) -> np.ndarray:
    """
    Apply the given number of 90 degrees rotations and flip to an array.

    Parameters
    ----------
    image : np.ndarray
        Array containing single image or patch, 2D or 3D.
    rotate_state : int
        Number of 90 degree rotations to apply.
    flip_state : int
        0 or 1, whether to flip the array or not.

    Returns
    -------
    np.ndarray
        Flipped and rotated array.
    """
    rotated = np.rot90(image, k=rotate_state, axes=(-2, -1))
    flipped = np.flip(rotated, axis=-1) if flip_state == 1 else rotated
    return flipped.copy()


def augment_batch(
    patch: np.ndarray,
    target: np.ndarray,
    seed: int = 42,
) -> Tuple[np.ndarray, ...]:
    """
    Apply augmentation function to patches and masks.

    Parameters
    ----------
    patch : np.ndarray
        Array containing single image or patch, 2D or 3D with masked pixels.
    original_image : np.ndarray
        Array containing original image or patch, 2D or 3D.
    mask : np.ndarray
        Array containing only masked pixels, 2D or 3D.
    seed : int, optional
        Seed for random number generator, controls the rotation and falipping.

    Returns
    -------
    Tuple[np.ndarray, ...]
        Tuple of augmented arrays.
    """
    rng = np.random.default_rng(seed=seed)
    rotate_state = rng.integers(0, 4)
    flip_state = rng.integers(0, 2)
    return (
        _flip_and_rotate(patch, rotate_state, flip_state),
        _flip_and_rotate(target, rotate_state, flip_state),
    )
