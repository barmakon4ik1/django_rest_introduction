from django.urls import path, include, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import GenreListRetrieveUpdateViewSet
from .views import *
from newapp.views import *


# В Django REST Framework, Router используется для автоматического создания
# URL՞маршрутов для ваших ViewSet. Это удобный инструмент, который упрощает
# настройку маршрутизации и обеспечивает автоматическое сопоставление
# стандартных CRUD операций с соответствующими HTTP методами и URL

# Виды ViewSets
# 1. DefaultRouter: Предоставляет стандартный набор маршрутов и добавляет
# маршрут для страницы API корня.
# 2. SimpleRouter: Похож на DefaultRouter, но не добавляет маршрут для страницы
# API корня.
router = DefaultRouter()

router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)
# router.register(r'genres', GenreListRetrieveUpdateViewSet)
# router.register(r'genres', GenreReadOnlyViewSet)

urlpatterns = [

    # BasicAuthentication / TokenAuthentication
    path('protected/', ProtectedDataView.as_view(), name='protected-data'),
    # path('api-tocken-auth/', obtain_auth_token, name='api-tocken-auth'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Simple JWT:
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', ReadOnlyOrAuthenticatedView.as_view(), name='admin'),



    re_path(r'^books/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', books_by_date_view, name='books-by-date'),
    path('user-book/', UserBookListView.as_view(), name='user-book'),
    # path('books/', BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-detail-update-delete'),
    # path('books/expensive/', ExpensiveBooksView.as_view(), name='book-expensive'),
    path('', include(router.urls)), # # Включение маршрутов, созданных роутером
    # path('books/', BookListView.as_view(), name='book-list-create'),  # Для получения всех книг и создания новой книги
    # path('books/<int:pk>/', BookDetailUpdateDeleteView.as_view(), name='book-detail-update-delete'),
    # Для операций с одной книгой



   ]





