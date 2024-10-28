from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'message': 'Lấy các sản phẩm thành công',
            'data': {
                'products': data,
                'pagination': {
                    'page': self.page.number,
                    'limit': self.page.paginator.per_page,
                    'page_size': self.page.paginator.num_pages
                }
            }
        })