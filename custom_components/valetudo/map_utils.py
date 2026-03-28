import struct
import zlib
import json
import logging

_LOGGER = logging.getLogger(__name__)


def extract_map_from_image(image_data: bytes) -> dict | None:
    # Valid PNG Header: 89 50 4E 47 0D 0A 1A 0A
    if image_data[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError("Invalid PNG file header")

    idx = 8
    length = len(image_data)
    map_json = None

    while idx < length:
        # Read Length (4 bytes, Big Endian)
        if idx + 4 > length:
            break
        chunk_length = struct.unpack(">I", image_data[idx:idx + 4])[0]
        idx += 4

        # Read Type (4 bytes)
        chunk_type_bytes = image_data[idx:idx + 4]
        try:
            chunk_type = chunk_type_bytes.decode('ascii')
        except UnicodeDecodeError:
            chunk_type = "UNKNOWN"
        idx += 4

        if chunk_type == "IEND":
            break

        # Data starts at idx, ends at idx + chunk_length
        if chunk_type == "zTXt":
            # The zTXt chunk data structure:
            # Keyword (1-79 bytes) + Null Separator (1 byte) + Compression Method (1 byte) + Compressed Data

            chunk_data = image_data[idx: idx + chunk_length]

            # Find the null separator
            try:
                null_index = chunk_data.index(b'\x00')
                # Keyword is latin-1 encoded according to PNG spec
                keyword = chunk_data[:null_index].decode('latin-1')

                if keyword == "ValetudoMap":
                    # Skip Keyword (n) + Null (1) + Compression Method (1)
                    # The data starts at null_index + 2
                    compressed_payload = chunk_data[null_index + 2:]

                    try:
                        decompressed = zlib.decompress(compressed_payload)
                        map_json = json.loads(decompressed)
                    except Exception as e:
                        _LOGGER.error(f"Failed to decompress/parse ValetudoMap: {e}")
                        raise e
            except ValueError:
                pass  # No null byte found, malformed zTXt

        # Move index past data
        idx += chunk_length

        # Skip CRC (4 bytes)
        idx += 4

        if map_json:
            # Found it, we can stop parsing
            break

    return map_json


def unpack_pixels(data: dict) -> dict:
    meta_data = data.get("metaData")
    layers = data.get("layers")

    if meta_data and meta_data.get("version") == 2 and isinstance(layers, list):
        for layer in layers:
            pixels = layer.get("pixels", [])
            compressed_pixels = layer.get("compressedPixels", [])

            if len(pixels) == 0 and len(compressed_pixels) > 0:
                new_pixels = []

                # compressedPixels structure: [xStart, y, count, xStart, y, count, ...]
                # Iterate by 3
                for k in range(0, len(compressed_pixels), 3):
                    x_start = compressed_pixels[k]
                    y = compressed_pixels[k + 1]
                    count = compressed_pixels[k + 2]

                    for j in range(count):
                        new_pixels.extend((x_start + j, y))

                layer["pixels"] = new_pixels

                if "compressedPixels" in layer:
                    del layer["compressedPixels"]

    return data


def extract_and_parse_map(image_data: bytes) -> dict | None:
    data = extract_map_from_image(image_data)
    if data:
        return unpack_pixels(data)
    return None


def approximate_segment(map_data: dict) -> dict | None:
    pixel_size = map_data.get("pixelSize", 5)

    robot_pos = None
    entities = map_data.get("entities") or []
    for entity in entities:
        if entity.get("type") == "robot_position":
            points = entity.get("points", [])
            if len(points) >= 2:
                robot_pos = (int(points[0] // pixel_size), int(points[1] // pixel_size))
            break

    if not robot_pos:
        return None

    rx, ry = robot_pos
    layers = map_data.get("layers") or []

    # -------------------------------------------------------------------------
    # PASS 1: Calculate Bounding Box distance for all segments
    # -------------------------------------------------------------------------
    candidates = []

    for layer in layers:
        if layer.get("type") != "segment":
            continue

        aabb_dist_sq = 0
        dimensions = layer.get("dimensions")

        # Calculate distance to Bounding Box
        if dimensions and "x" in dimensions and "y" in dimensions:
            min_x = dimensions["x"]["min"]
            max_x = dimensions["x"]["max"]
            min_y = dimensions["y"]["min"]
            max_y = dimensions["y"]["max"]

            dx = 0
            if rx < min_x:
                dx = min_x - rx
            elif rx > max_x:
                dx = rx - max_x

            dy = 0
            if ry < min_y:
                dy = min_y - ry
            elif ry > max_y:
                dy = ry - max_y

            aabb_dist_sq = (dx * dx) + (dy * dy)
        else:
            # Fallback if dimensions missing: treat as distance 0 to force pixel check
            aabb_dist_sq = 0

        candidates.append((aabb_dist_sq, layer))

    # Sort candidates by AABB distance (ascending)
    # This ensures we check the most likely segments first
    candidates.sort(key=lambda x: x[0])

    # -------------------------------------------------------------------------
    # PASS 2: Find exact pixel match
    # -------------------------------------------------------------------------
    closest_segment_info = None
    min_dist_sq = float('inf')

    for aabb_dist_sq, layer in candidates:
        # Since the list is sorted by AABB distance, if the theoretical minimum distance
        # to this segment (AABB) is already larger than the actual pixel distance
        # we found in a previous candidate, we can stop immediately.
        if aabb_dist_sq >= min_dist_sq:
            break

        pixels = layer.get("pixels", [])

        for i in range(0, len(pixels), 2):
            px = pixels[i]
            py = pixels[i + 1]

            dx = px - rx
            dy = py - ry

            dist_sq = (dx * dx) + (dy * dy)
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq

                meta = layer.get("metaData", {})
                closest_segment_info = {
                    "id": meta.get("segmentId"),
                    "name": meta.get("name")
                }

                # If distance is 0, we are exactly on a pixel of this segment.
                # We can't get better than 0.
                if min_dist_sq == 0:
                    return closest_segment_info

    return closest_segment_info
