# Blockchain Cryptocurrency Full Model
A complete blockchain model implementing cryptocurrency.

## Features:
- Crypto hashing based on SHA-256 algorithm
- Proof of Work consensus
- Dynamic mine rate difficulty adjustment
- 

## Project also includes:
- Unit tests for all methods (./backend/tests)
- 
-------------

## Command Reference

**Activate the virtual environment**
```
source blockchain-full-env/Scripts/activate
```

**Install all packages and dependencies**
```
pip3 install -r requirements.txt
```

**Run the tests**

*First make sure to Activate the virtual environment (see above)
```
python -m pytest backend/tests
```

**Start the application (Flask server) and API**

*First make sure to Activate the virtual environment (see above)
```
python -m backend.app
```
