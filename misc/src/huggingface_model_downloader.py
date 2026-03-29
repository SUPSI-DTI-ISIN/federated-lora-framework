from huggingface_hub import snapshot_download
import os

if __name__ == "__main__":

    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    MODEL_PATH = os.path.join( os.path.normpath( os.getenv("MODEL_PATH") ), "original" )
    HF_MODEL_ID = os.getenv("HF_MODEL_ID")
    snapshot_download(repo_id=HF_MODEL_ID, cache_dir=MODEL_PATH, token=HUGGINGFACE_TOKEN)
