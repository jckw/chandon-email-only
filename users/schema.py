import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model
from graphene import relay, ObjectType
import graphql_jwt
from graphql_jwt.decorators import login_required
from django.contrib.auth import authenticate


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


class ChangePassword(graphene.Mutation):
    class Arguments:
        old_password = graphene.String()
        new_password = graphene.String()

    user = graphene.Field(User)

    @login_required
    def mutate(self, info, old_password, new_password):
        email = info.context.user.email
        user = authenticate(email=email, password=old_password)

        if user is None:
            raise ValueError('Incorrect password')

        user.set_password(new_password)
        user.save()

        return ChangePassword(user=user)


class Query(ObjectType):
    user = graphene.Field(User)


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    login = graphql_jwt.ObtainJSONWebToken.Field()
    change_password = ChangePassword.Field()
