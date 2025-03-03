from typing import Any

from django.core.management.base import BaseCommand

from factories import artist_create


class Command(BaseCommand):
    help = "Seed the db with fixtures"

    def handle(self, *args: Any, **options: Any) -> None:
        genres = ["Christian", "Rock", "Pop", "Folk", "Metal", "Indie", "RnB", "Hip Hop"]
        for genre in genres:
            for _ in range(10):
                artist_create(genres=[genre])

        self.stdout.write(self.style.SUCCESS("Successfully created 10 artists"))
