from urllib.parse import quote, unquote

def normalize_url(hostname_and_port: str, original_path_and_query_string: str) -> str:
    hostname_and_port = hostname_and_port.lower()
    path_query = unquote(original_path_and_query_string)
    # Remove dangerous ../
    while '/../' in path_query:
        path_query = path_query.replace('/../', '/')
    # Re-encode
    path_query = quote(path_query, safe="/?&=%")
    return f"http://{hostname_and_port}{path_query if path_query.startswith('/') else '/' + path_query}"
