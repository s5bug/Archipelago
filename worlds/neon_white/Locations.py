import dataclasses
import typing
from dataclasses import dataclass
from typing import TypeVar, Generic, Callable

from BaseClasses import Location

A = TypeVar('A')
B = TypeVar('B')


class DeriveDataclassLFunctor(Generic[A]):
    # TODO fix this type
    @classmethod
    def deep_empty(cls) -> typing.Any:
        fields = dataclasses.fields(cls)
        new_fields = {}
        for field in fields:
            if field.type == A:
                new_fields[field.name] = None
            elif field.type == typing.Optional[A]:
                new_fields[field.name] = None
            elif issubclass(typing.get_origin(field.type), DeriveDataclassLFunctor):
                # TODO verify the relationship between field.type and DeriveDataclassLFunctor
                new_fields[field.name] = field.type.deep_empty()

        return cls(**new_fields)

    # TODO can't fix this type because Python has no notion of (∀α.(α→α))
    def map(self, f: Callable[[any], any]) -> typing.Any:
        fields = dataclasses.fields(type(self))
        new_fields = {}
        for field in fields:
            new_fields[field.name] = f(getattr(self, field.name))

        return (type(self))(**new_fields)

    # TODO fix this type
    def lmap(self, ctx: list[str], f: Callable[[list[str], A], B]) -> typing.Any:
        fields = dataclasses.fields(type(self))
        new_fields = {}
        for field in fields:
            if field.type == A:
                new_fields[field.name] = f(ctx + [field.name], getattr(self, field.name))
            elif field.type == typing.Optional[A]:
                if getattr(self, field.name) is None:
                    new_fields[field.name] = None
                else:
                    new_fields[field.name] = f(ctx + [field.name], getattr(self, field.name))
            elif issubclass(typing.get_origin(field.type), DeriveDataclassLFunctor):
                # TODO verify the relationship between field.type and DeriveDataclassLFunctor
                new_fields[field.name] = getattr(self, field.name).lmap(ctx + [field.name], f)

        return (type(self))(**new_fields)

    def lforeach(self, ctx: list[str], f: Callable[[list[str], A | None], None]) -> None:
        fields = dataclasses.fields(type(self))
        for field in fields:
            if field.type == A:
                f(ctx + [field.name], getattr(self, field.name))
            elif field.type == typing.Optional[A]:
                f(ctx + [field.name], getattr(self, field.name))
            elif issubclass(typing.get_origin(field.type), DeriveDataclassLFunctor):
                # TODO verify the relationship between field.type and DeriveDataclassLFunctor
                getattr(self, field.name).lforeach(ctx + [field.name], f)

    def lget(self, path: list[str]) -> A | None:
        fields = dataclasses.fields(type(self))
        for field in fields:
            if field.name == path[0]:
                if len(path) > 1:
                    return getattr(self, field.name).lget(path[1:])
                else:
                    return getattr(self, field.name)
        return None


@dataclass
class NeonWhiteLocationsQuest(DeriveDataclassLFunctor[A]):
    clear: A | None = None


@dataclass
class NeonWhiteLocationsJobMedals(DeriveDataclassLFunctor[A]):
    bronze: A | None = None
    silver: A | None = None
    gold: A | None = None
    ace: A | None = None
    author: A | None = None


@dataclass
class NeonWhiteLocationsJobGift(NeonWhiteLocationsJobMedals[A]):
    gift: A | None = None


@dataclass
class NeonWhiteLocationsMission01(DeriveDataclassLFunctor[A]):
    l01_movement: NeonWhiteLocationsJobGift[A]
    l02_pummel: NeonWhiteLocationsJobGift[A]
    l03_gunner: NeonWhiteLocationsJobGift[A]
    l04_cascade: NeonWhiteLocationsJobGift[A]
    l05_elevate: NeonWhiteLocationsJobGift[A]
    l06_bounce: NeonWhiteLocationsJobGift[A]
    l07_purify: NeonWhiteLocationsJobGift[A]
    l08_climb: NeonWhiteLocationsJobGift[A]
    l09_fasttrack: NeonWhiteLocationsJobGift[A]
    l10_glass_port: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission01[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission02(DeriveDataclassLFunctor[A]):
    l01_take_flight: NeonWhiteLocationsJobGift[A]
    l02_godspeed: NeonWhiteLocationsJobGift[A]
    l03_dasher: NeonWhiteLocationsJobGift[A]
    l04_thrasher: NeonWhiteLocationsJobGift[A]
    l05_outstretched: NeonWhiteLocationsJobGift[A]
    l06_smackdown: NeonWhiteLocationsJobGift[A]
    l07_catwalk: NeonWhiteLocationsJobGift[A]
    l08_fastlane: NeonWhiteLocationsJobGift[A]
    l09_distinguish: NeonWhiteLocationsJobGift[A]
    l10_dancer: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission02[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission03(DeriveDataclassLFunctor[A]):
    l01_guardian: NeonWhiteLocationsJobGift[A]
    l02_stomp: NeonWhiteLocationsJobGift[A]
    l03_jumper: NeonWhiteLocationsJobGift[A]
    l04_dash_tower: NeonWhiteLocationsJobGift[A]
    l05_descent: NeonWhiteLocationsJobGift[A]
    l06_driller: NeonWhiteLocationsJobGift[A]
    l07_canals: NeonWhiteLocationsJobGift[A]
    l08_sprint: NeonWhiteLocationsJobGift[A]
    l09_mountain: NeonWhiteLocationsJobGift[A]
    l10_superkinetic: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission03[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission04(DeriveDataclassLFunctor[A]):
    l01_arrival: NeonWhiteLocationsJobGift[A]
    l02_forgotten_city: NeonWhiteLocationsJobGift[A]
    l03_clocktower: NeonWhiteLocationsJobMedals[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission04[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission05(DeriveDataclassLFunctor[A]):
    l01_fireball: NeonWhiteLocationsJobGift[A]
    l02_ringer: NeonWhiteLocationsJobGift[A]
    l03_cleaner: NeonWhiteLocationsJobGift[A]
    l04_warehouse: NeonWhiteLocationsJobGift[A]
    l05_boom: NeonWhiteLocationsJobGift[A]
    l06_streets: NeonWhiteLocationsJobGift[A]
    l07_steps: NeonWhiteLocationsJobGift[A]
    l08_demolition: NeonWhiteLocationsJobGift[A]
    l09_arcs: NeonWhiteLocationsJobGift[A]
    l10_apartment: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission05[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission06(DeriveDataclassLFunctor[A]):
    l01_hanging_gardens: NeonWhiteLocationsJobGift[A]
    l02_tangled: NeonWhiteLocationsJobGift[A]
    l03_waterworks: NeonWhiteLocationsJobGift[A]
    l04_killswitch: NeonWhiteLocationsJobGift[A]
    l05_falling: NeonWhiteLocationsJobGift[A]
    l06_shocker: NeonWhiteLocationsJobGift[A]
    l07_bouquet: NeonWhiteLocationsJobGift[A]
    l08_prepare: NeonWhiteLocationsJobGift[A]
    l09_triptrack: NeonWhiteLocationsJobGift[A]
    l10_race: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission06[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission07(DeriveDataclassLFunctor[A]):
    l01_bubble: NeonWhiteLocationsJobGift[A]
    l02_shield: NeonWhiteLocationsJobGift[A]
    l03_overlook: NeonWhiteLocationsJobGift[A]
    l04_pop: NeonWhiteLocationsJobGift[A]
    l05_minefield: NeonWhiteLocationsJobGift[A]
    l06_mimic: NeonWhiteLocationsJobGift[A]
    l07_trigger: NeonWhiteLocationsJobGift[A]
    l08_greenhouse: NeonWhiteLocationsJobGift[A]
    l09_sweep: NeonWhiteLocationsJobGift[A]
    l10_fuse: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission07[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission08(DeriveDataclassLFunctor[A]):
    l01_heavens_edge: NeonWhiteLocationsJobGift[A]
    l02_zipline: NeonWhiteLocationsJobGift[A]
    l03_swing: NeonWhiteLocationsJobGift[A]
    l04_chute: NeonWhiteLocationsJobGift[A]
    l05_crash: NeonWhiteLocationsJobGift[A]
    l06_ascent: NeonWhiteLocationsJobGift[A]
    l07_straightaway: NeonWhiteLocationsJobGift[A]
    l08_firecracker: NeonWhiteLocationsJobGift[A]
    l09_streak: NeonWhiteLocationsJobGift[A]
    l10_mirror: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission08[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission09(DeriveDataclassLFunctor[A]):
    l01_escalation: NeonWhiteLocationsJobGift[A]
    l02_bolt: NeonWhiteLocationsJobGift[A]
    l03_godstreak: NeonWhiteLocationsJobGift[A]
    l04_plunge: NeonWhiteLocationsJobGift[A]
    l05_mayhem: NeonWhiteLocationsJobGift[A]
    l06_barrage: NeonWhiteLocationsJobGift[A]
    l07_estate: NeonWhiteLocationsJobGift[A]
    l08_trapwire: NeonWhiteLocationsJobGift[A]
    l09_ricochet: NeonWhiteLocationsJobGift[A]
    l10_fortress: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission09[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission10(DeriveDataclassLFunctor[A]):
    l01_holy_ground: NeonWhiteLocationsJobGift[A]
    l02_the_third_temple: NeonWhiteLocationsJobMedals[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission10[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission11(DeriveDataclassLFunctor[A]):
    l01_spree: NeonWhiteLocationsJobGift[A]
    l02_breakthrough: NeonWhiteLocationsJobGift[A]
    l03_glide: NeonWhiteLocationsJobGift[A]
    l04_closer: NeonWhiteLocationsJobGift[A]
    l05_hike: NeonWhiteLocationsJobGift[A]
    l06_switch: NeonWhiteLocationsJobGift[A]
    l07_access: NeonWhiteLocationsJobGift[A]
    l08_congregation: NeonWhiteLocationsJobGift[A]
    l09_sequence: NeonWhiteLocationsJobGift[A]
    l10_marathon: NeonWhiteLocationsJobGift[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission11[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsMission12(DeriveDataclassLFunctor[A]):
    l01_sacrifice: NeonWhiteLocationsJobMedals[A]
    l02_absolution: NeonWhiteLocationsJobMedals[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsMission12[A]':
        return self.map(f)


@dataclass
class NeonWhiteLocationsJobs(DeriveDataclassLFunctor[A]):
    m01_rebirth: NeonWhiteLocationsMission01[A]
    m02_killer_inside: NeonWhiteLocationsMission02[A]
    m03_only_shallow: NeonWhiteLocationsMission03[A]
    m04_the_old_city: NeonWhiteLocationsMission04[A]
    m05_the_burn_that_cures: NeonWhiteLocationsMission05[A]
    m06_covenant: NeonWhiteLocationsMission06[A]
    m07_reckoning: NeonWhiteLocationsMission07[A]
    m08_benediction: NeonWhiteLocationsMission08[A]
    m09_apocrypha: NeonWhiteLocationsMission09[A]
    m10_the_third_temple: NeonWhiteLocationsMission10[A]
    m11_thousand_pound_butterfly: NeonWhiteLocationsMission11[A]
    m12_hand_of_god: NeonWhiteLocationsMission12[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobGift[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocationsJobs[A]':
        return self.map(lambda a: a.map_medals(f))


@dataclass
class NeonWhiteLocationsSidequestsRed(DeriveDataclassLFunctor[A]):
    s1_elevate_traversal_1: A
    s2_elevate_traversal_2: A
    s3_purify_traversal: A
    s4_godspeed_traversal: A
    s5_stomp_traversal: A
    s6_fireball_traversal: A
    s7_dominion_traversal: A
    s8_book_of_life_traversal: A


@dataclass
class NeonWhiteLocationsSidequestsViolet(DeriveDataclassLFunctor[A]):
    s1_doghouse: A
    s2_choker: A
    s3_chain: A
    s4_hellevator: A
    s5_razor: A
    s6_all_seeing_eye: A
    s7_resident_saw_1: A
    s8_resident_saw_2: A


@dataclass
class NeonWhiteLocationsSidequestsYellow(DeriveDataclassLFunctor[A]):
    s1_sunset_flip_powerbomb: A
    s2_balloon_mountain: A
    s3_climbing_gym: A
    s4_fisherman_suplex: A
    s5_stf: A
    s6_arena: A
    s7_attitude_adjustment: A
    s8_rocket: A


@dataclass
class NeonWhiteLocationsSidequests(DeriveDataclassLFunctor[A]):
    red: NeonWhiteLocationsSidequestsRed[A]
    violet: NeonWhiteLocationsSidequestsViolet[A]
    yellow: NeonWhiteLocationsSidequestsYellow[A]


@dataclass
class NeonWhiteLocations(DeriveDataclassLFunctor[A]):
    jobs: NeonWhiteLocationsJobs[A]
    sidequests: NeonWhiteLocationsSidequests[A]

    def map_medals(self,
                   f: Callable[[NeonWhiteLocationsJobMedals[A]], NeonWhiteLocationsJobMedals[A]]
                   ) -> 'NeonWhiteLocations[A]':
        mapped = dataclasses.replace(self)
        mapped.jobs = mapped.jobs.map_medals(f)
        return mapped


base_location_namespace = 2874297668500000

job_bronze_offset = 1000
job_silver_offset = 2000
job_gold_offset = 3000
job_ace_offset = 4000
job_author_offset = 5000
job_gift_offset = 6000
sidequest_offset = 7000

job_names = [
    [
        'Movement',
        'Pummel',
        'Gunner',
        'Cascade',
        'Elevate',
        'Bounce',
        'Purify',
        'Climb',
        'Fasttrack',
        'Glass Port'
    ],
    [
        'Take Flight',
        'Godspeed',
        'Dasher',
        'Thrasher',
        'Outstretched',
        'Smackdown',
        'Catwalk',
        'Fastlane',
        'Distinguish',
        'Dancer'
    ],
    [
        'Guardian',
        'Stomp',
        'Jumper',
        'Dash Tower',
        'Descent',
        'Driller',
        'Canals',
        'Sprint',
        'Mountain',
        'Superkinetic'
    ],
    [
        'Arrival',
        'Forgotten City',
        'Clocktower'
    ],
    [
        'Fireball',
        'Ringer',
        'Cleaner',
        'Warehouse',
        'Boom',
        'Streets',
        'Steps',
        'Demolition',
        'Arcs',
        'Apartment'
    ],
    [
        'Hanging Gardens',
        'Tangled',
        'Waterworks',
        'Killswitch',
        'Falling',
        'Shocker',
        'Bouquet',
        'Prepare',
        'Triptrack',
        'Race'
    ],
    [
        'Bubble',
        'Shield',
        'Overlook',
        'Pop',
        'Minefield',
        'Mimic',
        'Trigger',
        'Greenhouse',
        'Sweep',
        'Fuse'
    ],
    [
        'Heavens Edge',
        'Zipline',
        'Swing',
        'Chute',
        'Crash',
        'Ascent',
        'Straightaway',
        'Firecracker',
        'Streak',
        'Mirror'
    ],
    [
        'Escalation',
        'Bolt',
        'Godstreak',
        'Plunge',
        'Mayhem',
        'Barrage',
        'Estate',
        'Trapwire',
        'Ricochet',
        'Fortress'
    ],
    [
        'Holy Ground',
        'The Third Temple'
    ],
    [
        'Spree',
        'Breakthrough',
        'Glide',
        'Closer',
        'Hike',
        'Switch',
        'Access',
        'Congregation',
        'Sequence',
        'Marathon'
    ],
    [
        'Sacrifice',
        'Absolution'
    ]
]

giftless_jobs = {'Clocktower', 'The Third Temple', 'Sacrifice', 'Absolution'}

companion_sidequests = [
    ('Red', [
        'Elevate Traversal I',
        'Elevate Traversal II',
        'Purify Traversal',
        'Godspeed Traversal',
        'Stomp Traversal',
        'Fireball Traversal',
        'Dominion Traversal',
        'Book of Life Traversal'
    ]),
    ('Violet', [
        'Doghouse',
        'Choker',
        'Chain',
        'Hellevator',
        'Razor',
        'All Seeing Eye',
        'Resident Saw I',
        'Resident Saw II'
    ]),
    ('Yellow', [
        'Sunset Flip Powerbomb',
        'Balloon Mountain',
        'Climbing Gym',
        'Fisherman Suplex',
        'STF',
        'Arena',
        'Attitude Adjustment',
        'Rocket'
    ])
]

all_locations = []
location_name_to_id = {}
location_name_to_path = {}
location_name_lfunct: NeonWhiteLocations[str] = NeonWhiteLocations.deep_empty()

medal_name_offsets = [
    ('Bronze', job_bronze_offset),
    ('Silver', job_silver_offset),
    ('Gold', job_gold_offset),
    ('Ace', job_ace_offset),
    ('Author', job_author_offset)
]

total_job_id = 0
chapter_idx = 0
for chapter_field in dataclasses.fields(location_name_lfunct.jobs):
    chapter_path = ["jobs", chapter_field.name]
    chapter_lfunct = getattr(location_name_lfunct.jobs, chapter_field.name)
    job_name_list = job_names[chapter_idx]
    job_idx = 0
    for job_field in dataclasses.fields(chapter_lfunct):
        job_path = chapter_path + [job_field.name]
        job_lfunct = getattr(chapter_lfunct, job_field.name)
        job_full_name = f'M{chapter_idx + 1:02d}L{job_idx + 1:02d} {job_name_list[job_idx]}'

        for (medal_name, offset) in medal_name_offsets:
            medal_field_name = medal_name.lower()
            medal_path = job_path + [medal_field_name]
            medal_full_name = f'{job_full_name}: {medal_name}'
            location_name_to_id[medal_full_name] = base_location_namespace + offset + total_job_id
            location_name_to_path[medal_full_name] = medal_path
            setattr(job_lfunct, medal_field_name, medal_full_name)
            all_locations.append(medal_full_name)

        if hasattr(job_lfunct, 'gift'):
            gift_path = job_path + ["gift"]
            gift_full_name = f'{job_full_name}: Gift'
            location_name_to_id[gift_full_name] = base_location_namespace + job_gift_offset + total_job_id
            location_name_to_path[gift_full_name] = gift_path
            setattr(job_lfunct, 'gift', gift_full_name)
            all_locations.append(gift_full_name)

        total_job_id += 1
        job_idx += 1

    chapter_idx += 1

total_sidequest_id = 0
companion_idx = 0
for companion_field in dataclasses.fields(location_name_lfunct.sidequests):
    companion_path = ["sidequests", companion_field.name]
    companion_lfunct = getattr(location_name_lfunct.sidequests, companion_field.name)
    (companion_name, companion_list) = companion_sidequests[companion_idx]
    sidequest_idx = 0
    for sidequest_field in dataclasses.fields(companion_lfunct):
        sidequest_clear_path = companion_path + [sidequest_field.name]
        sidequest_full_name = f'{companion_name}: {companion_list[sidequest_idx]}'

        location_name_to_id[sidequest_full_name] = base_location_namespace + sidequest_offset + total_sidequest_id
        location_name_to_path[sidequest_full_name] = sidequest_clear_path
        setattr(companion_lfunct, sidequest_field.name, sidequest_full_name)
        all_locations.append(sidequest_full_name)

        total_sidequest_id += 1
        sidequest_idx += 1

    companion_idx += 1


class NeonWhiteLocation(Location):
    game: str = "Neon White"
