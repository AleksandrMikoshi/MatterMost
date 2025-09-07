import os
import time
from dataclasses import dataclass
from typing import Dict, Set

from mattermostdriver import Driver
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    url: str
    scheme: str
    port: int
    token: str
    team_name: str
    channel_allowlist_raw: str
    global_allowlist_raw: str
    thread_allowlist_raw: str
    dm_notify: bool
    dm_text: str
    poll_interval: int


def load_config() -> Config:
    return Config(
        url=os.getenv("MM_URL", "localhost"),
        scheme=os.getenv("MM_SCHEME", "http"),
        port=int(os.getenv("MM_PORT", "8065")),
        token=os.getenv("MM_TOKEN", ""),
        team_name=os.getenv("TEAM_NAME", ""),
        channel_allowlist_raw=os.getenv("CHANNEL_ALLOWLIST", "").strip(),
        global_allowlist_raw=os.getenv("GLOBAL_ALLOWLIST", "").strip(),
        thread_allowlist_raw=os.getenv("THREAD_ALLOWLIST", "").strip(),
        dm_notify=(os.getenv("DM_NOTIFY", "no").lower() in ("yes", "true", "1")),
        dm_text=os.getenv("DM_TEXT", "Posting is restricted in {channel}. Contact admins."),
        poll_interval=int(os.getenv("POLL_INTERVAL", "5")),
    )


class ModeratorBot:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.driver = Driver({
            "url": cfg.url,
            "scheme": cfg.scheme,
            "port": cfg.port,
            "token": cfg.token,
            "verify": False,
            "timeout": 30,
        })
        self.team_id = None
        self.channel_name_to_id: Dict[str, str] = {}
        self.channel_id_to_name: Dict[str, str] = {}
        self.username_to_id: Dict[str, str] = {}
        self.id_to_username: Dict[str, str] = {}
        self.allow_by_channel: Dict[str, Set[str]] = {}
        self.global_allow: Set[str] = set()
        self.thread_allow: Set[str] = set()
        self.me_id = None
        self.last_post_time: Dict[str, str] = {}
        self.start_time = str(int(time.time() * 1000))

    def log(self, *args):
        print("[moderator-bot]", *args, flush=True)

    def start(self):
        self.driver.login()
        self.log("Logged in")

        me = self.driver.users.get_user("me")
        self.me_id = me["id"]

        team = self.driver.teams.get_team_by_name(self.cfg.team_name)
        if not team:
            raise RuntimeError(f"Team '{self.cfg.team_name}' not found")
        self.team_id = team["id"]

        self._load_channels()
        self._build_allowlists()
        self._poll_loop()

    def _load_channels(self):
        chans = self.driver.channels.get_channels_for_user(self.me_id, self.team_id)
        for ch in chans:
            self.channel_name_to_id[ch["name"]] = ch["id"]
            self.channel_id_to_name[ch["id"]] = ch["name"]
        self.log(f"Channels loaded: {len(self.channel_name_to_id)}")

    def _build_allowlists(self):
        if self.cfg.global_allowlist_raw:
            for uname in self._split_users(self.cfg.global_allowlist_raw):
                uid = self._get_user_id_by_username(uname)
                if uid:
                    self.global_allow.add(uid)

        if not self.cfg.channel_allowlist_raw:
            self.log("No CHANNEL_ALLOWLIST set — nothing to moderate.")
        else:
            per = self.cfg.channel_allowlist_raw.split(";")
            for item in per:
                item = item.strip()
                if not item or ":" not in item:
                    continue
                ch_name, users_str = item.split(":", 1)
                ch_name = ch_name.strip()
                ch_id = self.channel_name_to_id.get(ch_name)
                if not ch_id:
                    self.log(f"Channel '{ch_name}' not found or bot not a member — skipping.")
                    continue
                allowed: Set[str] = set(self.global_allow)
                for uname in self._split_users(users_str):
                    uid = self._get_user_id_by_username(uname)
                    if uid:
                        allowed.add(uid)
                self.allow_by_channel[ch_id] = allowed
                self.log(f"Allowlist for #{ch_name}: {len(allowed)} users")

        if self.cfg.thread_allowlist_raw:
            for ch_name in self.cfg.thread_allowlist_raw.split(","):
                ch_name = ch_name.strip()
                ch_id = self.channel_name_to_id.get(ch_name)
                if ch_id:
                    self.thread_allow.add(ch_id)
            self.log(f"Thread-allowlist: {len(self.thread_allow)} channels")

    @staticmethod
    def _split_users(users_str: str):
        return [u.strip().lstrip("@") for u in users_str.split(",") if u.strip()]

    def _get_user_id_by_username(self, username: str):
        if not username:
            return ""
        if username in self.username_to_id:
            return self.username_to_id[username]
        try:
            u = self.driver.users.get_user_by_username(username)
            if u:
                self.username_to_id[username] = u["id"]
                self.id_to_username[u["id"]] = username
                return u["id"]
        except Exception as e:
            self.log(f"Cannot resolve @{username}: {e}")
        return ""

    def _dm(self, user_id: str, text: str):
        try:
            dm = self.driver.channels.create_direct_message_channel([self.me_id, user_id])
            self.driver.posts.create_post({
                "channel_id": dm["id"],
                "message": text
            })
        except Exception as e:
            self.log(f"DM send failed: {e}")

    def _handle_posted(self, post: dict):
        user_id = post.get("user_id")
        channel_id = post.get("channel_id")
        post_id = post.get("id")

        if user_id == self.me_id:
            return
        if channel_id not in self.allow_by_channel:
            return

        allowed = self.allow_by_channel[channel_id]

        if user_id not in allowed:
            if post.get("root_id") and channel_id in self.thread_allow:
                return

        if user_id in allowed:
            return

        ch_name = self.channel_id_to_name.get(channel_id, channel_id)
        try:
            self.driver.posts.delete_post(post_id)
            self.log(f"Deleted post {post_id} in #{ch_name} from user {user_id}")
        except Exception as e:
            self.log(f"Failed to delete post {post_id}: {e}")
            return

        if self.cfg.dm_notify:
            try:
                msg = self.cfg.dm_text.format(channel=f"#{ch_name}")
            except Exception:
                msg = self.cfg.dm_text
            self._dm(user_id, msg)

    def _poll_loop(self):
        self.log(f"Starting polling every {self.cfg.poll_interval} seconds…")
        while True:
            for ch_id in self.allow_by_channel.keys():
                try:
                    posts_data = self.driver.posts.get_posts_for_channel(
                        ch_id,
                        params={"since": self.last_post_time.get(ch_id, self.start_time)}
                    )
                    posts_ordered = sorted(posts_data["posts"].values(), key=lambda x: x["create_at"])
                    for post in posts_ordered:
                        if int(post["create_at"]) > int(self.start_time) and \
                           str(post["create_at"]) > self.last_post_time.get(ch_id, self.start_time):
                            self._handle_posted(post)
                            self.last_post_time[ch_id] = str(post["create_at"])
                except Exception as e:
                    self.log(f"Error polling channel {ch_id}: {e}")
            time.sleep(self.cfg.poll_interval)


if __name__ == "__main__":
    cfg = load_config()
    if not cfg.token or not cfg.team_name:
        raise SystemExit("MM_TOKEN and TEAM_NAME are required")
    bot = ModeratorBot(cfg)
    bot.start()