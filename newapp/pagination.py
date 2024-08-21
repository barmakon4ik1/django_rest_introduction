from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


# class CustomPagination(PageNumberPagination):
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,
#             'page': self.page.number,
#             'previous': None if not self.page.has_previous() else self.page.previous_page_number(),
#             'next': None if not self.page.has_next() else self.page.next_page_number(),
#             'previous_link': self.get_previous_link(),
#             'next_link': self.get_next_link(),
#             'results': data
#         })


# Различные виды пагинаций:
# class BookPagination(PageNumberPagination): # Использование класса пагинации 1 способ
#     page_size = 3 # Количество элементов на странице
#     page_size_query_param = 'page_size'
#     max_page_size = 100

# class BookListView(ListAPIView): # Использование класса пагинации 2 способ
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     pagination_class = LimitOffsetPagination # Использование класса  пагинации


""" CursorPagination — это один из типов пагинации в Django REST Framework ՄDRFՅ,
который обеспечивает стабильную и безопасную навигацию по страницам данных. В
отличие от других методов пагинации, CursorPagination использует курсоры для
определения положения в наборе данных, что особенно полезно при работе с
динамически изменяющимися данными."""


class BookCursorPagination(CursorPagination):
    page_size = 3
    ordering = 'published_date' # Поле для курсора