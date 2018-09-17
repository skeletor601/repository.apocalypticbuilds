import re
 
from livestreamer.plugin import Plugin
from livestreamer.plugin.api import http, validate
from livestreamer.plugin.api.utils import parse_json
from livestreamer.stream import HLSStream
 
_url_re = re.compile(r"https://www.arconaitv.us/([^/]+)/")
 
SOURCES_RE = re.compile(r" data-item='([^']+)' ")
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
 
class ArconaiTv(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)
 
    def _get_streams(self):
        page = http.get(self.url)
        match = SOURCES_RE.search(page.text)
        if match is None:
            return
 
        sources = parse_json(match.group(1))
        if "sources" not in sources or not isinstance(sources["sources"], list):
            return
 
        for source in sources["sources"]:
            if "src" not in source or not source["src"].endswith(".m3u8"):
                continue
 
            yield "live", HLSStream(self.session, source["src"], headers={"User-Agent": USER_AGENT})
 
__plugin__ = ArconaiTv