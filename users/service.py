from django.core.paginator import Paginator

from .constants import PAGINATE_BY


def paginate_queryset(queryset, page):
    paginator = Paginator(queryset, PAGINATE_BY)
    return paginator.get_page(page)
