from typing import Any, Dict


def success_response(
        data: Any = None, message: str = "Success") -> Dict[str, Any]:
    response = {"message": message}
    if data is not None:
        if isinstance(data, dict):
            response.update(data)
        else:
            response["data"] = data
    return response


def paginated_response(items: list, total: int, page: int,
                       page_size: int) -> Dict[str, Any]:
    pages = max(1, (total + page_size - 1) // page_size)
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages
    }
