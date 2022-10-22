# -*- coding:utf-8 -*-

from pyquery import PyQuery
import requests


def get_qr_code(phone):
    url = 'https://cli.im/api/qrcode/code?'
    params = {
        "text": phone,
        "mhid": 'tBTGXVntncwhMHYoL9VUMa8',
    }
    html = requests.request(method="post", url=url, params=params).text
    # print(html)
    pq_html = PyQuery(''.join([html.replace('</body>', '').replace('</html>', ''), '</body></html>', ]))
    return 'https://'+pq_html('.qrcode_plugins_box_body img').attr('src')[2:]
