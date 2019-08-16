from django.core.management import base

from guess import models


class Command(base.BaseCommand):
    help = 'Check for a winner in the current contest'

    def handle(self, *args, **options):
        contest = models.LuckyCallContest.get_active_contest()
        if not contest:
            self.stdout.write('No contest was created yet.')
            return

        winner = contest.winner or contest.check_winner()
        if not winner:
            self.stdout.write('Nobody is the winner yet.')
            return

        self.stdout.write('-' * 80)
        self.stdout.write('We have a winner! {}'.format(winner.user_email))
        self.stdout.write('-' * 80)

        self.stdout.write('The received requests were:')
        for guess in contest.guesses:
            data = (
                guess.timestamp.isoformat(),
                guess.user_email,
                guess.keyword,
                str(guess.number),
            )
            self.stdout.write(' | '.join(data))
            if guess == winner:
                break
