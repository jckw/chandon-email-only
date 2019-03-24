import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from graphene import relay, ObjectType
import graphql_jwt


class User(DjangoObjectType):
    class Meta:
        model = get_user_model()
        interfaces = (relay.Node, )


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, email, password):
        UserModel = get_user_model()
        user = UserModel.objects.create_user(email, password)

        return CreateUser(user=user)


class Query(ObjectType):
    user = graphene.Field(User)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
