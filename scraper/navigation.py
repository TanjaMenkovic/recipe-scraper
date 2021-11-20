from collections import namedtuple

Navigation = namedtuple('Navigation', ['current', 'next_link'])

def parse_navigation(page):
    navigation = page.select_one('nav.navigation.pagination')

    current_page = int(navigation.select_one('span.current').text.strip())
    next_page = navigation.select_one('a.next')

    return Navigation(
        current = current_page,
        next_link = next_page.get('href') if next_page else None 
    )