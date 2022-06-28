# Clone repo
git clone git@github.com:Dastfox/FastApi.git

# delete previous conda env if any
conda deactivate
conda env remove --name FastAPI

# create env
conda create -n .env_FastAPI python=3.8.8 -y
conda install --force-reinstall -y -q --name FastAPI -c conda-forge --file requirements.txt

# activate env
conda activate FastAPI

# Launch app
cd src && start http://localhost:8000 && uvicorn main:app --reload 


