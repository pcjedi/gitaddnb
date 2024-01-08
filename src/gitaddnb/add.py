"""The main package file"""
import json
import subprocess
import sys


def addnb(file_path: str) -> None:
    """add a file to the git stage"""
    with open(file_path, encoding="utf-8") as f:
        original_content = f.read()
    j = json.loads(original_content)
    gitaddnb_processed = [
        cell["metadata"].get("gitaddnb", False)
        for cell in j["cells"]
        if cell["cell_type"] == "code" and cell.get("source", []) != []
    ]
    if not all(gitaddnb_processed):
        execution_counts = [
            cell["execution_count"] for cell in j["cells"] if cell["cell_type"] == "code" and cell.get("source", []) != []
        ]
        propper_order = list(range(1, 1 + len(execution_counts)))
        assert (
            execution_counts == propper_order or j["gitaddnb"]
        ), f"Not executed consecutively: {execution_counts}. Restart and Run All on {file_path}"
    with open(file_path, encoding="utf-8") as f:
        j2 = json.load(f)
    for cell in j2["cells"]:
        cell["outputs"] = []
        cell["execution_count"] = None
        cell["metadata"]["gitaddnb"] = True

    with open(file_path, mode="w", encoding="utf-8") as f:
        json.dump(obj=j2, fp=f, sort_keys=True)

    subprocess.run(["git", "add", file_path], check=False)

    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write(original_content)


def gitaddnb(args: list[str] = sys.argv[1:]) -> int:
    """run the cli"""
    file_paths = [arg for arg in args if not arg.startswith("-") and arg.endswith(".ipynb")]
    for file_path in file_paths:
        # check_execution_order(file_path=file_path)
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        addnb(file_path=file_path)
    return 0
