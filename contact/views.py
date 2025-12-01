from rest_framework.response import Response
from .models import Contact
from .serializers import ContactSerializer
from rest_framework import generics, status, permissions, filters
from rest_framework.pagination import PageNumberPagination


class ContactPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {"detail": "Thank you for contacting us! We’ll get back to you soon."},
            status=status.HTTP_201_CREATED,
        )


class ContactListView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = ContactPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "email", "subject", "message"]

    def get_queryset(self):
        queryset = Contact.objects.all().order_by("-created_at")

        # allow filtering for handled/unhandled messages
        handled = self.request.query_params.get("handled")
        if handled is not None:
            queryset = queryset.filter(handled=(handled.lower() == "true"))

        return queryset

class ContactDetailView(generics.RetrieveUpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]