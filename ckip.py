# -*-coding:utf-8-*-
import re
import requests
import concurrent.futures


class CkipSegmenter():
    def __init__(self, max_workers=8):
        self.max_workers = max_workers

    def seg(self, text):
        if not isinstance(text, str):
            try:
                text = text.decode('utf-8')
            except:
                raise UnicodeError('Input encoding should be UTF8 or UNICODE')
        try:
            data = {
                'query': text.encode('cp950'),
                'Submit': '送出'.encode('cp950')
            }
        except:
            raise Exception(
                'CKIP Segmentator only accepts characters encoded in CP950; however, it seems that there are some characters which cannot be encoded in CP950.')

        url_tar = 'http://sunlight.iis.sinica.edu.tw/cgi-bin/text.cgi'

        result = requests.post(url_tar, data=data)

        page_num = re.search("URL=\'/uwextract/pool/(\d*?).html\'", result.text).group(1)

        url_fin = 'http://sunlight.iis.sinica.edu.tw/uwextract/show.php?id={page_num}&type=tag'.format(page_num=page_num)

        seg = requests.get(url_fin)
        seg.encoding = 'cp950'
        seg = seg.text

        break_sign = '-' * 130

        seg_pat = re.compile('<pre>(.*?)</pre>', re.DOTALL)
        seg_clean = seg_pat.search(seg).group(1)
        seg_clean = seg_clean.replace(break_sign, '')
        seg_clean = seg_clean.replace('\n', '')
        fs = '\u3000'  # fullwidth space
        seg_fin = seg_clean.replace(fs, ' ')
        output = self.SegResult(seg_fin)
        return output

    def batch_seg(self, corpus):
        results = [None] * len(corpus)
        future_to_crawl = {}
        finished = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for index, text in enumerate(corpus):
                future_to_crawl[executor.submit(self.seg, text)] = index

            for future in concurrent.futures.as_completed(future_to_crawl):
                index = future_to_crawl[future]
                try:
                    result = future.result()
                    results[index] = result
                    finished += 1
                    print('{finished}/{corpus_len} collected.'.format(finished=finished, corpus_len=len(corpus)), end='\r')
                except Exception as exc:
                    future_to_crawl[executor.submit(self.seg, corpus[index])] = index
                    print('{exc}: {text:.20} failed, retrying...'.format(exc=exc, text=corpus[index]))

        return results

    class SegResult():
        def __init__(self, raw):
            self.raw = raw
            seg_fin_pat = re.compile('(.*?)\((\w*?)\)')
            tokens = []
            for tok in raw.split():
                res = seg_fin_pat.search(tok)
                if res:  # need to find out why None appears!
                    tokens.append((res.group(1), res.group(2)))
            output = ''
            for word, pos in tokens:
                output += '%s/%s ' % (word, pos)
            output = output.replace('__n__/FW', '\n')
            output = output.replace('__n__', '\n')
            output = output.replace('__<__', '<')
            output = output.replace('__>__', '>')
            output = output.strip()
            output = output.split(' ')
            res = []
            for i in output:
                tmp = i.partition('\n')
                for x in tmp:
                    if x != '':
                        res.append(x)
            fin = []
            for i in res:
                if i == '\n':
                    word = i
                    pos = 'LINEBREAK'
                else:
                    pat = re.search('(.*)/(\w+)$', i)
                    try:  # need to check
                        word = pat.group(1)
                    except:
                        word = i
                    word = self.num_patch(word)
                    try:
                        pos = pat.group(2)
                    except:
                        pos = 'None'
                fin.append((word, pos))
            self.res = fin
            self.tok, self.pos = zip(*fin)

        def num_patch(self, string):
            num_h = [chr(i) for i in range(48, 58)]
            num_f = [chr(i) for i in range(65296, 65306)]
            num_patch_dict = dict(list(zip(num_f, num_h)))
            output = ''
            for i in string:
                if i in num_patch_dict.keys():
                    output += num_patch_dict[i]
                else:
                    output += i
            return output

        def __str__(self):
            return '<SegResult {raw:.50} ...>'.format(raw=self.raw)

        def __repr__(self):
            return '<SegResult {raw:.50} ...>'.format(raw=self.raw)


if __name__ == '__main__':
    text = '''
斷詞服務採用TCP Socket連線傳輸資料，伺服器IP位址為140.109.19.104，連接埠為1501。'''

    ckip = CkipSegmenter()
    print('ckip.seg(str)')
    result = ckip.seg(text)
    print('result.res: {}\nresult.tok: {}\nresult.pos: {}\n'.format(result.res, result.tok, result.pos))
    print('ckip.batch_seg(list[str])')
    results = ckip.batch_seg([text] * 10)
    print(results)
