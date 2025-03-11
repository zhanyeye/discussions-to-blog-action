import os
import json
import requests
from pathlib import Path


def sanitize_filename(title):
    """  
    对标题进行处理，转换为合法的文件名  
    """
    return title.strip().replace(" ", "-").replace("/", "-").replace("\\", "-").lower()


def write_markdown(discussion, output_dir, workspace_root):
    """  
    将 Discussion 数据写入 Markdown 文件  
    """
    created_at = discussion['updated_at']
    year = created_at[:4]
    month = created_at[5:7]
    post_dir = os.path.join(workspace_root, output_dir, year, month)
    os.makedirs(post_dir, exist_ok=True)

    filename = f"{sanitize_filename(discussion['title'])}.md"
    filepath = os.path.join(post_dir, filename)

    # 构造 Markdown 内容（含 Front Matter）  
    front_matter = f"""---  
title: "{discussion['title']}"  
date: "{discussion['updated_at']}"  
draft: false  
discussion_id: "{discussion['node_id']}"  
---  
"""
    content = front_matter + "\n" + discussion["body"]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[INFO] 文件已生成：{filepath}")

    return filepath


def delete_markdown(filepath):
    """  
    删除指定 Markdown 文件  
    """
    if os.path.exists(filepath):
        os.remove(filepath)
        print(f"[INFO] 删除 Markdown 文件：{filepath}")
    else:
        print(f"[WARNING] 文件不存在：{filepath}")


def load_mapping(output_dir, workspace_root):
    """  
    加载映射文件并解析为字典  
    """
    map_path = os.path.join(workspace_root, output_dir, ".discussions_index.json")
    if os.path.exists(map_path):
        with open(map_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_mapping(output_dir, workspace_root, mapping):
    """  
    保存映射文件  
    """
    map_path = os.path.join(workspace_root, output_dir, ".discussions_index.json")
    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)
    print(f"[INFO] 映射文件已更新：{mapping}")


def process_created(discussion, output_dir, workspace_root, mapping):
    """  
    处理 "created" 事件  
    """
    filepath = write_markdown(discussion, output_dir, workspace_root)
    mapping[discussion["node_id"]] = filepath


def process_updated(discussion, output_dir, workspace_root, mapping):
    """
    处理 "edited" 事件
    """
    print(f"[INFO] 更新内容：{json.dumps(discussion)}")
    filepath = mapping.get(discussion["node_id"])
    if filepath and Path(filepath).stem != discussion["title"]:
        delete_markdown(filepath)
    new_filepath = write_markdown(discussion, output_dir, workspace_root)
    mapping[discussion["node_id"]] = new_filepath


def process_deleted(discussion, mapping):
    """  
    处理 "deleted" 事件  
    """
    filepath = mapping.pop(discussion["node_id"], None)
    if filepath:
        delete_markdown(filepath)


def run(output_dir, event_file_path="/github/workflow/event.json", workspace_root="/github/workspace", categories=None):
    """  
    主函数：根据 event.json 文件协调 Discussions 的处理  
    """
    if not os.path.exists(event_file_path):
        raise FileNotFoundError(f"无法找到事件文件 {event_file_path}。")

    # 读取event.json文件内容
    with open(event_file_path, "r", encoding="utf-8") as f:
        event = json.load(f)
    print(f"[INFO] 读取事件文件：{json.dumps(event)}")



    # 加载 mapping 文件  
    mapping = load_mapping(output_dir, workspace_root)

    # 处理 discussion
    action = event["action"].lower()
    discussion = event["discussion"]

    if categories and discussion["category"]["slug"].lower() not in categories:
        print("此 category 不需要转 blog")
        exit(0)


    if action == "created":
        print(f"[INFO] 处理新增事件: {discussion['html_url']}")
        process_created(discussion, output_dir, workspace_root, mapping)
    elif action == "edited":
        print(f"[INFO] 处理编辑事件: {discussion['html_url']}")
        process_updated(discussion, output_dir, workspace_root, mapping)
    elif action == "deleted":
        print(f"[INFO] 处理删除事件: {discussion['html_url']}")
        process_deleted(discussion, mapping)
    else:
        print(f"[WARNING] 未知动作 {action}，跳过 discussion_id: {discussion['html_url']}")

    # 保存最新的 mapping 文件  
    save_mapping(output_dir, workspace_root, mapping)
    print("[INFO] Discussions 同步完成！")
