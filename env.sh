export STAMPS=$PWD
export PATH=$PATH:$STAMPS/bin

# mt_prep_snap 20150404 $PWD/../sample_data_GR/INSAR_20150404 0.4
## real: 0m3,018s - user: 0m1,733s - sys:  0m1,269s
# calamp calamp.in 1561 /home/antonio/projects/forks/StaMPS/out/calamp.out f 1
## real: 0m0,280s - user: 0m0,271s - sys:  0m0,008s
# selpsc_patch /home/antonio/projects/forks/StaMPS/out/selpsc.in patch.in pscands.1.ij pscands.1.da mean_amp.flt f 1 
## real: 0m0,521s - user: 0m0,475s - sys:  0m0,008s 
# psclonlat /home/antonio/projects/forks/StaMPS/out/psclonlat.in pscands.1.ij pscands.1.ll
## real: 0m0,301s - user: 0m0,108s - sys:  0m0,193s
# pscdem /home/antonio/projects/forks/StaMPS/out/pscdem.in pscands.1.ij pscands.1.hgt
## real: 0m0,168s - user: 0m0,051s - sys:  0m0,100s
# pscphase /home/antonio/projects/forks/StaMPS/out/pscphase.in pscands.1.ij pscands.1.ph
## real: 0m1,919s - user: 0m0,737s - sys:  0m1,134s
