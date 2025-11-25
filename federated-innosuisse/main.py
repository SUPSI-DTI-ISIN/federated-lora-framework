import argparse

from app.orchestrator_service import core

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument("-f", "--folder", help="Pdf Folder path", required=True, default="./pdf-innosuisse", type=str)

    args = arg_parser.parse_args()

    core(args.folder)