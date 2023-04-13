from rest_framework.routers import DefaultRouter
from apps.expense_manager.api.views.expends_viewsets import ExpenseViewSet

router = DefaultRouter()

router.register(r'expense', ExpenseViewSet, basename='expense') #registramos la url correspondiente a la viewset 

urlpatterns = router.urls 