"""
DALL-E image generation service for career profession cards.
Images are generated once and cached permanently on disk.
"""

import logging
from pathlib import Path

import httpx

from backend.config import OPENAI_IMAGE_MODEL, OPENAI_IMAGE_SIZE
from backend.services.openai_client import get_openai_client

logger = logging.getLogger(__name__)

# Cache directory for generated images
IMAGES_DIR = Path(__file__).resolve().parent.parent / "cache" / "career_images"


def _image_path(profession_id: str) -> Path:
    return IMAGES_DIR / f"{profession_id}.png"


def has_cached_image(profession_id: str) -> bool:
    """Check whether a cached image already exists for this profession."""
    return _image_path(profession_id).exists()


def get_cached_image_path(profession_id: str) -> Path | None:
    """Return the path to a cached image, or None if it doesn't exist."""
    p = _image_path(profession_id)
    return p if p.exists() else None


async def generate_career_image(profession_id: str, profession_title: str) -> Path:
    """
    Generate a DALL-E image for a profession and save it to disk.
    If already cached, returns the cached path immediately.
    """
    cached = get_cached_image_path(profession_id)
    if cached:
        logger.info("Using cached image for %s", profession_id)
        return cached

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    prompt = (
        f"Professional, modern illustration of a {profession_title} at work. "
        "Clean minimal vector art style, soft ambient lighting, muted corporate "
        "color palette with subtle gradients, no text or words in the image. "
        "The scene should feel aspirational and approachable."
    )

    logger.info("Generating DALL-E image for %s …", profession_id)

    client = get_openai_client()
    response = await client.images.generate(
        model=OPENAI_IMAGE_MODEL,
        prompt=prompt,
        size=OPENAI_IMAGE_SIZE,
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    if not image_url:
        raise RuntimeError(f"DALL-E returned no URL for profession {profession_id}")

    # Download and save
    async with httpx.AsyncClient() as http:
        img_response = await http.get(image_url, timeout=60)
        img_response.raise_for_status()

    dest = _image_path(profession_id)
    dest.write_bytes(img_response.content)
    logger.info("Saved career image: %s (%d bytes)", dest, len(img_response.content))

    return dest
