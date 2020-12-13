import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from .models import Category, Movie, Review, User
from django.utils import timezone

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
 

 #INICIO DE REVIEW
class ReviewType(DjangoObjectType):
    class Meta:
        model = Review

class ReviewInput(graphene.InputObjectType):
    id = graphene.ID()
    comment = graphene.String()
    ranking = graphene.Int()
    movie = graphene.Int()
    user = graphene.Int()

class CreateReview(graphene.Mutation):
    class Arguments:
        input = ReviewInput(required=True)

    ok = graphene.Boolean()
    review = graphene.Field(ReviewType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user_obj = User.objects.get(id=input.user)
        movie_obj = Movie.objects.get(id=input.user)
        review_instance = Review(
          comment=input.comment,
          ranking=input.ranking,
          createdAt=timezone.now(),
          updatedAt= timezone.now(),
          movie=movie_obj,
          user=user_obj
          )
        review_instance.save()
        return CreateReview(ok=ok, review=review_instance)


class UpdateReview(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ReviewInput(required=True)

    ok = graphene.Boolean()
    review = graphene.Field(ReviewType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        review_instance = Review.objects.get(pk=id)
        if review_instance:
            ok = True           
            user_obj = User.objects.get(id=input.user)
            movie_obj = Movie.objects.get(id=input.user)

            review_instance.comment=input.comment
            review_instance.ranking=input.ranking
            review_instance.updatedAt=timezone.now()
            review_instance.movie=movie_obj
            review_instance.user=user_obj

            review_instance.save()            
            return UpdateReview(ok=ok, review=review_instance)
        return UpdateReview(ok=ok, review=None)

class FindReview(graphene.Mutation):
    class Arguments:
        movie_id = graphene.Int(required=True)        

    ok = graphene.Boolean()
    review = graphene.Field(ReviewType)

    @staticmethod
    def mutate(root, info, movie_id):
        ok = False        
        review_instance = Review.objects.get(movie=movie_id)
        if review_instance:
            ok = True                       
                
            return FindReview(ok=ok, review=review_instance)
        return FindReview(ok=ok, review=None)

#FIN DE REVIEW
 
 
   
class Query(graphene.ObjectType):
    category = graphene.List(CategoryType) 
    movie = relay.Node.Field(MovieNode)
    all_movies = DjangoFilterConnectionField(MovieNode)

    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    review = graphene.Field(ReviewType, id=graphene.Int(), movie_id=graphene.Int())     
    reviews = graphene.List(ReviewType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_category(self, info, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')        
        return Category.objects.all()
    
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        return user
    
    def resolve_review(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Review.objects.get(pk=id)

        return None    
    
    
    def resolve_reviews(self, info, **kwargs):
        return Review.objects.all()
#fin de las querys
class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_user = CreateUser.Field()
    create_movie = CrearMovie.Field()
    update_movie = UpdateMovie.Field()
    create_review = CreateReview.Field()
    update_review = UpdateReview.Field()
    find_review = FindReview.Field()
# fin de mutations
