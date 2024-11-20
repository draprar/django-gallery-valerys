import os
import requests
from gallery.models import InstagramPost, Category


def fetch_instagram_posts():
    access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("Instagram access token is missing. Set it in your .env file.")

    url = f"https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp&access_token={access_token}"
    response = requests.get(url).json()

    drawing_category, _ = Category.objects.get_or_create(title="Drawing")

    for post in response.get('data', []):
        if post['media_type'] == 'IMAGE':
            InstagramPost.objects.get_or_create(
                image_url=post['media_url'],
                caption=post.get('caption', ''),
                created_at=post['timestamp'],
                category=drawing_category
            )
