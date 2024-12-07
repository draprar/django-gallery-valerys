from django.core.management.base import BaseCommand
from django.utils import timezone
from gallery.models import Category, InstagramPost


class Command(BaseCommand):
    help = 'Fetch Instagram posts and assign to a specific category'

    def handle(self, *args, **kwargs):
        # Get the "Otednawden" category
        category = Category.objects.get(title='Otednawden')

        # Manually adding Instagram posts
        posts = [
            {
                'image_url': 'https://www.instagram.com/p/C9rut_PCAX_/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==/',
                'caption': 'I #drawing #draw #sketch #sketching #sketchbook #drawings #sketching #pencildrawing #pencil',
                'created_at': timezone.now(),
            },
            {
                'image_url': 'https://www.instagram.com/p/C9u2COtCx3F/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==',
                'caption': 'III #drawing #draw #sketch #sketching #sketchbook #drawings #sketching #pencildrawing #pencil',
                'created_at': timezone.now(),
            },
        ]

        for post_data in posts:
            InstagramPost.objects.create(
                image_url=post_data['image_url'],
                caption=post_data['caption'],
                created_at=post_data['created_at'],
                category=category,
            )

        self.stdout.write(self.style.SUCCESS('Successfully added Instagram posts to Otednawden category'))
