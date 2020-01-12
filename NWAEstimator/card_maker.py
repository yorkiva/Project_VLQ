def param_editor_new(mode, proc, m, kW, kZ, kH):

    MG_loc = "../MG5_aMC_v2_6_5/"

    if mode == "NODECAY":
        base_dir = "VLQ_" + proc +"_NODECAY"
    elif mode == "DECAY":
        base_dir = "VLQ_" + proc +"_DECAY"
    else:
        print "invalid mode. aborting card editing"
        return -1

    card_dir = MG_loc + base_dir + "/Cards/"
    card_name = card_dir + "param_card.dat"

    card_template = "param_card_mydefault_new.dat"

    f_def = open(card_template, "r")
    newcard = open(card_name, "w")

    for line in f_def:
        if ' # KTLh3 ' in line:
            newcard.write(' 3 %.6f # KTLh3 \n' %(kH))
        elif ' # KBLh3 ' in line:
            newcard.write(' 3 %.6f # KBLh3 \n' %(kH))
        elif ' # MTP ' in line:
            newcard.write(' 6000006 %i # MTP \n'%(m))
        elif ' # MBP ' in line:
            newcard.write(' 6000007 %i # MBP \n'%(m))
        elif ' # MX ' in line:
            newcard.write(' 6000005 %i # MX \n'%(m))
        elif ' # MY ' in line:
            newcard.write(' 6000008 %i # MY \n'%(m))
        elif ' # KTLw3 ' in line:
            newcard.write(' 3 %.6f # KTLw3 \n' %(kW))
        elif ' # KBLw3 ' in line:
            newcard.write(' 3 %.6f # KBLw3 \n' %(kW))
        elif ' # KXL3 ' in line:
            newcard.write(' 3 %.6f # KXL3 \n' %(kW))
        elif ' # KYL3 ' in line:
            newcard.write(' 3 %.6f # KYL3 \n' %(kW))
        elif ' # KTLz3 ' in line:
            newcard.write(' 3 %.6f # KTLz3 \n' %(kZ))
        elif ' # KBLz3 ' in line:
            newcard.write(' 3 %.6f # KBLz3 \n' %(kZ))
        else:
            newcard.write(line)
    f_def.close()
    newcard.close()
    return 1


def run_editor(mode, proc, tag):
    MG_loc = "../MG5_aMC_v2_6_5/"

    if mode == "NODECAY":
        base_dir = "VLQ_" + proc + "_NODECAY"
    elif mode == "DECAY":
        base_dir = "VLQ_" + proc + "_DECAY"
    else:
        print "invalid mode. aborting card editing"
        return -1

    card_dir = MG_loc + base_dir + "/Cards/"
    card_name = card_dir + "run_card.dat"

    card_template = "run_card_mydefault_new.dat"

    f_def = open(card_template, "r")
    newcard = open(card_name, "w")

    for line in f_def:
	if 'name of the run' in line:
            newcard.write('%s = run_tag ! name of the run \n' %(tag))
        else:
            newcard.write(line)

    return 1
        

