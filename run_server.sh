if [ ! -d "tmp" ]; then
    mkdir tmp
    chmod -R 777 tmp
fi

python3 -m load/load_data.py
python3 -m load/load_embeddings.py

uvicorn main:app --host 0.0.0.0