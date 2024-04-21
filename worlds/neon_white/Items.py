from BaseClasses import Item, ItemClassification

base_item_namespace = 2874297668000000

chapter_unlock_offset = 1000
cards_offset = 2000
card_abilities_offset = 3000
insight_offset = 4000

chapters = [
    'M01 Rebirth',
    'M02 Killer Inside',
    'M03 Only Shallow',
    'M04 The Old City',
    'M05 The Burn That Cures',
    'M06 Covenant',
    'M07 Reckoning',
    'M08 Benediction',
    'M09 Apocrypha',
    'M10 The Third Temple',
    'M11 Thousand Pound Butterfly',
    'M12 Hand of God'
]

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

all_items = {}
item_name_to_id = {}

item_individual_offset = 0
for chapter in chapters:
    all_items[chapter] = 1
    item_name_to_id[chapter] = base_item_namespace + chapter_unlock_offset + item_individual_offset
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

item_name_groups = {
    'Chapters': set(chapters),
    'Cards': set(cards),
    'CardAbilities': set(card_abilities),
    'Insights': set([name for (name, _) in insights])
}


progression_items = set(chapters) | set(cards) | set(card_abilities)


def item_classification(item: str) -> ItemClassification:
    if item in progression_items:
        return ItemClassification.progression
    elif item in cards or item in card_abilities:
        return ItemClassification.useful
    else:
        return ItemClassification.filler


class NeonWhiteItem(Item):
    game = "Neon White"
