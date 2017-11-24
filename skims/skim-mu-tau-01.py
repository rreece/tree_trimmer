"""
A tree_trimmer.py skim function to accept things firing muon triggers.
"""

def skim(ch):
    GeV = 1000.

    ## check triggers
    triggers = ["EF_mu24i_tight", "EF_mu36_tight", "EF_tau20_medium1_mu15", "EF_mu15_vbf_L1TAU8_MU10"]
    passed_trigger = False
    for trigger in triggers:
        if hasattr(ch, trigger) and getattr(ch, trigger):
            passed_trigger = True
            break

    if not passed_trigger:
        return False

    ## select muons
    mu_indexes = []
    mu_n = ch.mu_staco_n
    for i_mu in xrange(mu_n):
        if ch.mu_staco_pt[i_mu] > 30*GeV and ch.mu_staco_loose[i_mu]:
            mu_indexes.append(i_mu)

    if not mu_indexes:
        return False

    ## select taus
    tau_indexes = []
    tau_n = ch.tau_n
    for i_tau in xrange(tau_n):
        if ch.tau_pt[i_tau] > 35*GeV and ch.tau_numTrack[i_tau] in (1, 2, 3):
            tau_indexes.append(i_tau)

    if not tau_indexes:
        return False

    ## build muon TLVs
    mu_tlvs = []
    for i_mu in mu_indexes:
        tlv = ROOT.TLorentzVector()
        tlv.SetPtEtaPhiM(ch.mu_staco_pt[i_mu], ch.mu_staco_eta[i_mu], ch.mu_staco_phi[i_mu], ch.mu_staco_m[i_mu])
        mu_tlvs.append(tlv)

    ## build tau TLVs
    tau_tlvs = []
    for i_tau in tau_indexes:
        tlv = ROOT.TLorentzVector()
        tlv.SetPtEtaPhiM(ch.tau_pt[i_tau], ch.tau_eta[i_tau], ch.tau_phi[i_tau], ch.tau_m[i_tau])
        tau_tlvs.append(tlv)

    ## overlap removal
    has_non_overlap_cand = False
    for tau_tlv in tau_tlvs:
        for mu_tlv in mu_tlvs:
            if tau_tlv.DeltaR(mu_tlv) > 0.2:
                has_non_overlap_cand = True
                break

    return passed_trigger and has_non_overlap_cand

# EOF
