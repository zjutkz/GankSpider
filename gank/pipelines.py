# -*- coding: utf-8 -*-
from io import StringIO
import hashlib
import os.path
import shutil
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.utils.python import to_bytes
from scrapy.utils.misc import md5sum


class GankPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['beauty_url'], meta = {'time' : item['time']})

    def file_path(self, request, response=None, info=None, checksum=None):
        if not isinstance(request, Request):
            url = request
        else:
            url = request.url
        media_ext = os.path.splitext(url)[1] 
        if checksum is None:
            checksum = hashlib.sha1(to_bytes(url)).hexdigest()
        each_year = request.meta['time'].split("-")[0]
        each_month = request.meta['time'].split("-")[1]
        each_day = request.meta['time'].split("-")[2]
        path = '%s/%s/%s/%s%s' % (each_year, each_month, each_day.split(" ")[0], checksum, media_ext)
        return path

    def file_downloaded(self, response, request, info):
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        path = self.file_path(request, response=response, info=info, checksum=checksum)
        self.store.persist_file(path, buf, info)
        return checksum
