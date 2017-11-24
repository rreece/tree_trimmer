"""
A tree_trimmer.py skim function
"""


def skim(ch):
    import math
    GeV = 1000.

    ## check triggers
    triggers = ["EF_e24vhi_medium1", "EF_e60_medium1", "EF_tau20Ti_medium1_e18vh_medium1", "EF_e18vh_medium1_vbf_2L1TAU11I_EM14VH"]
    passed_trigger = False
    for trigger in triggers:
        if hasattr(ch, trigger) and getattr(ch, trigger):
            passed_trigger = True
            break

    if not passed_trigger:
        return False

    ## select electrons
    el_indexes = []
    el_n = ch.el_n
    for i_el in xrange(el_n):
        if ch.el_nSCTHits[i_el] + ch.el_nPixHits[i_el] < 4:
            pt = ch.el_cl_E[i_el]/math.cosh(ch.el_cl_eta[i_el])
        else:
            pt = ch.el_cl_E[i_el]/math.cosh(ch.el_tracketa[i_el])
        if pt > 30*GeV and ch.el_loosePP[i_el]:
            el_indexes.append(i_el)

    if not el_indexes:
        return False

    ## select taus
    tau_indexes = []
    tau_n = ch.tau_n
    for i_tau in xrange(tau_n):
        if ch.tau_pt[i_tau] > 35*GeV and ch.tau_numTrack[i_tau] in (1, 2, 3):
            tau_indexes.append(i_tau)

    if not tau_indexes:
        return False

    ## build electron TLVs
    el_tlvs = []
    for i_el in el_indexes:
        tlv = ROOT.TLorentzVector()
        if ch.el_nSCTHits[i_el] + ch.el_nPixHits[i_el] < 4:
            tlv.SetPtEtaPhiM(ch.el_cl_E[i_el]/math.cosh(ch.el_cl_eta[i_el]), ch.el_cl_eta[i_el], ch.el_cl_phi[i_el], 0.0)
        else:
            tlv.SetPtEtaPhiM(ch.el_cl_E[i_el]/math.cosh(ch.el_tracketa[i_el]), ch.el_tracketa[i_el], ch.el_trackphi[i_el], 0.0)
        el_tlvs.append(tlv)

    ## build tau TLVs
    tau_tlvs = []
    for i_tau in tau_indexes:
        tlv = ROOT.TLorentzVector()
        tlv.SetPtEtaPhiM(ch.tau_pt[i_tau], ch.tau_eta[i_tau], ch.tau_phi[i_tau], ch.tau_m[i_tau])
        tau_tlvs.append(tlv)

    ## overlap removal
    olr_tau_tlvs = []
    for tau_tlv in tau_tlvs:
        has_overlap = False
        for el_tlv in el_tlvs:
            if tau_tlv.DeltaR(el_tlv) < 0.2:
                has_overlap = True
                break
        if not has_overlap:
            olr_tau_tlvs.append(tau_tlv)

    return passed_trigger and el_tlvs and olr_tau_tlvs

# EOF
