import argparse
from config import load_config
from feeds import process_streams

def main(args):
    config = load_config(args.config_path)
    process_streams(config=config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="An app to transcribe audio feeds")

    parser.add_argument("--config-path", required=False, default="./config/config.yaml", help="Path to the output file")

    args = parser.parse_args()

    main(args)