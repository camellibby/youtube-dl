# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    unescapeHTML,
)


class CJSWIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?cjsw\.com/program/(?P<program_name>[\S]+)/(?P<id>[0-9]+)/?'
    IE_NAME = 'cjsw'
    _TEST = {
        'url': 'http://cjsw.com/program/freshly-squeezed/episode/20170620',
        'md5': 'cee14d40f1e9433632c56e3d14977120',
        'info_dict': {
            'id': '20170620',
            'ext': 'mp3',
            'title': 'Freshly Squeezed',
            'description': 'Sled Island artists featured // Live session with Phi Pho, followed by a live session with Sinzere & The Late Nights! // Stay Fresh Y\'all!!',
        }
    }

    def _real_extract(self, url):
        episode_id = self._match_id(url)

        webpage = self._download_webpage(url, episode_id)

        episode_controls = re.search(r'<div[^>]+class=(["\'])episode-controls\1[^>]*>', webpage)
        if not episode_controls:
            raise ExtractorError('No streamable podcast', video_id=episode_id, expected=True)

        title = unescapeHTML(self._search_regex(
            r'<button[^>]+data-showname=(["\'])(?P<title>.*?)\1[^>]*>', webpage, 'title', group='title'))
        description = unescapeHTML(self._html_search_regex(
            r'<p>(?P<description>.*?)</p>', webpage, 'description', fatal=False))
        formats = [{
            'url': self._html_search_regex(
                r'<button[^>]+data-audio-src=(["\'])(?P<audio_url>.*?)\1[^>]*>', webpage, 'audio_url', group='audio_url'),
            'ext': 'mp3',
        }]
        return {
            'id': episode_id,
            'title': title,
            'description': description,
            'formats': formats,
        }
