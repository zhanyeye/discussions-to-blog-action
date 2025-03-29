import os
import json
import logging
from pathlib import Path
from typing import Dict, Optional, Set

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# Define the version of .discussions_index.json
INDEX_FILE_VERSION = "1.0"


def sanitize_filename(title: str) -> str:
    """
    Sanitize the title to convert it into a valid filename.
    """
    return title.strip().replace(" ", "-").replace("/", "-").replace("\\", "-").lower()


def generate_front_matter(discussion: Dict) -> str:
    """
    Generate front matter for a Markdown file based on discussion data.
    """
    return (
        "---\n"
        f"title: \"{discussion['title']}\"\n"
        f"date: \"{discussion['updated_at']}\"\n"
        "draft: false\n"
        f"discussion_id: \"{discussion['node_id']}\"\n"
        "---\n"
    )


def write_markdown(discussion: Dict, output_dir: Path, workspace_root: Path) -> Path:
    """
    Write discussion data to a Markdown file.
    """
    created_at = discussion['updated_at']
    year, month = created_at[:4], created_at[5:7]
    post_dir = workspace_root / output_dir / year / month
    post_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{sanitize_filename(discussion['title'])}.md"
    filepath = post_dir / filename

    # Construct Markdown content (including Front Matter)
    front_matter = generate_front_matter(discussion)
    content = front_matter + "\n" + discussion["body"]

    filepath.write_text(content, encoding='utf-8')
    logging.info(f"File generated: {filepath}")

    return filepath


def delete_markdown(filepath: Path) -> None:
    """
    Delete the specified Markdown file.
    """
    if filepath.exists():
        filepath.unlink()
        logging.info(f"Deleted Markdown file: {filepath}")
    else:
        logging.warning(f"File does not exist: {filepath}")


def load_discussions_index(output_dir: Path, workspace_root: Path) -> Dict[str, Path]:
    """
    Load the discussions index file (.discussions_index.json) and parse it into a dictionary.
    """
    map_path = workspace_root / output_dir / ".discussions_index.json"

    # Default empty structure
    default_index = {"version": INDEX_FILE_VERSION, "discussions": {}}

    if map_path.exists():
        with map_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        version = data.get("version", "0.0")
        if version != INDEX_FILE_VERSION:
            logging.warning(f"Index file version mismatch: expected {INDEX_FILE_VERSION}, got {version}. Attempting to load anyway.")

        # Parse discussions content; fallback to empty if missing
        discussions = data.get("discussions", {})
        return {k: Path(v) for k, v in discussions.items()}

    return {}  # Return empty discussions if file doesn't exist


def save_discussions_index(output_dir: Path, workspace_root: Path, mapping: Dict[str, Path]) -> None:
    """
    Save the discussions index file (.discussions_index.json) with version information.
    """
    map_path = workspace_root / output_dir / ".discussions_index.json"
    data = {
        "version": INDEX_FILE_VERSION,
        "discussions": {k: str(v) for k, v in mapping.items()}
    }
    with map_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    logging.info(f"Index file updated: {map_path}")


def update_or_create_markdown(discussion: Dict, output_dir: Path, workspace_root: Path,
                              mapping: Dict[str, Path]) -> None:
    """
    Create or update a Markdown file based on discussion data.
    """
    filepath = mapping.get(discussion["node_id"])
    if filepath and filepath.stem != sanitize_filename(discussion["title"]):
        delete_markdown(filepath)

    new_filepath = write_markdown(discussion, output_dir, workspace_root)
    mapping[discussion["node_id"]] = new_filepath


def validate_event_data(event: Dict) -> Dict:
    """
    Validate event.json structure and required fields.
    """
    if "action" not in event or "discussion" not in event:
        raise ValueError("[ERROR] Invalid event.json format, missing 'action' or 'discussion'")

    discussion = event["discussion"]
    required_fields = ["node_id", "title", "updated_at", "html_url", "category"]
    for field in required_fields:
        if field not in discussion:
            raise ValueError(f"[ERROR] Missing required field '{field}' in discussion data")

    return discussion


def process_created(discussion: Dict, output_dir: Path, workspace_root: Path, mapping: Dict[str, Path]) -> None:
    """
    Process "created" event.
    """
    update_or_create_markdown(discussion, output_dir, workspace_root, mapping)


def process_updated(discussion: Dict, output_dir: Path, workspace_root: Path, mapping: Dict[str, Path]) -> None:
    """
    Process "edited" event.
    """
    update_or_create_markdown(discussion, output_dir, workspace_root, mapping)


def process_deleted(discussion: Dict, mapping: Dict[str, Path]) -> None:
    """
    Process "deleted" event.
    """
    filepath = mapping.pop(discussion["node_id"], None)
    if filepath:
        delete_markdown(filepath)


def run(
        output_dir: str,
        event_file_path: str = "/github/workflow/event.json",
        workspace_root: Optional[str] = None,
        categories: Optional[Set[str]] = None,
) -> None:
    """
    Main function: Coordinate the processing of Discussions based on event.json file.
    """
    workspace_root_path = Path(workspace_root or os.getenv("GITHUB_WORKSPACE", os.getcwd()))
    logging.info(f"Using workspace: {workspace_root_path}")

    event_file_path = Path(event_file_path)
    if not event_file_path.exists():
        event_file_path = Path(os.getenv("GITHUB_EVENT_PATH", ""))
        if not event_file_path.exists():
            logging.error("Event.json file does not exist.")
            exit(1)

    # Read event.json file content
    with event_file_path.open("r", encoding="utf-8") as f:
        event = json.load(f)

    discussion = validate_event_data(event)

    # Load mapping file
    output_dir_path = Path(output_dir)
    mapping = load_discussions_index(output_dir_path, workspace_root_path)

    # Filter categories if necessary
    if categories and discussion["category"]["slug"].lower() not in categories:
        logging.info(f"Category '{discussion['category']['slug']}' does not need to be processed.")
        exit(0)

    action = event["action"].lower()
    if action == "created":
        logging.info(f"Processing creation event: {discussion['html_url']}")
        process_created(discussion, output_dir_path, workspace_root_path, mapping)
    elif action == "edited":
        logging.info(f"Processing edit event: {discussion['html_url']}")
        process_updated(discussion, output_dir_path, workspace_root_path, mapping)
    elif action == "deleted":
        logging.info(f"Processing delete event: {discussion['html_url']}")
        process_deleted(discussion, mapping)
    else:
        logging.warning(f"Unknown action '{action}', skipping discussion_id: {discussion['html_url']}")

    # Save the latest mapping file
    save_discussions_index(output_dir_path, workspace_root_path, mapping)
    logging.info("Discussions synchronization complete!")
