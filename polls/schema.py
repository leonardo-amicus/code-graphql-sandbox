import graphene
from graphene_django import DjangoObjectType
from polls.models import Question, Response
from datetime import datetime


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question


class ResponseType(DjangoObjectType):
    class Meta:
        model = Response


class CreatePoll(graphene.Mutation):
    class Arguments:
        question = graphene.String(required=True)

    id = graphene.ID()
    pub_date = graphene.DateTime()
    question_text = graphene.String()

    def mutate(self, info, question):
        q = Question.objects.create(question_text=question)
        return CreatePoll(
            id=q.id,
            pub_date=q.pub_date,
            question_text=q.question_text
        )


class CreateResponse(graphene.Mutation):
    class Arguments:
        response_text = graphene.String(required=True)
        question_id = graphene.ID(required=True)

    id = graphene.ID()
    create_date = graphene.DateTime()
    response_text = graphene.String()
    question = graphene.Field(QuestionType)

    def mutate(self, info, question_id, response_text):
        question = Question.objects.get(pk=question_id)
        response = Response.objects.create(response_text=response_text,
                                           question_id=question.id)

        return CreateResponse(
            id=response.id,
            create_date=response.create_date,
            response_text=response.response_text,
            question=question,
        )


class UpdatePoll(graphene.Mutation):
    class Arguments:
        question_text = graphene.String(required=True)
        question_id = graphene.ID(required=True)

    question = graphene.Field(QuestionType)

    def mutate(self, info, question_text, question_id):
        question = Question.objects.get(pk=question_id)
        question.question_text = question_text
        question.edit_date = datetime.now()
        question.save()

        return UpdatePoll(question=question)


class DeletePoll(graphene.Mutation):
    class Arguments:
        question_id = graphene.ID(required=True)

    question = graphene.Field(QuestionType)

    def mutate(self, info, question_text, question_id):
        question = Question.objects.get(pk=question_id)
        question.delete()

        return UpdatePoll(question=question)


class Query(graphene.ObjectType):  # pylint: disable=no-init
    questions = graphene.List(QuestionType, n=graphene.Int(required=True))

    def resolve_questions(self, info, n=5):
        return Question.objects.all()[:n]


class Mutation(graphene.ObjectType):
    create_poll = CreatePoll.Field()
    create_response = CreateResponse.Field()
    update_poll = UpdatePoll.Field()
    delete_poll = DeletePoll.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
