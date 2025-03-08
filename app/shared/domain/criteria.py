from typing import List, Optional
from enum import Enum


class CriteriaOperators(Enum):
    EQUAL = "EQUAL"
    NOT_EQUAL = "NOT_EQUAL"
    GT = "GT"
    LT = "LT"
    GT_EQUAL = "GT_EQUAL"
    LT_EQUAL = "LT_EQUAL"
    CONTAINS = "CONTAINS"
    NOT_CONTAINS = "NOT_CONTAINS"
    LIKE = "LIKE"


class CriteriaOrderTypes(Enum):
    ASC = "ASC"
    DESC = "DESC"
    NONE = "NONE"


class CriteriaOrder:
    def __init__(self, order_by: str, order_type: Optional[CriteriaOrderTypes]) -> None:
        self.order_by = order_by
        self.order_type = order_type if order_type else CriteriaOrderTypes.ASC


class CriteriaFilter:
    def __init__(self, field: str, value, operator: CriteriaOperators) -> None:
        self.field = field
        self.value = value
        self.operator = operator if operator else CriteriaOperators.EQUAL


class Criteria:
    def __init__(
        self,
        filters: List[CriteriaFilter],
        order: Optional[CriteriaOrder] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> None:
        self.filters = filters
        self.order = order
        self.page = page
        self.limit = limit
