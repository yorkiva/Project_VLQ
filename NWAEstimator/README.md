Code and Setup for Determining Correction factor for cross-section calculation with Narrow Width Approximation (NWA):

1. Download MadGraph from https://launchpad.net/mg5amcnlo/2.0/2.6.x and the VLQ UFO Model from http://feynrules.irmp.ucl.ac.be/raw-attachment/wiki/NLOModels/vlq_v4_4fns.ufo.tgz
2. Unpack MadGraph within the ../Project_VLQ/ Directory and place the unpacked VLQ UFO model inside the models/ directory in MadGraph
3. Run MadGraph to generate process from the one of the process cards inside the Proc_Cards/ directory
4. Change the MadGraph directory name inside the .py scripts (currently hardcoded!)
5. Run the follwoing command to generate events for a given process:
   	   python processrunner.py <process_name>
6. Step 5 may take a while (10-12 hours)! After that run the following command to obtain the parameterized correction factors
   		python PNWAEstimator_All.py <process_name>
