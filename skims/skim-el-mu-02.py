"""
A tree_trimmer.py skim function
"""


def skim(ch):
    import math
    GeV = 1000.

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

    ## select muons
    mu_indexes = []
    mu_n = ch.mu_staco_n
    for i_mu in xrange(mu_n):
        if ch.mu_staco_pt[i_mu] > 20*GeV and ch.mu_staco_loose[i_mu]:
            mu_indexes.append(i_mu)

    if not mu_indexes:
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

    ## build muon TLVs
    mu_tlvs = []
    for i_mu in mu_indexes:
        tlv = ROOT.TLorentzVector()
        tlv.SetPtEtaPhiM(ch.mu_staco_pt[i_mu], ch.mu_staco_eta[i_mu], ch.mu_staco_phi[i_mu], ch.mu_staco_m[i_mu])
        mu_tlvs.append(tlv)

    ## overlap removal
    has_non_overlap_cand = False
    for mu_tlv in mu_tlvs:
        for el_tlv in el_tlvs:
            if mu_tlv.DeltaR(el_tlv) > 0.2:
                has_non_overlap_cand = True
                break

    return has_non_overlap_cand

# EOF
