import unittest

from x_publisher import XPublisher


class XPublisherTests(unittest.TestCase):
    def test_tweet_text_is_at_most_30_words_and_280_chars(self):
        text = XPublisher.tweet_text(' '.join(f'word{i}' for i in range(100)), 'meeting-123')
        self.assertLessEqual(len(text.split()), 30)
        self.assertLessEqual(len(text), 280)

    def test_meeting_hint_prevents_identical_posts(self):
        summary = 'A repeated meeting decision with the same opening text. A new research task follows.'
        first = XPublisher.tweet_text(summary, 'first-meeting')
        second = XPublisher.tweet_text(summary, 'second-meeting', [first])
        self.assertNotEqual(first, second)
        self.assertNotIn('first-meeting', first)
        self.assertNotIn('second-meeting', second)
        self.assertLessEqual(len(first.split()), 30)
        self.assertLessEqual(len(second.split()), 30)

    def test_tweet_uses_the_conclusion_instead_of_repeated_opening(self):
        summary = 'The recurring opening says no launch. New evidence requires a different research test before any decision.'
        text = XPublisher.tweet_text(summary, 'meeting-123')
        self.assertIn('New evidence requires', text)
        self.assertNotIn('The recurring opening says', text)
        self.assertLessEqual(len(text.split()), 30)

    def test_tweet_removes_dash_characters(self):
        text = XPublisher.tweet_text('Review unresolved evidence — not branding or launch dates. Follow up with the team.', 'meeting')
        self.assertNotRegex(text, r'[-–—−]')
        self.assertLessEqual(len(text.split()), 30)

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
