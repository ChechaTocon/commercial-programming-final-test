import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Category, Movie, Review, User

# Querys
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

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
    category = graphene.Field(CategoryType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        category_instance = Category(name=input.name,
                                     color=input.color)
        category_instance.save()
        return CreateCategory(ok=ok, category=category_instance)

#Espacio para usuario

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)        

    def mutate(self, info, username, password, email, first_name, last_name):
        user = get_user_model()(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


#fin del espacio para el usuario    
class Query(graphene.ObjectType):
    category = graphene.List(CategoryType)    
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_category(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user
#fin de las querys
class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_user = CreateUser.Field()
# fin de mutations
