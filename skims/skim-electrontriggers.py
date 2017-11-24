"""
A tree_trimmer.py skim function to accept things firing electron triggers.
"""

def skim(ch):
    for trigger in ["EF_e24vhi_medium1", "EF_e60_medium1", "EF_tau20Ti_medium1_e18vh_medium1", "EF_e18vh_medium1_vbf_2L1TAU11I_EM14VH"]:
        if hasattr(ch, trigger) and getattr(ch, trigger):
            return True
    return False

# EOF
