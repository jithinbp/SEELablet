pyuic4 template_experiments.ui -o template_experiments.py 
#pyuic4 icon.ui -o icon.py
#pyuic4 outputs.ui -o outputs.py
#pyuic4 analogScope.ui -o analogScope.py
#pyuic4 transistorCE.ui -o transistorCE.py
#pyuic4 sensorTemplate.ui -o sensorTemplate.py
#pyuic4 wirelessTemplate.ui -o wirelessTemplate.py
#pyuic4 diodeIV.ui -o diodeIV.py
#pyuic4 rectifier.ui -o rectifier.py
#pyuic4 template_transient.ui -o template_transient.py
#pyuic4 arbitStream.ui -o arbitStream.py
cd widgets/
pyuic4 dial.ui -o dial.py 
pyuic4 button.ui -o button.py
pyuic4 selectAndButton.ui -o selectAndButton.py
cd ..
