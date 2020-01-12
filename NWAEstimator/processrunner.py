import subprocess
import card_maker
import os.path
import sys
sys.path.append('../')
from VLQCouplingCalculator import VLQCouplingCalculator as vlq

def processor(outdir, outfile, run_command, runname, mode, m, k, xiW, xiZ, xiH):

    if not (os.path.exists(outdir) and os.path.exists(outfile)):
        subprocess.call([run_command, runname, "-f"])
        
    if not (os.path.exists(outdir) and os.path.exists(outfile)):
        print "Something went wrong! Maybe MG didn't run properly. Retrying for m = %i, cw = %i and cz = %i" %(m, cw, cz)
        print outdir, outfile
        card_maker.param_editor(mode, m, k, xiW, xiZ, xiH)
        card_maker.run_editor(mode, "_00")
        processor(outdir, outfile, run_command, runname, mode, m, k, xiW, xiZ, xiH)

def processor_new(outdir, outfile, run_command, runname, mode, proc, m, kW, kZ, kH):

    if not (os.path.exists(outdir) and os.path.exists(outfile)):
        subprocess.call([run_command, runname, "-f"])
        
    if not (os.path.exists(outdir) and os.path.exists(outfile)):
        print "Something went wrong! Maybe MG didn't run properly. Retrying for m = %i, c1 = %i and c2 = %i" %(m, c1, c2)
        print outdir, outfile
        card_maker.param_editor_new(mode, proc, m, kW, kZ, kH)
        card_maker.run_editor(mode, proc, "_00")
        processor_new(outdir, outfile, run_command, runname, mode, proc, m, kW, kZ, kH)

try:
    proc = sys.argv[1]
except:
    print "No process specified. Exiting"
    sys.exit(1)

basedir = "../"
decay_dir = basedir + "MG5_aMC_v2_6_5/VLQ_" + proc + "_DECAY/"
nodecay_dir = basedir + "MG5_aMC_v2_6_5/VLQ_" + proc + "_NODECAY/"

XS_DOC_0 = open("Data/xs_table_" + proc + ".txt","w")
##XS_DOC_1 = open("xs_table_chcz_mode.txt","w")

masses = range(10,24,2)

if proc[0] == 'W' and proc[2] in ['W','Z']:
    cws = range(2,12,2) + [0.5]
    if proc[1] in ['X','Y']:
        czs = [0]
    else:
        czs = range(2,12,2) + [0.5]
    chs = [0]
    c1s = cws
    c2s = czs
    c3s = chs
    seq = 'wzh'
elif proc[0] == 'W' and proc[2] == 'H':
    cws = chs = range(2,12,2) + [0.5]
    czs = [0]
    c1s = cws
    c2s = chs
    c3s = czs
    seq = 'whz'
elif proc[0] == 'Z' and proc[2] in ['H','Z']:
    chs = czs = range(2,12,2) + [0.5]
    cws = [0]
    c1s = czs
    c2s = chs
    c3s = cws
    seq = 'zhw'
elif proc[0] == 'Z' and proc[2] == 'W':
    cws = czs = range(2,12,2) + [0.5]
    chs = [0]
    c1s = czs
    c2s = cws
    c3s = chs
    seq = 'zwh'

cws = chs = range(0,11,2) + [0.5]
czs = [0]
c = vlq()

for m in masses:
    c1s_done = {}
    for c1 in c1s:
        if c1 == 0: continue
        if proc[0] == 'W': runname_nodec = 'RUN_M_' + str(m*100) + '_CW_' + str(c1)
        else: runname_nodec = 'RUN_M_' + str(m*100) + '_CZ_' + str(c1)
        for c2 in c2s:
            #if c2 == 0: continue
            for c3 in c3s + [c2]:
                if seq == 'wzh':
                    runname_dec = 'RUN_M_' + str(m*100) + '_CW_' + str(c1) + '_CZ_' + str(c2) + '_CH_' + str(c3)
                    _cw = c1/10.0
                    _cz = c2/10.0
                    _ch = c3/10.0
                elif seq == 'whz':
                    runname_dec = 'RUN_M_' + str(m*100) + '_CW_' + str(c1) + '_CZ_' + str(c3) + '_CH_' + str(c2)
                    _cw = c1/10.0
                    _cz = c3/10.0
                    _ch = c2/10.0
                elif seq == 'zwh':
                    runname_dec = 'RUN_M_' + str(m*100) + '_CW_' + str(c2) + '_CZ_' + str(c1) + '_CH_' + str(c3)
                    _cw = c2/10.0
                    _cz = c1/10.0
                    _ch = c3/10.0
                elif seq == 'zhw':
                    runname_dec = 'RUN_M_' + str(m*100) + '_CW_' + str(c3) + '_CZ_' + str(c1) + '_CH_' + str(c2)
                    _cw = c3/10.0
                    _cz = c1/10.0
                    _ch = c2/10.0

                _m = m*100.0
                
                c.setMVLQ(_m)
                c.setc_Vals(_cw, _cz, _ch)
                v = c.getKappas()
                print v
                #_k = v[0]
                _kW = v[0]
                _kZ = v[1]
                _kH = v[2]

                # if _kH == 0.:
                #     _kH = 0.00001
                #     #_kZ = _kZ - _kH
                # elif _kZ == 0.:
                #     _kZ = 0.00001
                #     #_kH = _kH - 0.00001

                card_maker.param_editor_new("NODECAY", proc, _m, _kW, _kZ, _kH)
                card_maker.param_editor_new("DECAY", proc, _m, _kW, _kZ, _kH)
                #card_maker.param_editor("DECAY",_m, _k, _xiW, _xiZ, _xiH)
                card_maker.run_editor("NODECAY",proc,"_00")
                card_maker.run_editor("DECAY",proc,"_00")

                # For allowing decay
                outdir = decay_dir + "Events/" + runname_dec
                outfile = outdir + "/" + runname_dec + "__00_banner.txt"
                run_command = decay_dir + "bin/generate_events"

                print outdir
                print outfile

                #processor(outdir, outfile, run_command, runname_dec, "DECAY",_m, _k, _xiW, _xiZ, _xiH)
                processor_new(outdir, outfile, run_command, runname_dec, "DECAY", proc, _m, _kW, _kZ, _kH)

                decay_file = open(outfile, "r")

                for line in decay_file:
                    if '(pb)' in line:
                        val = line.split()
                        try:
                            xs_decay = float(val[5])
                        except:
                            print "something is wrong! This is val: ", val, "Aborting DECAY for m = %i, cw = %i and cz = %i" %(m, cw, cz)
                            continue

                decay_file.close()

                # For without decay 
                outdir = nodecay_dir + "Events/" + runname_nodec
                outfile = outdir + "/" + runname_nodec + "__00_banner.txt"
                run_command = nodecay_dir + "bin/generate_events"

                print outdir
                print outfile
                print "c1s done so far: ", c1s_done.keys()

                if c1 not in c1s_done.keys():

                    #processor(outdir, outfile, run_command, runname_nodec, "NODECAY", _m, _k, _xiW, _xiZ, _xiH)
                    processor_new(outdir, outfile, run_command, runname_nodec, "NODECAY", proc, _m, _kW, _kZ, _kH)

                    nodecay_file = open(outfile, "r")

                    for line in nodecay_file:
                        if '(pb)' in line:
                            val = line.split()
                            try:
                                xs_nodecay = float(val[5])
                            except:
                                print "something is wrong! This is val: ", val, "Aborting NODECAY for m = %i, cw = %i and cz = %i" %(m, cw, cz)
                                continue

                    nodecay_file.close()
                    c1s_done[c1] = xs_nodecay
                else:

                    xs_nodecay = c1s_done[c1]

                s = str(m) + " " +  str(_cw) + " " + str(_cz) + " " + str(_ch) + " " + str(xs_nodecay) + " " + str(xs_decay) + " \n"
                XS_DOC_0.write(s)
                # if ch == 0:
                #     XS_DOC_0.write(s)
                #     XS_DOC_0.flush()
                # else:
                #     XS_DOC_1.write(s)
                #     XS_DOC_1.flush()
                
XS_DOC_0.close()
#XS_DOC_1.close()
