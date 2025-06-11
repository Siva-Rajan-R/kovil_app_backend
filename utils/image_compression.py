from PIL import Image
import io

def compress_image_to_target_size(image_binary: bytes, target_size_bytes=5 * 1024 * 1024, min_quality=60) -> bytes:
    image = Image.open(io.BytesIO(image_binary))

    # Convert to RGB to avoid format issues (like PNG with alpha)
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    quality = 95
    step = 5

    while quality >= min_quality:
        buffer = io.BytesIO()
        image.save(buffer, format="WEBP", optimize=True, quality=quality)
        size = buffer.tell()
        
        if size <= target_size_bytes:
            buffer.seek(0)
            return buffer.read()
        
        quality -= step

    # Fallback: resize if still too big
    width, height = image.size
    while size > target_size_bytes and width > 200:
        width = int(width * 0.9)
        height = int(height * 0.9)
        image = image.resize((width, height), Image.LANCZOS)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", optimize=True, quality=quality)
        size = buffer.tell()

    buffer.seek(0)
    
    return buffer.read()