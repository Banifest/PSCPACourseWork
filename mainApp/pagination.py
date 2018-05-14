from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'limit'
    max_page_size = 100
    # ordering = ('first_name','id','email','username','last_name',)
    #
    # def __init(self, fields: list):
    #     self.ordering = fields
    #     pass
