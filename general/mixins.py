from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PaginationMixin(object):
    PER_PAGE = 10
    
    def paginate(self, obj_list):
        page = self.request.GET.get('page', 1)
        per_page = self.request.GET.get('per-page', self.PER_PAGE)
        paginator = Paginator(obj_list, per_page)
        try:
            paginated = paginator.page(page)
        except PageNotAnInteger:
            paginated = paginator.page(1)
        except EmptyPage:
            paginated = paginator.page(paginator.num_pages)
        return paginated
        
