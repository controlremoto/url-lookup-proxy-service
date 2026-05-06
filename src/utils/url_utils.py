from urllib.parse import quote, unquote
from src.utils.logger import get_logger
from src.config.constants import LOGGER_NAME

logger = get_logger(LOGGER_NAME)


"""
Returns True if the constructed URL exceeds max_length.
"""

def is_url_too_long(norm_host: str, norm_path_query: str, max_length: int) -> bool:
    normalized_url = f"http://{norm_host}{norm_path_query if norm_path_query.startswith('/') else '/' + norm_path_query}"
    return len(normalized_url) > max_length

"""
Normalize the hostname_and_port and original_path_and_query_string for consistent DB lookup.
Returns a tuple: (normalized_hostname_and_port, normalized_path_and_query_string)
- Lowercases the host/port
- Unquotes, sanitizes, and re-encodes the path/query
"""

def normalize_url(hostname_and_port: str, original_path_and_query_string: str) -> tuple[str, str]:
    normalized_host = hostname_and_port.lower()
    path_query = unquote(original_path_and_query_string)
    while '/../' in path_query:
        path_query = path_query.replace('/../', '/')
    normalized_path_query = quote(path_query, safe="/?&=%")
    logger.info(f"Normalized URL: original=({normalized_host}, {original_path_and_query_string}) -> ({normalized_host}, {normalized_path_query})")
    return normalized_host, normalized_path_query
