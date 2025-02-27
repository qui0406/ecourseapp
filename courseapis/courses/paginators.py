from rest_framework.pagination import PageNumberPagination # type: ignore


class CoursePaginator(PageNumberPagination):
    page_size = 1
    