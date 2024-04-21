from dataclasses import dataclass

from Options import Toggle, PerGameCommonOptions, DeathLink


class RewardBronzeTrophies(Toggle):
    """Enables Bronze Trophies as locations."""
    display_name = "Reward Bronze Trophies"


class RewardSilverTrophies(Toggle):
    """Enables Silver Trophies as locations."""
    display_name = "Reward Silver Trophies"


class RewardGoldTrophies(Toggle):
    """Enables Gold Trophies as locations."""
    display_name = "Reward Gold Trophies"


class RewardAceTrophies(Toggle):
    """Enables Ace Trophies as locations."""
    display_name = "Reward Ace Trophies"


class RewardAuthorTrophies(Toggle):
    """Enables Author Trophies as locations."""
    display_name = "Reward Author Trophies"


class RewardGifts(Toggle):
    """Enables Gifts as locations."""
    display_name = "Reward Gifts"


class RewardSidequests(Toggle):
    """Enables Sidequests as locations."""
    display_name = "Reward Sidequests"


@dataclass
class NeonWhiteOptions(PerGameCommonOptions):
    reward_bronze_trophies: RewardBronzeTrophies
    reward_silver_trophies: RewardSilverTrophies
    reward_gold_trophies: RewardGoldTrophies
    reward_ace_trophies: RewardAceTrophies
    reward_author_trophies: RewardAuthorTrophies
    reward_gifts: RewardGifts
    reward_sidequests: RewardSidequests
    death_link: DeathLink
