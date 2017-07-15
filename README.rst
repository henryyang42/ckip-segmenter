Ckip Segmenter
-----------

A Python client for the Chinese Word Segmentation System (see `ckipsvr.iis.sinica.edu.tw <http://ckipsvr.iis.sinica.edu.tw/>`_) provided by Academia Sinica Chinese Knowledge and Information Processing (CKIP) Group. The core was adapted from [amigcamel/PyCCS](https://github.com/amigcamel/PyCCS).

Installation
-----------

https://pypi.python.org/pypi/ckip-segmenter
Simply run the following command:
.. code-block:: sh

    pip install ckip-segmenter

If ``pip`` is not available, you can also `download it manually from PyPI <https://pypi.python.org/pypi/ckip-segmenter>`_.

*Note: Currently only Python 3+ is supported.*

Usage
-----------

Summon a ``CkipSegmenter``
--------------------------

.. code:: ipython3

    from ckip import CkipSegmenter
    segmenter = CkipSegmenter()

    text = '詞是最小有意義且可以自由使用的語言單位。任何語言處理的系統都必須先能分辨文本中的詞才能進行進一步的處理'
    corpus = [
        '詞是最小有意義且可以自由使用的語言單位',
        '任何語言處理的系統都必須先能分辨文本中的詞才能進行進一步的處理',
        '例如機器翻譯、語言分析、語言了解、資訊抽取',
        '因此中文自動分詞的工作成了語言處理不可或缺的技術',
        '基本上自動分詞多利用詞典中收錄的詞和文本做比對',
        '找出可能包含的詞，由於存在歧義的切分結果',
        '因此多數的中文分詞程式多討論如何解決分詞歧義的問題',
        '而較少討論如何處理詞典中未收錄的詞出現的問題（新詞如何辨認）',
    ]

The result object contains ``res``, ``tok`` and ``pos``
-------------------------------------------------------

.. code:: ipython3

    result = segmenter.seg(text)
    # result.res is a list of tuples contain a token and its pos-tag.
    print('result.res: {}\n'.format(result.res))

    # result.tok and result.pos contains only tokens and pos-tags respectively.
    print('result.tok: {}\n'.format(result.tok))
    print('result.pos: {}\n'.format(result.pos))



.. parsed-literal::

    result.res: [('詞', 'Na'), ('是', 'SHI'), ('最', 'Dfa'), ('小', 'VH'), ('有', 'V_2'), ('意義', 'Na'), ('且', 'Cbb'), ('可以', 'D'), ('自由', 'VH'), ('使用', 'VC'), ('的', 'DE'), ('語言', 'Na'), ('單位', 'Na'), ('。', 'PERIODCATEGORY'), ('任何', 'Neqa'), ('語言', 'Na'), ('處理', 'VC'), ('的', 'DE'), ('系統', 'Na'), ('都', 'D'), ('必須', 'D'), ('先能', 'Nb'), ('分辨', 'VE'), ('文本', 'Nb'), ('中', 'Ng'), ('的', 'DE'), ('詞', 'Na'), ('才能', 'Na'), ('進行', 'VC'), ('進一步', 'D'), ('的', 'DE'), ('處理', 'VC')]

    result.tok: ['詞', '是', '最', '小', '有', '意義', '且', '可以', '自由', '使用', '的', '語言', '單位', '。', '任何', '語言', '處理', '的', '系統', '都', '必須', '先能', '分辨', '文本', '中', '的', '詞', '才能', '進行', '進一步', '的', '處理']

    result.pos: ['Na', 'SHI', 'Dfa', 'VH', 'V_2', 'Na', 'Cbb', 'D', 'VH', 'VC', 'DE', 'Na', 'Na', 'PERIODCATEGORY', 'Neqa', 'Na', 'VC', 'DE', 'Na', 'D', 'D', 'Nb', 'VE', 'Nb', 'Ng', 'DE', 'Na', 'Na', 'VC', 'D', 'DE', 'VC']



Using ``batch_seg`` for a list of text would be slightly faster
---------------------------------------------------------------

.. code:: ipython3

    segmenter.batch_seg(corpus)


.. parsed-literal::

    8/8 collected.



.. parsed-literal::

    [<SegResult  詞(Na) 是(SHI) 最(Dfa) 小(VH) 有(V_2) 意義(Na) 且(Cbb) 可以 ...>,
     <SegResult  任何(Neqa) 語言(Na) 處理(VC) 的(DE) 系統(Na) 都(D) 必須(D) 先能 ...>,
     <SegResult  例如(P) 機器(Na) 翻譯(VC) 、(PAUSECATEGORY) 語言(Na) 分析(VC ...>,
     <SegResult  因此(Cbb) 中文(Na) 自動(VH) 分詞(Na) 的(DE) 工作(Na) 成(VG) 了 ...>,
     <SegResult  基本(Na) 上(Ncd) 自動(VH) 分詞(Na) 多(D) 利用(VC) 詞典(Na) 中( ...>,
     <SegResult  找出(VC) 可能(D) 包含(VJ) 的(DE) 詞(Na) ，(COMMACATEGORY)  ...>,
     <SegResult  因此(Cbb) 多數(Neqa) 的(DE) 中文(Na) 分詞(Na) 程式(Na) 多(D)  ...>,
     <SegResult  而(Cbb) 較少(D) 討論(VE) 如何(D) 處理(VC) 詞典(Na) 中(Ng) 未(D ...>]




