deactivate
if((test-path .\Scripts\activate) -eq "False")
{
    cd ..
    python -m venv ASSOY
    cd ASSOY
}
.\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt