#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4 sw=4 sts=4 ff=unix ft=python expandtab

import os
import sys
import json
import re
import traceback
import requests
import random
import codecs
import inspect
import redis


class Subculture(object):
    """ abstract """
    content = None
    speaker = None
    __redis_db = 14  # don't change me if changes will cause collision other app
    conn = None
    enable_flood_check = True

    def __init__(self, text=None, speaker=None):
        self.speaker = speaker

    def redis_connect(self):
        if self.conn is None:
            self.conn = redis.Redis(host='127.0.0.1', db=self.__redis_db)

    def check_flood(self, speaker='', sec=30):
        if self.enable_flood_check is False:
            return True

        self.redis_connect()

        key = 'flood_%s__%s' % (self.__class__.__name__, speaker)
        if self.conn.get(key) is not None:
            return False

        self.conn.set(key, '1')
        self.conn.expire(key, sec)

        return True

    def clear_flood_status(self, speaker='', sec=30):
        self.redis_connect()
        key = 'flood_%s__%s' % (self.__class__.__name__, speaker)
        self.conn.delete(key)

    def fetch(self, url):
        self.content = None
        headers = {
            "User-Agent": r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
        }
        try:
            r = requests.get(url, headers=headers)
            if r.status_code == requests.codes.ok:
                self.content = r.content
            else:
                self.content = '?:' + str(r.status_code)
        except Exception:
            self.content = traceback.format_exc()

    def response(self):
        """ abstract """
        return None


class SubcultureKnowerLevel(Subculture):

    def response(self):
        self.redis_connect()
        level = self.conn.incr("knower-%s" % self.speaker, 1)
        return u"おっ、分かり度 %d ですか" % level


class SubcultureKnowerLevelUp(Subculture):

    def response(self):
        self.redis_connect()
        self.conn.incr("knower-%s" % self.speaker, 1)
        return None


class SubcultureGyazoScraper(Subculture):
    """ gyazo image url extactor """
    pick_re = '<meta content="(http://i.gyazo.com/([0-9a-z\.]+))" name="twitter:image" />'

    def __init__(self, text=None, speaker=None):
        self.pick_re = re.compile(self.pick_re)
        if text is not None:
            self.fetch(text)

    def response(self):
        m = self.pick_re.search(self.content)
        if m and m.group():
            return m.group(1)
        else:
            return None


class SubcultureMETAR(Subculture):
    """ Weather METARs """
    url = 'http://api.openweathermap.org/data/2.5/weather?q=Tokyo,jp'

    def __init__(self, text=None, speaker=None):
        self.fetch(self.url)

    def response(self):
        try:
            w = json.loads(self.content)
            temp_c = float(w["main"]["temp"]) - 273.15
            weather = w["weather"][0]["description"]
            icon_url = 'http://openweathermap.org/img/w/' + w["weather"][0]["icon"] + '.png'
            pressure = int(w["main"]["pressure"])
            humidity = int(w["main"]["humidity"])

            return u'%s (%.1f\u2103; %d\u3371; %d%%)\n%s' % (weather, temp_c, pressure, humidity, icon_url)

        except:
            return traceback.format_exc()


class SubcultureOmochi(Subculture):
    """ omochi """
    def response(self):
        omochi = [
            'http://limg3.ask.fm/assets/318/643/185/thumb/15.png',
            'http://icondecotter.jp/data/11787/1253637750/3da1de4437114e091d35483a03824989.png',
            'https://pbs.twimg.com/media/BcPKzauCQAEN7oR.png',
            'http://www.ttrinity.jp/_img/product/21/21201/1489293/1689893/4764618/product_img_f_4764618.jpg',
            'http://zigg.jp/wp-content/uploads/2014/05/00_Icon.png',
            'http://i.gyazo.com/5f7f28f4794fa6023afa3a0cab0c3ac0.png',
            'http://i.gyazo.com/5f7f28f4794fa6023afa3a0cab0c3ac0.png',
            'http://img-cdn.jg.jugem.jp/f29/2946929/20140106_445358.jpg',
            'http://img-cdn.jg.jugem.jp/f29/2946929/20140106_445355.jpg',
            'https://pbs.twimg.com/media/ByjWDq-CYAAeArB.jpg',
            'https://pbs.twimg.com/media/BsuorQICUAA3nMw.jpg',
            ]

        # dont response within 30 seconds
        if self.check_flood(self.speaker, 30) is False:
            return None

        random.seed()
        return omochi[random.randrange(0, len(omochi))]


class SubcultureStone(Subculture):
    """ stone """
    def response(self):
        stone = [
            # Gyazo
            'http://i.gyazo.com/cc5cf9e9f19c4276af1380a18146eadb.png',
            'http://i.gyazo.com/671fee5ce52c6350ace3728fce53fa84.png',
            'http://i.gyazo.com/ca2b01ff7ceb4f3195e33025b7005554.png',
            'http://i.gyazo.com/e5b966c89fd9fd9711ab2d9acdb7daf1.png',
            'http://i.gyazo.com/254db6809c8bbb32e10c80ff8b731a65.png',
            'http://i.gyazo.com/dfce33d4bba619e315fa1a676d0c84ba.png',
            'http://i.gyazo.com/c0c780844c4b015ecfade90138332f22.png',
            'http://i.gyazo.com/30e9859104a68414b2c9f3b8a023ae00.png',
            'http://i.gyazo.com/716c9e12dafb47f2da1e31fbeeb6a467.png',
            'http://i.gyazo.com/a043f697cad2d34ee4febc071d47b03e.png',
            'http://i.gyazo.com/a12974aabdf48eb50e1f81d513546f15.png',
            'http://i.gyazo.com/41dd1a0d542504b44b6028ad472411ce.png',
            'http://i.gyazo.com/d0414248b36a5cfd3ef5456f1b73f28e.png',
            'http://i.gyazo.com/4c75f3c6393ed809472023e583508465.png',
            'http://i.gyazo.com/2e8cbd1c5b450ab7256579bd55a1487e.png',
            'http://i.gyazo.com/1c5243b9aaa91d651a57764a1cc33ef0.png',
            'http://i.gyazo.com/ed92327451d2e7faf581a2024589451f.png',
            'http://i.gyazo.com/3175440fd6c5329a9f35d5191b5920b2.png',
            'http://i.gyazo.com/4793f98f008e2abb1d28af4a38178c3a.png',
            'http://i.gyazo.com/b57b175072f7f9aaca93f1fc460cd63e.png',
            'http://i.gyazo.com/ba99fc4f1f0dc5c90f28cd2b4683a863.png',
            'http://i.gyazo.com/3c7269601fb9afab5c33e272f3054a28.png',
            'http://i.gyazo.com/e5de9dc949228363acb36ed0e3f6b1cb.png',
            'http://i.gyazo.com/72e4d75d8e21479ab50624ab88c8ce17.png',
            'http://i.gyazo.com/f652a12aa54ffd491de317cb981b48b9.png',
            'http://i.gyazo.com/0969e1c43acea1f70632b2157eba5793.png',
            'http://i.gyazo.com/99a4c3f45ee3758a37cac260c171c5d2.png',
            'http://i.gyazo.com/b83f854434de8b4bae0c9d5bb84365f4.png',
            'http://i.gyazo.com/f018d843af2338150b7522dfed84da08.png',
            'http://i.gyazo.com/1c5243b9aaa91d651a57764a1cc33ef0.png',
            'http://i.gyazo.com/3c7269601fb9afab5c33e272f3054a28.png',
            'http://i.gyazo.com/0969e1c43acea1f70632b2157eba5793.png',
            'http://i.gyazo.com/f018d843af2338150b7522dfed84da08.png',
            'http://i.gyazo.com/99a4c3f45ee3758a37cac260c171c5d2.png',

            # etc
            'http://i.gyazo.com/4fd0d04bd674ae6179d2e5de6340161f.png',
            'http://www.gohongi-beauty.jp/blog/wp-content/uploads/2013/08/stone_4.png',
            'http://shonankit.blog.so-net.ne.jp/blog/_images/blog/_285/shonankit/9223616.jpg',
            'http://shonankit.blog.so-net.ne.jp/blog/_images/blog/_285/shonankit/9223612.jpg',
            'http://nyorokesseki.up.seesaa.net/image/kesseki400_300.jpg',
            'http://shonankit.c.blog.so-net.ne.jp/_images/blog/_285/shonankit/02-3c13d.jpg',
            'http://livedoor.blogimg.jp/fknews/imgs/4/c/4c478d9b.jpg',
            'http://i.gyazo.com/29a38b2b9202862189d8f7a4df1e8886.png',
            'http://i.gyazo.com/183cade0a96dfcac84a113125a46bfa9.png',
            u'西山石\nhttp://i.gyazo.com/ed7b4e6adaa018c4a8212c7590a98ab3.png',
            ]

        if self.check_flood(self.speaker, 30) is False:
            return None

        random.seed()
        return stone[random.randrange(0, len(stone))]


class SubcultureWaterFall(Subculture):
    """ water fall """
    def response(self):
        urls = [
            u'http://i.gyazo.com/78984f360ddf36de883ec0488a4178cb.png',
            u'http://i.gyazo.com/684523b240128b6f0eb21825e52f5c6c.png',
            ]

        if self.check_flood(self.speaker, 10) is False:
            return None

        return '\n'.join(urls)


class SubcultureHai(Subculture):
    """ hai """
    def response(self):
        random.seed()

        res = None
        if random.randrange(0, 100) > 50:
            res = u'はい'
        else:
            res = u'はいじゃないが'

        return res


class SubcultureHitozuma(Subculture):
    """ hitozuma """
    def response(self):
        random.seed()

        res = None
        if random.randrange(0, 100) == 0:
            if random.randrange(0, 100) > 0:
                res = u'はい'
            else:
                res = u'いいえ'

        return res


class AnotherIsMoreKnowerThanMe(Subculture):

    def response(self):
        knower = ['kuzuha', 'ykic', 'esehara']

        K = SubcultureKnowerLevelUp('', self.speaker)
        K.response()

        random.seed()
        return 'No, %s culture.' % knower[random.randrange(0, len(knower))]


class HateSubculture(Subculture):

    def response(self):
        random.seed()
        return u'　\n' * (random.randint(10) * 20)


class NotSubculture(object):
    """ main """
    debug = True
    body = None
    message = None
    texts = None
    dic = {'^(Ｓ|ｓ|S|s)(ｕｂ|ub)\s*((Ｃ|ｃ|C|c)(ｕｌｔｕｒｅ|ulture))?$': 'No',
           u'ベンゾ': u'曖昧',
           u'カエリンコ': u'いいですよ',
           u'^(Ｔａｒｏ|Taro|太郎|Ｙａｒｏ|Yaro|野郎)$': 'Esehara Likes Taro and Yaro.',
           u'(:?\(sun\)|おはようございます|ohayougozaimasu)': u'☀',
           u'^サ(ブ|ヴ)(カルチャー)?(なの)?(では)?(\?|？|。)*$': '?',
           u'^(\?|？)$': '?',
           u'^はい(じゃないが)?$': SubcultureHai,
           u'(kumagai|ykic|kuzuha|esehara|tajima|niryuu|takano(:?32)?|usaco|voqn|tomad|yuiseki|pha|布) culture': AnotherIsMoreKnowerThanMe,
           u'さすが\s?(kuzuha|ykic|usaco|pha|esehara|niryuu|tajima|usaco)\s?(さん)?': u'わかるなー',
           u'さすが\s?(くまがい|熊谷|kumagai|tinbotu|ｋｕｍａｇａｉ|ｔｉｎｂｏｔｕ)\s?(さん)?': u'?',
           u'わかるなー*$': SubcultureKnowerLevel,
           u'(doge2048|JAL\s?123)': u'なるほど',
           u'(鐵|鐡)道(では)?$': u'おっ',
           u'電車': u'鐵道または軌道車',
           u'戦い': u'戰いでしょ',
           u'拝承': u'拝復',
           u'あなた': u'あなたとJAVA, 今すぐダウンロー\nド\nhttps://www.java.com/ja/',
           u'^おもち$': SubcultureOmochi,
           u'^石$': SubcultureStone,
           u'山だ?$': u'やまいくぞ',
           u'がんばるぞい(！|!)?$': 'http://cdn-ak.f.st-hatena.com/images/fotolife/w/watari11/20140930/20140930223157.jpg',
           u'ストールするぞ(ほんとに)?$': u'はい',
           u'(俺は|おれは)?もう(だめ|ダメ)だ$': u'どうすればいいんだ',
           u'どうすればいいんだ': u'おれはもうだめだ',
           u'(は|の|とか)((きも|キモ)いの|(サブ|サヴ))(では)?$': u'?',
           u'^(クソ|糞|くそ)(すぎる|だな)ー?$': u'ごめん',
           # 'http://gyazo.com': SubcultureGyazoScraper,
           u'^(?:(今日?|きょう)?外?(暑|寒|あつ|さむ)い(のかな|？|\?)|METAR|天気)$': SubcultureMETAR,
           u'^消毒$': SubcultureWaterFall,
           u'^流す$': HateSubculture,
           u'(わか|分か|なるほど|はい|おもち|かわいい|便利|タダメシ|機運|老|おっ|ですね|サブ|布|水)': SubcultureKnowerLevelUp,
           '.': SubcultureHitozuma,
           }

    def __init__(self):
        self.httpheaderHasAlreadySent = False

    def httpheader(self, header="Content-Type: text/plain; charset=UTF-8\n"):
        if self.httpheaderHasAlreadySent is False:
            print header
            self.httpheaderHasAlreadySent = True

    def read_http_post(self, method, http_post_body):
        if self.body is None and method == 'POST':
            self.body = http_post_body
            try:
                self.message = json.loads(self.body)
            except Exception:
                if self.debug:
                    self.httpheader()
                    print traceback.format_exc()
                    sys.exit(0)
                else:
                    self.httpheader()
                    print "json decode error:", self.body
                    sys.exit(0)

    def response(self):
        self.httpheader()
        if self.message is None:
            return

        for n in self.message['events']:
            if 'text' in n['message']:
                speaker = n['message']['speaker_id']
                text = n['message']['text']
                for dict_k, dict_res in self.dic.iteritems():
                    pattern = re.compile(dict_k)
                    if pattern.search(text):
                        if inspect.isclass(dict_res):
                            I = dict_res(text, speaker)
                            r = I.response()
                            if r:
                                yield r
                        else:
                            yield dict_res


if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    no = NotSubculture()
    post_body = sys.stdin.read()
    no.read_http_post(os.environ.get('REQUEST_METHOD'), post_body)
    for r in no.response():
        print r
