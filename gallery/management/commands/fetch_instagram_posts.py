from django.core.management.base import BaseCommand
from django.utils import timezone
from gallery.models import Category, InstagramPost


class Command(BaseCommand):
    help = 'Fetch Instagram posts and assign to a specific category'

    def handle(self, *args, **kwargs):
        # Get the "Otednawden" category or prompt the user to specify a category
        category_title = input("Enter the category title (default: 'Otednawden'): ") or 'Otednawden'
        try:
            category = Category.objects.get(title=category_title)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Category '{category_title}' does not exist."))
            return

        while True:
            # Collect post details from the user
            image_url = input("Enter the Instagram post URL (or type 'exit' to quit): ")
            if image_url.lower() == 'exit':
                break

            caption = input("Enter the post caption: ")
            created_at = timezone.now()  # You can allow a custom date if needed

            # Save the post
            InstagramPost.objects.create(
                image_url=image_url,
                caption=caption,
                created_at=created_at,
                category=category,
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully added Instagram post: {image_url}"))

        self.stdout.write(self.style.SUCCESS('All posts added successfully!'))
