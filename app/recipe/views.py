"""
Views for the recipe APIs.
"""

from core.models import (
    Recipe,
    Tag,
    Ingredient
)

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
    IngredientSerializer
)

from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class RecipeViewSet(viewsets.ModelViewSet):
    """Handles Logic for Recipe APIs. / View for manage recipe APIs."""

    # Objects available for this viewset
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    # Token Authentication
    authentication_classes = [TokenAuthentication]
    # Permissions that authenticated users have in the system
    permission_classes = [IsAuthenticated]

    """ Overiding getquery set method to filter the recipes for
    authenticated user"""
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    """ Overriding this method as we have different serializer for
    list and detail view"""
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            self.serializer_class = RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""

        """When a new recipe is created then assigning authencticated user
        to that recipe"""
        serializer.save(user=self.request.user)


class BaseRecipeAttrViewSet(mixins.UpdateModelMixin,
                            mixins.ListModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):

    """Base viewset for recipe attributes."""
    # Token Authentication
    authentication_classes = [TokenAuthentication]
    # Permissions that authenticated users have in the system
    permission_classes = [IsAuthenticated]

    """ Overiding getquery set method to filter the Tags/Ingredients for
    authenticated user """
    def get_queryset(self):
        """Retrieve Tags/Ingredients for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in the database"""

    # Objects available for this viewset
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage Ingredients in the database"""

    # Objects available for this viewset
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
