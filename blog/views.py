from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Blog, Category
from .serializers import BlogSerializer, CategorySerializer

from rest_framework.pagination import PageNumberPagination
from .serializers import BlogListSerializer


@api_view(["GET"])
def fetch_blogs(request):
    blogs = Blog.objects.filter(status="published").order_by("-created")

    paginator = PageNumberPagination()
    paginator.page_size = 10  # adjust batch size
    result_page = paginator.paginate_queryset(blogs, request)

    serializer = BlogListSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


# Fetch single blog by slug
@api_view(["GET"])
def fetch_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)


# Create blog post
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_blog(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Update blog by slug

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticatedOrReadOnly])
def update_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # ensure only author can update
    if request.user != blog.author and not request.user.is_staff:
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    serializer = BlogSerializer(blog, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete blog by slug
@api_view(["DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.user != blog.author and not request.user.is_staff:
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    blog.delete()
    return Response({"message": "Blog deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([IsAuthenticatedOrReadOnly])
def toggle_publish(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    # only author can toggle
    if request.user != blog.author and not request.user.is_staff:
        return Response({"error": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    # toggle status
    if blog.status == "published":
        blog.status = "draft"
    else:
        blog.status = "published"

    blog.save()
    return Response(
        {"message": f"Blog is now {blog.status}", "status": blog.status},
        status=status.HTTP_200_OK
    )

# Fetch all categories


@api_view(["GET"])
@permission_classes([AllowAny])
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
