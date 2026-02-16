import argparse
import json
import tomllib
from pathlib import Path

from mlflow_service import create_app

def save_openapi(output_path: str = "openapi.json"):
    with open("../pyproject.toml", "rb") as f:
        project_toml_data = tomllib.load(f)
    version = project_toml_data["project"]["version"]

    openapi_schema = create_app().openapi()
    openapi_schema["info"]["version"] = version

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(openapi_schema, f, indent=2, ensure_ascii=False)

    print(f"OpenAPI generated: {output_file.absolute()}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        "-o",
        default="openapi.json",
        help="Output file path (default: openapi.json)"
    )

    args = parser.parse_args()
    save_openapi(output_path=args.output)