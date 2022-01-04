from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param
from .models import Equipment

class EquipmentPagination(PageNumberPagination):
    page_size=Equipment.EQUIPMENT_PER_PAGE
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'current': self.request.build_absolute_uri(),
                'first': self.get_first_link(),
                'last': self.get_last_link(),
            },
            'current_page': self.page.number,
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'per_page': self.page.paginator.per_page,
            'results': data,
        })

    def get_first_link(self):
        url = self.request.build_absolute_uri()
        page_number = 1
        return replace_query_param(url, self.page_query_param, page_number)

    def get_last_link(self):
        url = self.request.build_absolute_uri()
        page_number = self.page.paginator.num_pages
        return replace_query_param(url, self.page_query_param, page_number)