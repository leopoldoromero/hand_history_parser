from typing import Dict, Any, Tuple
from app.shared.domain.criteria import Criteria, CriteriaOperators, CriteriaOrderTypes


def criteria_to_mongo_query(
    criteria: Criteria,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    query = {}
    sort_options = []

    operator_map = {
        CriteriaOperators.EQUAL: "$eq",
        CriteriaOperators.NOT_EQUAL: "$ne",
        CriteriaOperators.GT: "$gt",
        CriteriaOperators.LT: "$lt",
        CriteriaOperators.GT_EQUAL: "$gte",
        CriteriaOperators.LT_EQUAL: "$lte",
        CriteriaOperators.CONTAINS: "$regex",
        CriteriaOperators.NOT_CONTAINS: "$not",
        CriteriaOperators.LIKE: "$regex",
    }

    for filter_obj in criteria.filters:
        field = filter_obj.field
        value = filter_obj.value
        operator = operator_map.get(filter_obj.operator, "$eq")

        if filter_obj.operator in {CriteriaOperators.CONTAINS, CriteriaOperators.LIKE}:
            value = f".*{value}.*"

        query[field] = {operator: value}

    if criteria.order:
        order_field = criteria.order.order_by
        order_type = 1 if criteria.order.order_type == CriteriaOrderTypes.ASC else -1
        sort_options.append((order_field, order_type))

    options = {
        "sort": sort_options if sort_options else None,
        "skip": (criteria.page - 1) * criteria.limit
        if criteria.page and criteria.limit
        else 0,
        "limit": criteria.limit if criteria.limit else 0,
    }

    return query, options
