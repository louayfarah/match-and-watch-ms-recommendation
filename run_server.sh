if [ ! -d "tmp" ]; then
    mkdir tmp
    chmod -R 777 tmp
fi

python3 -u load/load_embeddings.py
python3 -u load/load_model.py

uvicorn main:app --host 0.0.0.0