from BaseClasses import Item, ItemClassification, Region
from worlds.AutoWorld import WebWorld, World

from .Items import (item_name_to_id as i_item_name_to_id, all_items as i_all_items,
                    item_name_groups as i_item_name_groups, item_classification as i_item_classification, NeonWhiteItem,
                    chapters as i_chapters)

from .Locations import location_name_to_id as l_location_name_to_id, all_locations as l_all_locations, \
    job_names as l_job_names, NeonWhiteLocation, giftless_jobs as l_giftless_jobs, \
    companion_sidequests as l_companion_sidequests, location_name_lfunct as l_location_name_lfunct
from .Options import NeonWhiteOptions
from ..generic.Rules import set_rule


class NeonWhiteWebWorld(WebWorld):
    # TODO: theme

    bug_report_page = "https://github.com/s5bug/NeonWhiteAP/issues"


class NeonWhiteWorld(World):
    """Neon White is a single-player speedrunning FPS where you can sacrifice
    your guns for godlike parkour moves."""

    game = "Neon White"
    web = NeonWhiteWebWorld()
    topology_present = True

    options_dataclass = NeonWhiteOptions
    options: NeonWhiteOptions

    item_name_to_id = i_item_name_to_id
    location_name_to_id = l_location_name_to_id
    item_name_groups = i_item_name_groups

    def generate_early(self) -> None:
        self.reward_medals = []
        if self.options.reward_bronze_trophies.value:
            self.reward_medals.append('Bronze')
        if self.options.reward_silver_trophies.value:
            self.reward_medals.append('Silver')
        if self.options.reward_gold_trophies.value:
            self.reward_medals.append('Gold')
        if self.options.reward_ace_trophies.value:
            self.reward_medals.append('Ace')
        if self.options.reward_author_trophies.value:
            self.reward_medals.append('Author')
        self.reward_gifts = self.options.reward_gifts.value
        self.reward_sidequests = self.options.reward_sidequests.value

    def create_item(self, name: str) -> NeonWhiteItem:
        return NeonWhiteItem(name, i_item_classification(name), self.item_name_to_id[name], self.player)

    def create_event(self, name: str) -> NeonWhiteItem:
        return NeonWhiteItem(name, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        # TODO: exclusions
        total_item_count = 0
        location_count = len(l_all_locations)
        for item_name in i_all_items:
            count = i_all_items[item_name]
            total_item_count += count
            self.multiworld.itempool += [self.create_item(item_name) for _ in range(count)]

        junk = location_count - total_item_count
        # TODO: actual junk items
        self.multiworld.itempool += [self.create_item('Insight: Green') for _ in range(junk)]

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        for chapter in range(0, 12):
            chapter_region = Region(f'M{chapter + 1:02d}', self.player, self.multiworld)

            chapter_l = l_job_names[chapter]
            chapter_dict = {}
            job_idx = 1
            for job in chapter_l:
                job_full_name = f'M{chapter + 1:02d}L{job_idx:02d} {job}'
                for medal in self.reward_medals:
                    location_name = f'{job_full_name}: {medal}'
                    chapter_dict[location_name] = self.location_name_to_id[location_name]

                if job not in l_giftless_jobs and self.reward_gifts:
                    location_name = f'{job_full_name}: Gift'
                    chapter_dict[location_name] = self.location_name_to_id[location_name]

                job_idx += 1

            chapter_region.add_locations(chapter_dict, NeonWhiteLocation)

            if chapter == 11:
                absolution_loc = NeonWhiteLocation(self.player, 'M12L02 Absolution: Clear', None, chapter_region)
                chapter_region.locations.append(absolution_loc)

            def has_item_capture(item: str):
                return lambda state: state.has(item, self.player)
            menu_region.connect(chapter_region, rule=has_item_capture(i_chapters[chapter]))

        if self.reward_sidequests:
            for (companion, companion_l) in l_companion_sidequests:
                companion_region = Region(companion, self.player, self.multiworld)

                sidequest_dict = {}
                for sidequest in companion_l:
                    location_name = f'{companion}: {sidequest}'
                    sidequest_dict[location_name] = self.location_name_to_id[location_name]

                companion_region.add_locations(sidequest_dict, NeonWhiteLocation)

                menu_region.connect(companion_region)

    def generate_basic(self) -> None:
        (self.multiworld
         .get_location('M12L02 Absolution: Clear', self.player)
         .place_locked_item(self.create_event('Absolution')))

        self.multiworld.completion_condition[self.player] =\
            lambda state: state.has('Absolution', self.player)

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region('Menu', self.player), "neon_white.puml")

    def set_rules(self) -> None:
        from worlds.neon_white.Rules import reachability_full

        def lset_rule(path: list[str], rule) -> None:
            location_name = l_location_name_lfunct.lget(path)
            try:
                location = self.multiworld.get_location(location_name, self.player)
                set_rule(location, rule.as_lambda(self.player))
            except KeyError:
                pass

        reachability_full.lmap([], lset_rule)

        set_rule(self.multiworld.get_location('M12L02 Absolution: Clear', self.player),
                 lambda state: state.has('Card: Book of Life', self.player) and
                               state.has('Ability: Book of Life', self.player) and
                               state.has('Card: Dominion', self.player))
