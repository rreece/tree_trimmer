"""
A tree_trimmer.py skim function to accept things firing muon triggers.
"""

def skim(ch):
    for trigger in ["EF_mu24i_tight", "EF_mu36_tight", "EF_tau20_medium1_mu15", "EF_mu15_vbf_L1TAU8_MU10"]:
        if hasattr(ch, trigger) and getattr(ch, trigger):
            return True
    return False

# EOF
