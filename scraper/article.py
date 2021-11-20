from collections import namedtuple

from .article_meta import parse_meta

# whole record information
Article = namedtuple('Article', ['name', 'images',  'summary', 'meta'])

def parse_article(post):
    # posts can have multiple pictures
    # structure is "url width" so we only use "url" and ignore "width"
    images = []
    src_set = post.img.get('data-lazy-srcset')
    for img in src_set.split(',') if src_set else [post.img.get('data-lazy-src')]:
        images.append(img.strip().split(' ')[0])

    # meta information like calories, fats, carbs 
    # and green, blue and purple point and keys
    # are parsed here 
    post_meta = post.select_one('div.post-meta')

    record = Article(
        name = post.h2.text,
        images = images,
        summary = post.select_one('div.post-content').text.strip(),
        meta = parse_meta(post_meta)
    )

    return record
