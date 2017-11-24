tree_trimmer.py
==============================================

A general ROOT tree skimmer and slimmmer.


SYNOPSIS
-------------------------------

    tree_trimmer.py [OPTIONS] file1.root [file2.root ... skim.py] [OPTIONS]


DESCRIPTION
-------------------------------

This is a very general and configurable script for skimming (skipping
events) and slimming (dropping branches) ROOT TTrees.

An example call is:

    tree_trimmer.py -t mytree -b vars.txt -s skim -k 'CollectionTree,tauPerfMeta/TrigConfTree' *.root skim.py

This call would chain together TTrees named 'mytree' in all '*.root' files.
Then it would turn-off the branch status of all branches in mytree, except
for those listed in vars.txt, which can look something like this:

    EventNumber
    RunNumber
    lbn
    el_*

Then, it would skim mytree according to the skim(tree) function specified
with the option -s, and implemented in skim.py.  The additional trees
specified by the option -k, would also be kept in their entirety.

The counts of all events and the events passing the skim are recorded in
the first and second bins of a histogram, 'h_n_events', that is saved in
each output file.


OPTIONS
------------------------------------

    -h, --help
        Prints this docstring and exits.
        
    -b FILE, --branches_on_file=FILE
        When specified, FILE should be the name of a file containing branch
        names, or fnmatch patterns for branch names, one per line.
        (# comments are allowed.)  This specifies the branches that
        should be turned-on, all others are turned-off.

    -B FILE, --branches_off_file=FILE
        When specified, FILE should be the name of a file containing branch
        names, or fnmatch patterns for branch names, one per line.
        (# comments are allowed.)  This specifies the branches that
        should be turned-off, even if they were turned-on in the
        branches_off_file above; good for specifying exceptions.

    -k 'TREE1,DIR/TREE2,...', --keep_trees='TREE1,DIR/TREE2,...'
        Comma-separated names of additional trees (metadata, config, ...) that
        should be coppied in their entirety, in addtion to the main tree being
        skimmed.

    -m NUM, --max_events=NUM
        Max number of events to run over the input trees.

    -M MB, --max_tree_size=MB
        Specifies the ROOT.TTree.SetMaxTreeSize in MB.  By default, ROOT should
        make it 1900 MB.

    -o FILE, --out=FILE
        Specifies the name of the output file, 'skim.root' by default.

    -s FUNC, --skim=FUNC
        Specifies the name of a user-supplied skimming function, FUNC(tree),
        that should return True/False if the current entry in tree passes
        the skim.  The user should implement FUNC in a python file and provide
        it as a command-line argument.  For example, to skim for events that
        have a 20 GeV electron candidate, one could write:

            def skim(ch):
                for i_el in xrange(ch.el_n):
                    if ch.el_pt[i_el] > 20000.0:
                        return True
                return False

    -t NAME, --tree=NAME
        Specifies the name of the main tree to be skimmed (skipping events) and
        slimmed (dropping branches), 'tauPerf' by default.


AUTHOR
------------------------

Ryan Reece  <ryan.reece@cern.ch>


COPYRIGHT
------------------------

Copyright 2011 Ryan Reece          
License: GPL <http://www.gnu.org/licenses/gpl.html>


SEE ALSO
------------------------

ROOT <http://root.cern.ch>


TO DO
------------------------

- Optionally copy all additional objects in input files.  One has to
  pragram support for all ROOT object types that may copy differently,
  and treat the main tree as a special case.
- Does not work if output exceeds one file.  The trees appear to be
  duplicated in the output files.
- Progress bar?


2011-06-15

