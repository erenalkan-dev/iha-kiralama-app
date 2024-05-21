from rest_framework import viewsets
from .models import User, UAV, Rent,Model, Brand, Category
from .serializers import UserSerializer, UAVSerializer,RentSerializer,ModelSerializer,BrandSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes as pc, api_view
from .permissions import IsAuthenticatedForNonPost,IsAuthenticatedForNonGet
from django.db.models import Q
from datetime import datetime
from rest_framework.pagination import LimitOffsetPagination
from django.core.files.storage import default_storage

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedForNonPost]

class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    

    serializer_class = UAVSerializer
    permission_classes = [IsAuthenticatedForNonGet]

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.id
        return super().create(request, *args, **kwargs)

    # override to add filtering options to rent
    def list(self, request, *args, **kwargs):
        query_params = request.GET
        start_time_param = query_params.get("start_date",None )
        end_time_param = query_params.get("end_date",None )
        only_owneds_param = query_params.get("only_owneds", "false" )

        

        start_time = datetime.strptime(start_time_param, '%Y-%m-%dT%H:%M') if start_time_param else None
        end_time = datetime.strptime(end_time_param, '%Y-%m-%dT%H:%M') if end_time_param else None
        user_id = request.user.id

        if start_time and end_time:
            if user_id and only_owneds_param == "true":
                rent_list = Rent.objects.filter(Q(start_time__lte=end_time, end_time__gte=start_time)).values_list('uav_id', flat=True)
                uav_list = UAV.objects.filter(owner=user_id)
                uav_list= uav_list.exclude(id__in=rent_list)
            else:
                rent_list = Rent.objects.filter(Q(start_time__lte=end_time, end_time__gte=start_time)).values_list('uav_id', flat=True)
                uav_list = UAV.objects.all()
                uav_list= uav_list.exclude(id__in=rent_list)
        else:
            if user_id and only_owneds_param:
                uav_list = UAV.objects.filter(owner=user_id)
            else:
                uav_list = UAV.objects.all()
        
        # Paginate the queryset
        paginator = LimitOffsetPagination()
        paginated_uav_list = paginator.paginate_queryset(uav_list, request)

        serializer = UAVSerializer(paginated_uav_list, many=True)
        for e in serializer.data:
            model_data = Model.objects.filter(id=e["model"]).first()
            category_data = Category.objects.filter(id=e["category"]).first()
            owner_data = User.objects.filter(id=e["owner"]).first()
            e["model"] = model_data.name
            e["brand"] = model_data.brand.name
            e["category"] = category_data.name
            e["owner_username"] = owner_data.username
            if user_id:
                e["owned"] = int(user_id) == e["owner"]
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        uav = UAV.objects.filter(id=self.get_object().id)
        serializer = UAVSerializer(uav, many=True)

        for e in serializer.data:
            model_data = Model.objects.filter(id=e["model"]).first()
            category_data = Category.objects.filter(id=e["category"]).first()
            e["model"] = model_data.name
            e["brand"] = model_data.brand.name
            e["category"] = category_data.name
        return Response(serializer.data)
    

class RentViewSet(viewsets.ModelViewSet):
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    permission_classes = [IsAuthenticatedForNonGet]

    # override to add filtering options to rent
    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        if user_id:
            rent_list = Rent.objects.filter(user=user_id)
        else:
            rent_list = Rent.objects.all()
        serializer = RentSerializer(rent_list, many=True)

        for e in serializer.data:
            user_data = User.objects.filter(id=e["user"]).first()
            uav_data = UAV.objects.filter(id=e["uav"]).first()
            model_data = Model.objects.filter(id=uav_data.model.id).first()
            brand_data = Brand.objects.filter(id=model_data.brand.id).first()
            e["username"] = user_data.username
            e["uav_name"] = uav_data.model.name + " -  " + brand_data.name
        
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        print(request.data["user"])
        return super().create(request, *args, **kwargs)

class ModelViewSet(viewsets.ModelViewSet):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticatedForNonGet]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticatedForNonGet]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedForNonGet]