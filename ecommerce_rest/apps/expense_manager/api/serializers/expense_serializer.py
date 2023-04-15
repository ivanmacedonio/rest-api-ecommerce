from rest_framework import serializers
from apps.expense_manager.models import *


class SupplierRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier

        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:

        model = Expense

        exclude = ('state', 'created_date', 'modified_date', 'deleted_date')
        