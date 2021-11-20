from collections import namedtuple

# point information
Point = namedtuple('SmartPoint', ['green', 'blue', 'purple'])

Key = namedtuple('Key', ['name', 'url', 'image'])

Nutrition = namedtuple('Nutrition', ['calories', 'carbs', 'fat', 'proteins'])

Meta = namedtuple('Meta', [ 'keys', 'point', 'nutrition' ])

def parse_keys(post_meta):
    # parsing of keys
    keys = []
    icons = post_meta.select_one('div.icons')
    links_in_icons = icons.find_all('a') if icons else []
    for link in links_in_icons:
        keys.append(
            Key(name = link.img.get('alt'), url=link.get('href'), image=link.img.get('data-lazy-src')),
        )

    return keys

def parse_smart_points(post_meta):
    # parsing of smartpoints
    # in some cases we don't have smart points
    smart_points = post_meta.select_one('span.smartpoints') 

    blue = smart_points.select_one('span.blue') if smart_points else None
    green = smart_points.select_one('span.green') if smart_points else None
    purple = smart_points.select_one('span.purple') if smart_points else None

    return Point(
        blue=int(blue.text) if blue else None,
        green=int(green.text) if green else None,
        purple=int(purple.text) if purple else None,
    )

def parse_nutrition(post_meta):
    calories = post_meta.select_one('span.recipe-meta-value.value-calories')
    protein = post_meta.select_one('span.recipe-meta-value.value-protein')
    carbs = post_meta.select_one('span.recipe-meta-value.value-carbs')
    fat = post_meta.select_one('span.recipe-meta-value.value-fat')

    get_number = lambda text: float(text.strip().split(' ')[0])

    return Nutrition(
        calories = get_number(calories.text) if calories else None, 
        proteins = get_number(protein.text) if protein else None,
        carbs = get_number(carbs.text) if carbs else None, 
        fat = get_number(fat.text) if fat else None
    )

def parse_meta(post_meta):
    return Meta(
        keys = parse_keys(post_meta), 
        point = parse_smart_points(post_meta), 
        nutrition = parse_nutrition(post_meta)
    )