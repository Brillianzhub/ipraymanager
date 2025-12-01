# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from django.db.models import Q
# from .models import ShareTemplate
# from .serializers import TemplateSerializer, TemplateListSerializer
# from .permissions import TemplatePermission


# class TemplateViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for Template model with custom permissions
#     """
#     queryset = ShareTemplate.objects.all()
#     serializer_class = TemplateSerializer
#     permission_classes = [TemplatePermission]

#     def get_serializer_class(self):
#         """Use minimal serializer for list view"""
#         if self.action == 'list':
#             return TemplateListSerializer
#         return TemplateSerializer

#     def get_queryset(self):
#         """
#         Optionally filter templates by type
#         """
#         queryset = ShareTemplate.objects.all()
#         template_type = self.request.query_params.get('type', None)

#         if template_type:
#             queryset = queryset.filter(template_type=template_type)

#         search = self.request.query_params.get('search', None)
#         if search:
#             queryset = queryset.filter(
#                 Q(name__icontains=search) | Q(template_type__icontains=search)
#             )

#         return queryset

#     @action(detail=False, methods=['get'])
#     def types(self, request):
#         """
#         Get available template types
#         """
#         types = [
#             {'value': choice[0], 'label': choice[1]}
#             for choice in ShareTemplate.TEMPLATE_TYPE_CHOICES
#         ]
#         return Response(types)

#     @action(detail=False, methods=['get'])
#     def verses(self, request):
#         """
#         Get verse templates only
#         """
#         templates = ShareTemplate.objects.filter(template_type='verse')
#         serializer = TemplateListSerializer(templates, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'])
#     def prayers(self, request):
#         """
#         Get prayer templates only
#         """
#         templates = ShareTemplate.objects.filter(template_type='prayer')
#         serializer = TemplateListSerializer(templates, many=True)
#         return Response(serializer.data)


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import ShareTemplate
from .serializers import TemplateSerializer, TemplateListSerializer
from .permissions import TemplatePermission


class TemplateViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Template model with custom permissions
    """
    queryset = ShareTemplate.objects.all()
    serializer_class = TemplateSerializer
    permission_classes = [TemplatePermission]

    def get_queryset(self):
        """
        Optionally filter templates by type
        """
        queryset = ShareTemplate.objects.all()
        template_type = self.request.query_params.get('type', None)

        if template_type:
            queryset = queryset.filter(template_type=template_type)

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(template_type__icontains=search)
            )

        return queryset

    @action(detail=False, methods=['get'])
    def minimal(self, request):
        """
        Get minimal template list (for dropdown/selection purposes)
        """
        templates = self.get_queryset()
        serializer = TemplateListSerializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def types(self, request):
        """
        Get available template types
        """
        types = [
            {'value': choice[0], 'label': choice[1]}
            for choice in ShareTemplate.TEMPLATE_TYPE_CHOICES
        ]
        return Response(types)

    @action(detail=False, methods=['get'])
    def verses(self, request):
        """
        Get verse templates only
        """
        templates = ShareTemplate.objects.filter(template_type='verse')
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def prayers(self, request):
        """
        Get prayer templates only
        """
        templates = ShareTemplate.objects.filter(template_type='prayer')
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)
