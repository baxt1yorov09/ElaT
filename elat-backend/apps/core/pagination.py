"""Cursor pagination, 20 items per page (SPEC §13, §18.9)."""

from __future__ import annotations

from rest_framework.pagination import CursorPagination as DRFCursorPagination


class CursorPagination(DRFCursorPagination):
    page_size = 20
    max_page_size = 50
    page_size_query_param = "page_size"
    ordering = "-created_at"
    cursor_query_param = "cursor"
