import abc
import dataclasses
from dataclasses import dataclass
from typing import Callable, TypeVar, Generic

from BaseClasses import CollectionState
from .Locations import NeonWhiteLocations, NeonWhiteLocationsJobs, NeonWhiteLocationsMission01, \
    NeonWhiteLocationsJobGift, NeonWhiteLocationsMission02, NeonWhiteLocationsJobMedals, NeonWhiteLocationsSidequests, \
    NeonWhiteLocationsSidequestsRed, NeonWhiteLocationsSidequestsViolet, NeonWhiteLocationsSidequestsYellow, \
    NeonWhiteLocationsMission03, NeonWhiteLocationsMission04, NeonWhiteLocationsMission05, NeonWhiteLocationsMission06, \
    NeonWhiteLocationsMission07, NeonWhiteLocationsMission08, NeonWhiteLocationsMission09, NeonWhiteLocationsMission10, \
    NeonWhiteLocationsMission11, NeonWhiteLocationsMission12

A = TypeVar('A')


class Variable(abc.ABC, Generic[A]):
    @abc.abstractmethod
    def as_lambda(self, player: int) -> Callable[[CollectionState], A]:
        pass

    def __and__(self: 'Variable[bool]', other: 'Variable[bool]') -> 'Variable[bool]':
        return AndVariable(self, other)

    def __or__(self: 'Variable[bool]', other: 'Variable[bool]') -> 'Variable[bool]':
        return OrVariable(self, other)


@dataclass
class AndVariable(Variable[bool]):
    left: Variable[bool]
    right: Variable[bool]

    def as_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        left_l = self.left.as_lambda(player)
        right_l = self.right.as_lambda(player)
        return lambda state: left_l(state) and right_l(state)


@dataclass
class OrVariable(Variable[bool]):
    left: Variable[bool]
    right: Variable[bool]

    def as_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        left_l = self.left.as_lambda(player)
        right_l = self.right.as_lambda(player)
        return lambda state: left_l(state) or right_l(state)


@dataclass
class HasItemVariable(Variable[bool]):
    item_name: str

    def as_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(self.item_name, player)


@dataclass
class HasAtLeastItemVariable(Variable[bool]):
    item_name: str
    target_count: int

    def as_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(self.item_name, player, self.target_count)


@dataclass
class DualWeapon:
    main: Variable[bool]
    discard: Variable[bool]


@dataclass
class ConstantVariable(Variable[bool]):
    value: bool

    def as_lambda(self, player: int) -> Callable[[CollectionState], bool]:
        return lambda state: self.value


always: Variable[bool] = ConstantVariable(True)
katana: Variable[bool] = HasItemVariable('Card: Katana')
elevate = DualWeapon(HasItemVariable('Card: Elevate'), HasItemVariable('Ability: Elevate'))
purify = DualWeapon(HasItemVariable('Card: Purify'), HasItemVariable('Ability: Purify'))
godspeed = DualWeapon(HasItemVariable('Card: Godspeed'), HasItemVariable('Ability: Godspeed'))

insight_red: Callable[[int], Variable[bool]] = lambda x: HasAtLeastItemVariable('Insight: Red', x)
insight_violet: Callable[[int], Variable[bool]] = lambda x: HasAtLeastItemVariable('Insight: Violet', x)
insight_yellow: Callable[[int], Variable[bool]] = lambda x: HasAtLeastItemVariable('Insight: Yellow', x)


reachability: NeonWhiteLocations[Variable[bool]] = NeonWhiteLocations(
    jobs=NeonWhiteLocationsJobs(
        m01_rebirth=NeonWhiteLocationsMission01(
            l01_movement=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_pummel=NeonWhiteLocationsJobGift(
                ace=always,
                author=purify.discard,
                gift=always
            ),
            l03_gunner=NeonWhiteLocationsJobGift(
                ace=always,
                author=purify.main & purify.discard,
                gift=purify.discard
            ),
            l04_cascade=NeonWhiteLocationsJobGift(
                ace=elevate.discard,
                author=elevate.main & elevate.discard,
                gift=elevate.discard
            ),
            l05_elevate=NeonWhiteLocationsJobGift(
                author=elevate.discard,
                gift=always
            ),
            l06_bounce=NeonWhiteLocationsJobGift(
                ace=elevate.discard,
                author=elevate.main & elevate.discard,
                gift=elevate.discard
            ),
            l07_purify=NeonWhiteLocationsJobGift(
                gold=purify.main,
                ace=purify.discard,
                author=purify.main & purify.discard,
                gift=purify.discard
            ),
            l08_climb=NeonWhiteLocationsJobGift(
                author=purify.discard,
                gift=purify.discard
            ),
            l09_fasttrack=NeonWhiteLocationsJobGift(
                bronze=always,
                ace=katana | purify.main,
                author=purify.main & (purify.discard | elevate.discard),
                gift=elevate.discard & purify.discard
            ),
            l10_glass_port=NeonWhiteLocationsJobGift(
                gold=elevate.main & elevate.discard,
                ace=purify.discard | (elevate.discard & (katana | purify.main)),
                author=purify.main & purify.discard & elevate.discard,
                gift=purify.discard | elevate.discard
            )
        ),
        m02_killer_inside=NeonWhiteLocationsMission02(
            l01_take_flight=NeonWhiteLocationsJobGift(
                ace=elevate.discard & purify.discard,
                author=elevate.discard & purify.discard & (purify.main | elevate.main),
                gift=elevate.discard & purify.discard
            ),
            l02_godspeed=NeonWhiteLocationsJobGift(
                bronze=katana & godspeed.main,
                author=godspeed.discard,
                gift=godspeed.discard
            ),
            l03_dasher=NeonWhiteLocationsJobGift(
                silver=katana | godspeed.main,
                gold=godspeed.discard,
                ace=godspeed.discard & (godspeed.main | elevate.main),
                author=godspeed.main & godspeed.discard & elevate.main & elevate.discard,
                gift=always
            ),
            l04_thrasher=NeonWhiteLocationsJobGift(
                ace=godspeed.discard,
                author=godspeed.discard & godspeed.main,
                gift=godspeed.discard
            ),
            l05_outstretched=NeonWhiteLocationsJobGift(
                bronze=elevate.discard,
                silver=elevate.discard & godspeed.main,
                gold=elevate.discard & godspeed.discard,
                author=godspeed.main & godspeed.discard & elevate.discard,
                gift=elevate.discard
            ),
            l06_smackdown=NeonWhiteLocationsJobGift(
                gold=elevate.discard & (elevate.main | katana | godspeed.main),
                author=elevate.discard & godspeed.discard,
                gift=elevate.discard
            ),
            l07_catwalk=NeonWhiteLocationsJobGift(
                ace=godspeed.discard,
                author=godspeed.discard & godspeed.main,
                gift=godspeed.discard
            ),
            l08_fastlane=NeonWhiteLocationsJobGift(
                ace=always,
                author=godspeed.discard,
                gift=always
            ),
            l09_distinguish=NeonWhiteLocationsJobGift(
                gold=elevate.discard & godspeed.discard,
                ace=elevate.main & elevate.discard & godspeed.discard,
                author=elevate.discard & godspeed.main & godspeed.discard,
                gift=elevate.discard & godspeed.discard
            ),
            l10_dancer=NeonWhiteLocationsJobGift(
                bronze=elevate.discard & godspeed.main,
                ace=elevate.discard & godspeed.discard,
                author=elevate.discard & godspeed.discard & godspeed.main,
                gift=godspeed.discard
            )
        ),
        m03_only_shallow=NeonWhiteLocationsMission03(
            l01_guardian=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_stomp=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_jumper=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_dash_tower=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_descent=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_driller=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_canals=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_sprint=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_mountain=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_superkinetic=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m04_the_old_city=NeonWhiteLocationsMission04(
            l01_arrival=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_forgotten_city=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_clocktower=NeonWhiteLocationsJobMedals(
                author=always
            )
        ),
        m05_the_burn_that_cures=NeonWhiteLocationsMission05(
            l01_fireball=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_ringer=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_cleaner=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_warehouse=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_boom=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_streets=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_steps=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_demolition=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_arcs=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_apartment=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m06_covenant=NeonWhiteLocationsMission06(
            l01_hanging_gardens=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_tangled=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_waterworks=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_killswitch=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_falling=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_shocker=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_bouquet=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_prepare=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_triptrack=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_race=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m07_reckoning=NeonWhiteLocationsMission07(
            l01_bubble=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_shield=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_overlook=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_pop=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_minefield=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_mimic=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_trigger=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_greenhouse=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_sweep=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_fuse=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m08_benediction=NeonWhiteLocationsMission08(
            l01_heavens_edge=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_zipline=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_swing=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_chute=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_crash=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_ascent=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_straightaway=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_firecracker=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_streak=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_mirror=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m09_apocrypha=NeonWhiteLocationsMission09(
            l01_escalation=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_bolt=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_godstreak=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_plunge=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_mayhem=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_barrage=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_estate=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_trapwire=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_ricochet=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_fortress=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m10_the_third_temple=NeonWhiteLocationsMission10(
            l01_holy_ground=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_the_third_temple=NeonWhiteLocationsJobMedals(
                author=always
            )
        ),
        m11_thousand_pound_butterfly=NeonWhiteLocationsMission11(
            l01_spree=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l02_breakthrough=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l03_glide=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l04_closer=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l05_hike=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l06_switch=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l07_access=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l08_congregation=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l09_sequence=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            ),
            l10_marathon=NeonWhiteLocationsJobGift(
                author=always,
                gift=always
            )
        ),
        m12_hand_of_god=NeonWhiteLocationsMission12(
            l01_sacrifice=NeonWhiteLocationsJobMedals(
                author=always
            ),
            l02_absolution=NeonWhiteLocationsJobMedals(
                author=always
            )
        )
    ),
    sidequests=NeonWhiteLocationsSidequests(
        red=NeonWhiteLocationsSidequestsRed(
            s1_elevate_traversal_1=insight_red(2),
            s2_elevate_traversal_2=insight_red(4),
            s3_purify_traversal=insight_red(6),
            s4_godspeed_traversal=insight_red(8),
            s5_stomp_traversal=insight_red(11),
            s6_fireball_traversal=insight_red(13),
            s7_dominion_traversal=insight_red(15),
            s8_book_of_life_traversal=insight_red(18)
        ),
        violet=NeonWhiteLocationsSidequestsViolet(
            s1_doghouse=insight_violet(2),
            s2_choker=insight_violet(4),
            s3_chain=insight_violet(6),
            s4_hellevator=insight_violet(8),
            s5_razor=insight_violet(11),
            s6_all_seeing_eye=insight_violet(13),
            s7_resident_saw_1=insight_violet(15),
            s8_resident_saw_2=insight_violet(17)
        ),
        yellow=NeonWhiteLocationsSidequestsYellow(
            s1_sunset_flip_powerbomb=insight_yellow(2),
            s2_balloon_mountain=insight_yellow(4),
            s3_climbing_gym=insight_yellow(6),
            s4_fisherman_suplex=insight_yellow(9),
            s5_stf=insight_yellow(10),
            s6_arena=insight_yellow(11),
            s7_attitude_adjustment=insight_yellow(12),
            s8_rocket=insight_yellow(13)
        )
    )
)


def cascade_medals(jm: NeonWhiteLocationsJobMedals[Variable[bool]]) -> NeonWhiteLocationsJobMedals[Variable[bool]]:
    plus = dataclasses.replace(jm)
    plus.author = jm.author or ConstantVariable(False)
    plus.ace = plus.author | (jm.ace or ConstantVariable(False))
    plus.gold = plus.ace | (jm.gold or ConstantVariable(False))
    plus.silver = plus.gold | (jm.silver or ConstantVariable(False))
    plus.bronze = plus.silver | (jm.bronze or ConstantVariable(False))
    return plus


def level_required(path: list[str], variable: Variable[bool]) -> Variable[bool]:
    if path[0] == "jobs":
        from worlds.neon_white.Locations import level_name_lfunct
        return variable & HasItemVariable(level_name_lfunct.lget(path[1:]))
    else:
        return variable


reachability_full = reachability.map_medals(cascade_medals).lmap([], level_required)
