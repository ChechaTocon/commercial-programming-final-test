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

# Inicio para la movie
class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class MovieNode(DjangoObjectType):
    class Meta:
        model = Movie
        # Permite un filtrado mas avanzado
        filter_fields = {
            'poster': ['exact', 'icontains', 'istartswith'],
            'movieName': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'createdAt': ['exact', 'icontains'],
            'updatedAt': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (relay.Node, )
class CrearMovie(graphene.Mutation):
    class Arguments:
        poster= graphene.String()
        movieName = graphene.String()
        description= graphene.String()    
        category = graphene.Int()

    movie = graphene.Field(MovieNode)
    def mutate(self, info, poster, movieName,  description, category):
        objeto_categoria=Category.objects.get(id=category)
        movie = Movie.objects.create(
            poster= poster,
            movieName = movieName,
            description = description,       
            category=objeto_categoria                             
        )           

        movie.save()
        return CrearMovie(
            movie=movie
        )
class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        poster = graphene.String()
        movieName = graphene.String()
        description = graphene.String()
        category = graphene.List(graphene.ID)
    movie = graphene.Field(MovieType)

    def mutate(self, info, id, poster=None, movieName=None, description= None, category=None):
      movie = Movie.objects.get(pk=id)
      movie.poster = poster if poster is not None else movie.poster
      movie.movieName = movieName if movieName is not None else movie.movieName
      movie.description = description if description is not None else movie.description

      if category is not None:
        category_set = []
        for category_id in category:
          category_object = Category.objects.get(pk=category_id)
        movie.category = category_object


      movie.save()

      return UpdateMovie(movie=movie)

# FIn del espacio para a movie
 
 
 
   
class Query(graphene.ObjectType):
    category = graphene.List(CategoryType) 
    movie = relay.Node.Field(MovieNode)
    all_movies = DjangoFilterConnectionField(MovieNode)

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
    create_movie = CrearMovie.Field()
    update_movie = UpdateMovie.Field()
# fin de mutations
