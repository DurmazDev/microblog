from app.config import SECRET_KEY
import math
import jwt


def create_token(data: object):
    """
    Signs data with JWT.

    Parameters
    ---------
    data: Object

    Returns
    ---------
    string
        JWT signed token.
    """
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def paginate_query(query, page: int, limit: int, schema, sort: [str] = []):
    """
    Paginates a query and returns results along with pagination information.

    Parameters
    ----------
    query: QuerySet
        The query to paginate.
    page: int
        Current page number.
    limit: int
        Number of items per page.
    schema: Schema
        Schematic of the query model.
    sort: List[String] -> Example: ["-created_at", "vote"]


    Returns
    -------
    dict
        Paginated results with pagination information.
    """
    page = 1 if page < 1 else page
    limit = 50 if limit < 1 else limit
    # WARN(ahmet): If page greater than total_page we should not run the query
    offset = (page - 1) * limit
    results = query.skip(offset).limit(limit)

    if sort:
        results = results.order_by(*sort)

    result_count = query.count()

    if result_count == 0:
        return {"error": "No results found."}, 404

    results = schema.dump(results, many=True)
    total_pages = math.ceil(result_count / limit)

    return {
        "results": results,
        "pagination": {
            "current_page": page,
            "next_page": None if page == total_pages else page + 1,
            "prev_page": None if page == 1 else page - 1,
            "total_count": result_count,
            "total_pages": total_pages,
        },
    }, 200
