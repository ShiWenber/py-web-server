$project_name='py-web-server'


deactivate

if((test-path .\Scripts\activate) -eq "False")
{
    cd ..
    python -m venv $project_name
    cd $project_name
}
.\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
