import unittest

from x_publisher import XPublisher


class XPublisherTests(unittest.TestCase):
    def test_tweet_text_is_at_most_30_words_and_280_chars(self):
        text = XPublisher.tweet_text(' '.join(f'word{i}' for i in range(100)))
        self.assertLessEqual(len(text.split()), 30)
        self.assertLessEqual(len(text), 280)

    def test_bearer_token_alone_cannot_publish(self):
        publisher = XPublisher({
            'X_POST_MEETINGS': 'true',
            'X_CONSUMER_KEY': 'consumer',
            'X_CONSUMER_SECRET': 'secret',
            'X_BEARER_TOKEN': 'bearer',
        })
        self.assertFalse(publisher.configured())
        self.assertIn('user access token', publisher.reason())
        self.assertFalse(publisher.post('A meeting summary')['posted'])

    def test_posting_can_be_disabled(self):
        publisher = XPublisher({'X_POST_MEETINGS': 'false'})
        self.assertFalse(publisher.configured())
        self.assertIn('disabled', publisher.reason())


if __name__ == '__main__':
    unittest.main()
