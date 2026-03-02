import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "unified_posts.json"

def get_dt(post):
    date_str = post.get("date")
    if not date_str:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        if "T" in date_str:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        else:
            # VK format "YYYY-MM-DD HH:MM:SS"
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
    except:
        return datetime.min.replace(tzinfo=timezone.utc)

def get_title(post):
    text = post.get("text", "")
    lines = text.splitlines()
    title = post.get("title")
    if not title and lines:
        title = lines[0][:60]
    if not title:
        source = post.get("source", "unknown")
        title = f"Post from {source.upper()}"
    return title

def is_stub(post):
    text = (post.get("text") or "").strip()
    links = post.get("links") or []
    title = get_title(post)
    
    if not text:
        return True
    if title.startswith("Post from "):
        return True
    if len(text) < 100 and not links:
        return True
    return False

def merge_posts(target, source):
    """Merge source post into target post."""
    # Merge media
    if "media" not in target:
        target["media"] = []
    
    new_media = source.get("media", [])
    source_id = source.get("id")
    for item in new_media:
        if "post_id" not in item:
            item["post_id"] = source_id
    
    target["media"].extend(new_media)
    
    # Merge text
    source_text = (source.get("text") or "").strip()
    target_text = (target.get("text") or "").strip()
    
    if source_text and source_text != target_text:
        # Don't append if it's just a "Post from..." title
        if not get_title(source).startswith("Post from "):
            if target_text:
                target["text"] = target_text + "\n\n" + source_text
            else:
                target["text"] = source_text
    
    # Merge links
    if "links" not in target:
        target["links"] = []
    for link in source.get("links", []):
        if link not in target["links"]:
            target["links"].append(link)

def main():
    if not DATA_PATH.exists():
        print(f"Error: {DATA_PATH} not found.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        posts = json.load(f)

    print(f"Loaded {len(posts)} posts.")

    # 1. Deduplicate
    # Group by (id, date, text_hash)
    seen = {}
    deduped = []
    for p in posts:
        key = (p.get("id"), p.get("date"), (p.get("text") or "").strip()[:100])
        if key not in seen:
            seen[key] = p
            deduped.append(p)
        else:
            # If current has media and old doesn't, or vice-versa, merge media?
            # For now just keep first.
            pass
    
    print(f"After deduplication: {len(deduped)} posts.")
    deduped.sort(key=get_dt)

    # 2. Group into clusters within 1 hour
    clusters = []
    if not deduped:
        return

    current_cluster = [deduped[0]]
    for i in range(1, len(deduped)):
        dt_current = get_dt(deduped[i])
        dt_prev = get_dt(deduped[i-1])
        
        if (dt_current - dt_prev).total_seconds() <= 3600:
            current_cluster.append(deduped[i])
        else:
            clusters.append(current_cluster)
            current_cluster = [deduped[i]]
    clusters.append(current_cluster)

    # 3. Process each cluster
    final_posts = []
    merged_total = 0

    for cluster in clusters:
        if len(cluster) == 1:
            final_posts.append(cluster[0])
            continue
        
        # cluster has multiple posts within 1 hour of each other
        anchors = [p for p in cluster if not is_stub(p)]
        
        if not anchors:
            # All are stubs, merge all into the first one
            target = cluster[0]
            for i in range(1, len(cluster)):
                merge_posts(target, cluster[i])
                merged_total += 1
            final_posts.append(target)
        else:
            # Merging stubs into closest anchor
            for p in cluster:
                if p in anchors:
                    continue
                
                # It's a stub, find closest anchor
                dt_p = get_dt(p)
                closest_anchor = min(anchors, key=lambda a: abs((get_dt(a) - dt_p).total_seconds()))
                merge_posts(closest_anchor, p)
                merged_total += 1
            
            final_posts.extend(anchors)

    # Sort final results
    final_posts.sort(key=get_dt)

    print(f"Done! Merged {merged_total} posts.")
    print(f"Final count: {len(final_posts)} posts.")
    
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(final_posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
