# Solution

Try opening the file in Word.
I get this error:

> We're sorry.
> We can't open look_closer.docx because we found a problem with its contents.
>
> Details:
>
> The file is corrupt and cannot be opened.

Clicking "OK" gives the option to recover;
clicking "Yes" opens the file with the contents "Look closer!"

Save the new file next to the old one and compare them:

```bash
todo...
```

Here's the first hunk:

```diff
--- /dev/fd/11  2018-10-13 20:07:49.000000000 -0400
+++ /dev/fd/13  2018-10-13 20:07:49.000000000 -0400
@@ -105,13 +105,13 @@
 00000680  0a 1a f0 bc d1 ea 7a a3  bf a7 c5 89 85 2c 09 a1  |......z......,..|
 00000690  09 89 2f fb 7c 66 5c 12  5a fe e7 8a e6 19 3f 36  |../.|f\.Z.....?6|
 000006a0  ef 21 59 b4 5f e1 6f 1b  9c 5d 41 f3 01 00 00 ff  |.!Y._.o..]A.....|
-000006b0  ff 03 00 78 9c cb 48 4c  ce 4e 2f a9 ae 8a f4 08  |...x..HL.N/.....|
-000006c0  76 89 ca 4e ca 09 f7 0b  c8 2b 31 35 ae 05 00 73  |v..N.....+15...s|
-000006d0  a9 08 ef 50 4b 03 04 14  00 06 00 08 00 00 00 21  |...PK..........!|
-000006e0  00 d6 64 b3 51 f4 00 00  00 31 03 00 00 1c 00 08  |..d.Q....1......|
-000006f0  01 77 6f 72 64 2f 5f 72  65 6c 73 2f 64 6f 63 75  |.word/_rels/docu|
-00000700  6d 65 6e 74 2e 78 6d 6c  2e 72 65 6c 73 20 a2 04  |ment.xml.rels ..|
-00000710  01 28 a0 00 01 00 00 00  00 00 00 00 00 00 00 00  |.(..............|
+000006b0  ff 03 00 50 4b 03 04 14  00 06 00 08 00 00 00 21  |...PK..........!|
+000006c0  00 d6 64 b3 51 f4 00 00  00 31 03 00 00 1c 00 08  |..d.Q....1......|
+000006d0  01 77 6f 72 64 2f 5f 72  65 6c 73 2f 64 6f 63 75  |.word/_rels/docu|
+000006e0  6d 65 6e 74 2e 78 6d 6c  2e 72 65 6c 73 20 a2 04  |ment.xml.rels ..|
+000006f0  01 28 a0 00 01 00 00 00  00 00 00 00 00 00 00 00  |.(..............|
+00000700  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
+00000710  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
 00000720  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
 00000730  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
 00000740  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
```

It looks like recovering the file removed some data, specifically

```
000006b0           78 9c cb 48 4c  ce 4e 2f a9 ae 8a f4 08     |x..HL.N/.....|
000006c0  76 89 ca 4e ca 09 f7 0b  c8 2b 31 35 ae 05 00 73  |v..N.....+15...s|
000006d0  a9 08 ef                                          |...|

Let's take a look at that:

```pycon
```
>>> data = bytes.fromhex("""
...          78 9c cb 48 4c  ce 4e 2f a9 ae 8a f4 08
... 76 89 ca 4e ca 09 f7 0b  c8 2b 31 35 ae 05 00 73
... a9 08 ef
... """)
>>> from subprocess import run
>>> run(['file', '-'], input=data, capture_output=True)
CompletedProcess(
    args=['file', '-'],
    returncode=0,
    stdout=b'/dev/stdin: zlib compressed data\n',
    stderr=b'')
>>> from zlib import decompress
>>> decompress(data)
b'hackgt{zYHSDZkblWNPnt53}'
```

Tada!
