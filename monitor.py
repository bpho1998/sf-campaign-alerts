import json,os,feedparser,requests
RSS_URL="https://netfile.com/connect2/api/public/list/filing/rss/SFO/campaign.xml"
WEBHOOK=os.environ["DISCORD_WEBHOOK"];SEEN_FILE="seen.json"
def load():
    return json.load(open(SEEN_FILE)) if os.path.exists(SEEN_FILE) else []
def save(s):
    json.dump(s,open(SEEN_FILE,"w"),indent=2)
feed=feedparser.parse(RSS_URL)
seen=load()
if not seen:
    save([e.link for e in feed.entries]);print("Initialized seen list.");raise SystemExit
changed=False
for e in reversed(feed.entries):
    if e.link not in seen:
        requests.post(WEBHOOK,json={"content":f"📢 **New SF Campaign Filing**\n**Title:** {e.title}\n**Date:** {getattr(e,'published','Unknown')}\n{e.link}"})
        seen.append(e.link);changed=True
if changed: save(seen)
