from BaseClasses import Item, ItemClassification
from worlds.neon_white import Locations

base_item_namespace = 2874297668000000

level_unlock_offset = 1000
cards_offset = 2000
card_abilities_offset = 3000
insight_offset = 4000
neon_rank_offset = 5000

levels = []

chapter_num = 1
for chapter in Locations.job_names:
    level_num = 1
    for level in chapter:
        levels.append(f'M{chapter_num:02d}L{level_num:02d} {level}')
        level_num += 1

    chapter_num += 1

cards = [
    'Card: Katana',
    'Card: Purify',
    'Card: Elevate',
    'Card: Godspeed',
    'Card: Stomp',
    'Card: Fireball',
    'Card: Dominion',
    'Card: Book of Life'
]

card_abilities = [
    'Ability: Purify',
    'Ability: Elevate',
    'Ability: Godspeed',
    'Ability: Stomp',
    'Ability: Fireball',
    'Ability: Dominion',
    'Ability: Book of Life'
]

insights = [
    ('Insight: Yellow', 17 + 8),
    ('Insight: Red', 22 + 8),
    ('Insight: Violet', 22 + 8),
    ('Insight: Raz', 14),
    ('Insight: Mikey', 14),
    ('Insight: Green', 4)
]

neon_rank = [
    ('Neon Rank', 100)
]

all_items = {}
item_name_to_id = {}

item_individual_offset = 0
for level in levels:
    all_items[level] = 1
    item_name_to_id[level] = base_item_namespace + level_unlock_offset + item_individual_offset
    item_individual_offset += 1

item_individual_offset = 0
for card in cards:
    all_items[card] = 1
    item_name_to_id[card] = base_item_namespace + cards_offset + item_individual_offset
    item_individual_offset += 1

item_individual_offset = 0
for card_ability in card_abilities:
    all_items[card_ability] = 1
    item_name_to_id[card_ability] = base_item_namespace + card_abilities_offset + item_individual_offset
    item_individual_offset += 1

item_individual_offset = 0
for (name, count) in insights:
    all_items[name] = count
    item_name_to_id[name] = base_item_namespace + insight_offset + item_individual_offset
    item_individual_offset += 1

all_items['Neon Rank'] = 100
item_name_to_id['Neon Rank'] = base_item_namespace + neon_rank_offset

item_name_groups = {
    'Levels': set(levels),
    'Cards': set(cards),
    'CardAbilities': set(card_abilities),
    'Insights': set([name for (name, _) in insights]),
    'NeonRank': {'Neon Rank'}
}


progression_items = {'Neon Rank'} | set(cards) | set(card_abilities) | {'M12L02 Absolution'}
useful_items = set(levels) | {'Insight: Yellow', 'Insight: Red', 'Insight: Violet'}


def item_classification(item: str) -> ItemClassification:
    if item in progression_items:
        return ItemClassification.progression
    elif item in useful_items:
        return ItemClassification.useful
    else:
        return ItemClassification.filler


class NeonWhiteItem(Item):
    game = "Neon White"
