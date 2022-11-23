from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase


class TestPolls(GraphQLTestCase):
    GRAPHQL_URL = "/"

    def test_returns_questions(self):
        poll_response = self.query("""
            {
                questions(n: 10) {
                    questionText
                }
            }
        """)
        self.assertEqual(len(poll_response.json()['data']['questions']), 0)

    def test_creates_question(self):
        question = "How are you?"
        response = self.query(
            """
            mutation createPoll($question: String!) {
                createPoll(question: $question) {
                    id,
                    pubDate,
                    questionText
                }
            }
            """,
            operation_name="createPoll",
            variables={"question": question}
        )

        # This validates the status code and if you get errors
        self.assertResponseNoErrors(response)
        self.assertEqual(response.json()['data']
                         ['createPoll']['questionText'], question)
        self.assertIsNotNone(
            response.json()['data']['createPoll'].get('pubDate', None))
