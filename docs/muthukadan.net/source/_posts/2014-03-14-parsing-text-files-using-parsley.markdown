---
layout: single
title: Parsing text files using Parsley
date:   2014-03-14
categories: python
---

I was looking for a parser library to convert a [wikisource text] into
other formats.  The wikisource text contains Holy Bible translation
into Malayalam language known as "Sathyavedapusthakam".

I found [Parsley] very interesting after watching the [PyCon talk] by
its author.  Parsley doesn't support Python 3 yet.  Then, I used a
[fork] to run my code.  The fork author has already send a [pull
request].  So, I hope Parsley will officially support Python 3 soon.

[fork]: https://github.com/vsajip/parsley
[wikisource text]: http://ml.wikisource.org/wiki/സത്യവേദപുസ്തകം
[Parsley]: http://parsley.readthedocs.org
[PyCon talk]: http://www.youtube.com/watch?v=t5X3ljCOFSY
[pull request]: https://github.com/python-parsley/parsley/pull/18

The format of my input file was something as given below.  The actual
text contains a mix of Malayalam and English characters encoded in
"utf-8" format. However, for simplicity I removed Malayalam from the
below input text:

{% raw %}
```
{{Some Text}}
{{Navi|
Prev=Some Text|
Next=Some Text|
}}
{{Some Text}}

{{verse|1}} Verse One

{{Verse|2}} Verse Two

{{Navi|
Prev=Some Text|
Next=Some Text|
}}
```
{% endraw %}

My parsing code is part of a bigger module with other functionalities.
Here is a stripped-down version of my parsing code:

{% raw %}
```python
import sys
import parsley

parser = parsley.makeGrammar("""
fix = '{{' <((anything|ws):x ?(x not  in '}') -> x)+>:s '}}' -> s
num = '{{' ('V'|'v') 'erse|' <digit+>:s '}}' -> int(s)
text =  <((anything|ws):x ?(x not in '{') -> x)+>:s  -> s
verse = (fix ws){3} (num:n text:t -> (n, t))+:l fix anything* -> l
""", {})

wikitext = open(sys.argv[1]).read()
verses = parser(wikitext).verse()
print(verses)
```
{% endraw %}

I think, the parsing grammar should be possible to improve.  But this
is what I reached after many iterations.  If you have any suggestions
to improve the grammar, please send it to me :)

If you want to run the above code, save the input text given above in
a file and run the program with the input file as an argument.

The output will be a list of tuples.  Each tuple contains an integer
and string values.  Here is the output for the above input text:

{% raw %}
```
[(1, ' Verse One\n\n'), (2, ' Verse Two\n\n')]
```
{% endraw %}

The official [documentation] has enough infomation about the usage.
And the [git repo] has more examples.

[documentation]: http://parsley.readthedocs.org
[git repo]: https://github.com/python-parsley/parsley
