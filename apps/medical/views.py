from rest_framework import viewsets,filters,generics,status,mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import *

class Pagination(PageNumberPagination):
    '''
    自定义分页
    '''
    #默认每页显示的个数
    page_size = 10
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #页码参数
    page_query_param = 'page'
    #最多能显示多少页
    max_page_size = 100

# class ProvinceViewSet(CacheResponseMixin ,mixins.ListModelMixin, viewsets.GenericViewSet):
#     """返回省份数据"""
#     queryset = Areas.objects.filter(area_parent=None) # 过滤查询,返回父级为空的数据
#     serializer_class = ProvinceSerializer
#     pagination_class = Pagination  # 自定义分页类
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)  # 过滤搜索排序
#     search_fields = ('area_id', 'area_name')  # =表示精准搜索
#     ordering_fields = ('area_id',)  # 时间排序
#
# class AreasViewSet(CacheResponseMixin ,mixins.ListModelMixin, viewsets.GenericViewSet):
#     """返回市、区镇数据"""
#     serializer_class = AreasSerializer
#     search_fields = ('area_id', 'area_name')  # =表示精准搜索
#     ordering_fields = ('area_id',)  # 时间排序
#     def get_queryset(self):
#         """
#         因为需要使用参数,所以构造一个方法
#         :return:
#         """
#         area_parent = self.kwargs["area_parent"]
#         return Areas.objects.filter(area_parent__pk=area_parent)

class AreasViewSet(viewsets.ReadOnlyModelViewSet):
    """
    行政区划信息
    """
    pagination_class = None  # 区划信息不分页

    def get_queryset(self):
        """
        提供数据集
        """
        if self.action == 'list':
            return Areas.objects.filter(area_parent=None)
        else:
            return Areas.objects.all()

    def get_serializer_class(self):
        """
        提供序列化器
        """
        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer

class HospitalViewSet(viewsets.ReadOnlyModelViewSet):
    '''
        查看医院详情
        list:
            获得医院列表
    '''
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    pagination_class = Pagination # 自定义分页
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 过滤 搜索 排序
    ordering_fields = ('hospital_province', )
    search_fields = ('hospital_name', 'hospital_province', 'hospital_city',
                     'hospital_district', 'hospital_tel', 'hospital_email')

class DiagnosisViewSet(CacheResponseMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       viewsets.GenericViewSet):

    '''
        create:
            上传一张图片，返回诊断结果,request中需要包含user(即userid)
        retrieve:
            展示当前用户诊断结果详情
            URL请求包含主键id，主键id，用户user,诊断图片image,诊断时间addtime
        list:
            展示当前用户所有诊断案例
            返回主键id，用户user,诊断图片image,诊断时间resltime
    '''
    serializer_class = DiagnosisSerializer
    queryset = Diagnosis.objects.all() #.order_by('diagnosis_id') # 必须加排序规则否则报错
    pagination_class = Pagination # 自定义分页类
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter) # 过滤搜索排序


    # # 设置filter的类为我们自定义的类
    # filter_class = GoodsFilter
    # filters_fields = ('diagnosis_prop') # 过滤诊断结果
    search_fields = ('diagnosis_id','diagnosis_prop','diagnosis_title') # =表示精准搜索
    ordering_fields = ('diagnosis_addtime', ) # 时间排序
    # lookup_field = None
    # lookup_field = 'user_id'
    # lookup_url_kwarg = ['id','user_id']
    permission_classes = (IsAuthenticated,)
    # 动态修改序列化类
    def get_serializer_class(self):
        if self.action == 'create':
            return DiagnosisCreateSerializer
        return DiagnosisSerializer

    def get_queryset(self):
        return Diagnosis.objects.filter(user=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'create':
    #             return [permissions.IsAuthenticated(),]
    #     return  [permissions.IsAuthenticated(), IsOwner()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        #print(serializer.data) # 显示一个字典{'id': 10, 'prop': 'yyy', 'image': 'http://127.0.0.1:8000/media/results/images/3_VfNyfYz.jpg', 'resltime': '2018-10-25T10:48:11.419092+08:00'}
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()