from django.db.models import Avg
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Book
from .serializers import *
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

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


# Представление для списка и создания объектов
class BookListCreateView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    # pagination_class = BookPagination # Использование класса пагинации 1 способ
    # pagination_class = LimitOffsetPagination # Использование класса пагинации 2 способ
    pagination_class = BookCursorPagination  # Использование класса пагинации CursorPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'publisher', 'is_bestseller'] # Поля для фильтрации
    search_fields = ['title', 'author'] # Поля для поиска
    ordering_fields = ['published_date', 'price'] # Поля для сортировки

    # Добавление кастомной логики перед сохранением
    def create(self, request, *args, **kwargs):
        # Получение данных из запроса
        data = request.data.copy()
        # Кастомная логика: Установка значения по умолчанию для автора, если не указан
        if 'author' not in data or not data['author']:
            data['author'] = 'Unknown Author'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['include_related'] = self.request.query_params.get('include_related', 'false').lower() == 'true'
        return context


class ExpensiveBooksView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def list(self, request, *args, **kwargs):
        # Вычисление средней цены
        average_price = Book.objects.aggregate(average_price=Avg('price'))['average_price']
        # Получение книг с ценой выше средней
        queryset = Book.objects.filter(price__gt=average_price)
        # Сериализация данных
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# Представление для получения, обновления и удаления конкретного объекта
class BookDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Переопределение метода для добавления кастомной логики - создали доп поле is_discounted
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

    # Добавление поля к ответу, проверяющего, что цена со скидкой меньше цены
        if response.data.get('discounted_price') is not None and response.data.get('price') is not None:
            response.data['is_discounted'] = response.data['discounted_price'] < response.data['price']
        else:
            response.data['is_discounted'] = False
        return response

    # Добавление кастомной проверки перед обновлением
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) # обновить все или часть объекта
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Пример проверки: цена книги не должна быть ниже минимальной
        if serializer.validated_data.get('price', instance.price) < 5.00:
            return Response({'error': 'Price cannot be less than 5.00'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)

    # Добавление кастомной логики при удалении объекта
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        self.perform_destroy(instance)
    # Пример кастомной логики: логирование успешного удаления
        print(f"Book deleted: {instance}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Переопределение метода, добавление записи, которая не показывается пользователю
    def get_object(self):
        # Получение параметра pk из URL
        pk = self.kwargs.get('pk')
        # Попытка найти объект по pk, исключая запрещенные
        try:
            book = self.queryset.get(pk=pk, is_banned=False)
        except Book.DoesNotExist:
            # Обработка ошибки, если объект не найден или запрещен
            raise NotFound(detail=f"Book with id '{pk}' not found or is banned.")
        return book


class GenreListCreateView(ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'name' # Указывает использовать поле 'name' для поиска
    lookup_url_kwarg = 'genre_name' # Указывает параметр URL 'genre_name' для получения значения

# class BookListCreateView(GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         books = self.get_queryset()
#         serializer = self.get_serializer(books, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class BookDetailUpdateDeleteView(GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#
#     def get(self, request, *args, **kwargs):
#         book = self.get_object()
#         serializer = self.get_serializer(book)
#         return Response(serializer.data)
#
#     def put(self, request, *args, **kwargs):
#         book = self.get_object()
#         serializer = self.get_serializer(book, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def patch(self, request, *args, **kwargs):
#         book = self.get_object()
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# https://127.0.0.1:8000/books/?author=John&published_year=2023

# @api_view(['POST'])
# def create_genre(request):
#     serializer = GenreSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response


# @api_view(['GET', 'POST'])
# def book_list_create(request):
#     if request.method == 'GET':
#         books = Book.objects.all()
#         serializer = BookListSerializer(books, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'POST':
#         serializer = BookCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail_update_delete(request, pk):
#     try:
#         book = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = BookDetailSerializer(book)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     elif request.method == 'PUT':
#         serializer = BookCreateSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         book.delete()
#         return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
#
