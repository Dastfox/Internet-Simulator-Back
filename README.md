# Clone repo
git clone git@github.com:Dastfox/FastApi.git

# delete previous conda env if any
conda deactivate
conda env remove --name env_FastAPI

# create env
conda create -n env_FastAPI python=3.8.8 -y
conda install --force-reinstall -y -q --name env_FastAPI -c conda-forge --file requirements.txt


# activate env
conda activate env_FastAPI

# Launch app
start http://localhost:8000/docs && uvicorn src.main:app --reload 


