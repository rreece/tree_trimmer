#!/usr/bin/env python

# prun  --exec "python tree_trimmer.py - -b vars_v01.txt -s skim -k tauPerfMeta/TrigConfTree skim_mu.py %IN" --inDS user.reece.data11_7TeV.periodF.muons.tauPerf-01-01-02.D3PD.01/ --outDS user.reece.data11_7TeV.periodF.muons.tauPerf-01-01-02.D3PD.v01.skim_mu.02/ --outputs skim.root --athenaTag=16.6.6 --destSE=UPENN_LOCALGROUPDISK --nGBPerJob=4

import argparse, sys, os
import copy

import samples

#------------------------------------------------------------------------------
def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--d3pds"       , type=str, default=''      , help='')
    parser.add_argument("--samples"     , type=str, default=''      , help='')
    parser.add_argument("--athenaTag"   , type=str, default='17.2.7', help='')
    parser.add_argument("--destSE"      , type=str, default=''      , help='')
    parser.add_argument("--excludedSite", type=str, default=''      , help='')
    parser.add_argument("--nGBPerJob"   , type=str, default=''      , help='')
    parser.add_argument("--nFilesPerJob", type=str, default=''      , help='')
    parser.add_argument("--skim"        , type=str, default=''      , help='')
    parser.add_argument("--site"        , type=str, default=''      , help='')
    parser.add_argument("--user"        , type=str, default=''      , help='')
    parser.add_argument("--version"     , type=str, default=''      , help='')
    parser.add_argument("--mergeOutput"    , action="store_true", default=False)
    parser.add_argument("--individualOutDS", action="store_true", default=False)
    parser.add_argument("--debug"          , action="store_true", default=False)
    args = parser.parse_args()
#    if not args.skim        : sys.exit(' ERROR: Need txt file --skim with skim function for prun. Exiting.')
#    if not args.user        : sys.exit(' ERROR: Need --user. Exiting.')
#    if not args.version     : sys.exit(' ERROR: Need --version. Exiting.')
    return args


#------------------------------------------------------------------------------
def main():

    args = options()
    log = file('submit.log', 'a')

    #--------------------------------------------------------------------------
    # stable config
    #--------------------------------------------------------------------------
    user = 'reece'
    version = 'v07'
#    skim = 'skims/skim-mu-tau-02.py'
    skim = 'skims/skim-el-mu-02.py'
    tree_trimmer_ops = {
        '-k':   'CollectionTree,tauMeta/TrigConfTree,tauMeta/BunchConfTree',
        '-s':   'skim',
        '-t':   'tau',
        '-B':   'boff/boff-05.txt',
#        '-M':   '4000',
        'args': [''],
        }
    
    prun_ops = {}
    prun_ops['--exec']    = '\"python tree_trimmer.py - %s\"'
    prun_ops['--outputs'] = 'skim.root'
    if args.athenaTag    : prun_ops['--athenaTag']    = args.athenaTag
    if args.site         : prun_ops['--site']         = args.site
    if args.destSE       : prun_ops['--destSE']       = args.destSE
    if args.nGBPerJob    : prun_ops['--nGBPerJob']    = args.nGBPerJob
    if args.nFilesPerJob : prun_ops['--nFilesPerJob'] = args.nFilesPerJob
    if args.excludedSite : prun_ops['--excludedSite'] = args.excludedSite

    #--------------------------------------------------------------------------
    # samples
    #--------------------------------------------------------------------------
    from samples.p1344 import mc
    from samples.p1443 import data

    the_samples = []

#### mu-had samples   #####################################
#    the_samples += mc.ZDYtautaus
#    the_samples += mc.ZDYmumus
#    the_samples += mc.WmunuNpXs
#    the_samples += mc.WtaunuNpXs
#    the_samples += mc.WmunuMassives
#    the_samples += mc.WtaunuMassives
#    the_samples += mc.dibosons
#    the_samples += mc.tops
#    the_samples += mc.Zprimes
#    the_samples += [
#                    data.Muons.periodA,
#                    data.Muons.periodB,
#                    data.Muons.periodC,
#                    data.Muons.periodD,
#                    data.Muons.periodE,
#                   ]
#    the_samples += [
#                    data.Muons.periodG,
#                    data.Muons.periodH,
#                    data.Muons.periodI,
#                    data.Muons.periodJ,
#                    data.Muons.periodL,
#                    ]
#
#### el-mu samples   ######################################
    the_samples += mc.ZDYtautaus
    the_samples += mc.ZeeNpXs
    the_samples += mc.ZmumuNpXs
    the_samples += mc.ZDYees
    the_samples += mc.ZDYmumus
#    the_samples += mc.WenuNpXs
#    the_samples += mc.WmunuNpXs
#    the_samples += mc.WtaunuNpXs
#    the_samples += mc.WenuMassives
#    the_samples += mc.WmunuMassives
#    the_samples += mc.WtaunuMassives
#    the_samples += mc.dibosons
#    the_samples += mc.tops
#    the_samples += mc.Zprimes
#    the_samples += [
#                    data.Egamma.periodA,
#                    data.Egamma.periodB,
#                    data.Egamma.periodC,
#                    data.Egamma.periodD,
#                    data.Egamma.periodE,
#                    ]
#    the_samples += [
#                    ]
#                    data.Egamma.periodG,
#                    data.Egamma.periodH,
#                    data.Egamma.periodI,
#                    data.Egamma.periodJ,
#                    data.Egamma.periodL,
#                    ]
#    the_samples += [
#                    data.Muons.periodA,
#                    data.Muons.periodB,
#                    data.Muons.periodC,
#                    data.Muons.periodD,
#                    data.Muons.periodE,
#                   ]
#    the_samples += [
#                    data.Muons.periodG,
#                    data.Muons.periodH,
#                    data.Muons.periodI,
#                    data.Muons.periodJ,
#                    data.Muons.periodL,
#                    ]

    datasets = []
    for s in the_samples:
        assert len(s.d3pds) == 1
        datasets.append( s.d3pds[0] )

    #--------------------------------------------------------------------------
    for d3pd in datasets:
        tmp_tree_trimmer_ops = copy.deepcopy(tree_trimmer_ops) # deep for args list
        tmp_tree_trimmer_ops['args'].append(skim)
        tmp_tree_trimmer_ops['args'].append('%IN')
    
        tmp_prun_ops = copy.deepcopy(prun_ops)
    
        short_dataset = samples.Sample.shortenD3PD(d3pd).rstrip('/')
    
        outname = '%(inDS)s.%(skim)s.%(version)s/' % {
                'inDS' : short_dataset,
    #            'vars' : os.path.basename(os.path.splitext(tmp_tree_trimmer_ops['-B'])[0]), # vars/vars-01.txt    -> vars-01
                'skim' : os.path.basename(os.path.splitext(skim)[0]),                  # skims/skim-el-01.py -> skim-el-01
                'version' : version,
                }
        if not outname.startswith('user.%s.' % user):
            outname = 'user.%s.%s' % (user, outname)
    
        assert len(outname) <= 132, '%s: %s' % (len(outname), outname)
    
        tmp_prun_ops['--exec'] = tmp_prun_ops['--exec'] % dict_to_cmd(tmp_tree_trimmer_ops)
        tmp_prun_ops['--inDS'] = d3pd
        tmp_prun_ops['--outDS'] = outname
    
        cmd = 'prun %s' % dict_to_cmd(tmp_prun_ops)
        print cmd
        if not args.debug:
            os.system(cmd)
            log.write(cmd + '\n')
    
    log.close()


#------------------------------------------------------------------------------
# misc functions
#------------------------------------------------------------------------------

#______________________________________________________________________________
def parse_input(filename):
    f = open(filename)
    datasets_options = []
    for line in f:
        line = line.split('#')[0].strip() # remove comments
        if line:
            words = line.split()
            dataset = words[0]
            option = ''
            if len(words) > 1:
                option = ' '.join(words[1:])
            datasets_options.append( (dataset, option) )
    f.close()
    return datasets_options

#______________________________________________________________________________
def dict_to_cmd(d):
    a = []
    for key, val in d.iteritems():
        if key.startswith('--'):
            a.append('%s=%s' % (key,val))
        elif key.startswith('-'):
            a.append('%s %s' % (key,val))
        elif key == 'args':
            pass
        else:
            print 'Key: %s is not of cmd opt format (-k or --key).  Ignored.' % key
    a.extend( d.get('args', []) )
    cmd = ' '.join(a)
    return cmd

#______________________________________________________________________________
def lchop(s, x):
    if s.startswith(x):
        return s[len(x):]
    else:
        return s

#______________________________________________________________________________
def rchop(s, x):
    if s.endswith(x):
        return s[:-1*len(x)]
    else:
        return s


#______________________________________________________________________________
if __name__ == '__main__': main()

# EOF

