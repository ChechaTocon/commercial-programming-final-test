import graphene
from graphene_django import DjangoObjectType
from .models import Category, Movie, Review, User

# Querys


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query(graphene.ObjectType):
    Category = graphene.List(CategoryType)

    def resolve_juegos(self, info, **kwargs):
        return Category.objects.all()

# Fin de querys


# Mutations
class CategoryInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    color = graphene.String()


class CreateCategory(graphene.Mutation):
    class Arguments:
        input = CategoryInput(required=True)

    ok = graphene.Boolean()
    Category = graphene.Field(CategoryInput)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_instance = Category(name=input.name,
                                     color=input.color)
        category_instance.save()
        return CreateCategory(ok=ok, category=category_instance)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
# fin de mutations
