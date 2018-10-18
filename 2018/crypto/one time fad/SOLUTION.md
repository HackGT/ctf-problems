# One Time Fad

## Solution
With the provided source code, the competitors should notice that this is a simple one time pad encryption scheme. However, rather than directly decrypting items passed into it, this one time pad will randomly xor every byte with the second-to-last set of two binary value of one of the following bytes: ¯\\(ツ)/¯

The following line defines the choice of the second to last set of two binary mystery characters:

```python
mystery = int(''.join([bin(ord(random.choice(box_of_tricks)))[-3:-1] for x in range(len(keyBinStr) // 2)]), 2)
```


At first, it seems to be an impossible task. However, examining the byte sequence yields some interesting results. Let us convert that entire string to binary:

<center>

| Character |      Binary String       |
|:---------:|:------------------------:|
|    `¯`    |    `______10101[11]1`    |
|    `\`    |    `_______1011[10]0`    |
|    `(`    |    `________101[00]0`    |
|    `ツ`   |    `11000011000[10]0`    |
|    `)`    |    `________101[00]1`    |
|    `/`    |    `________101[11]1`    |
|    `¯`    |    `______10101[11]1`    |

</center>

Using this table, we can clearly see that each bit has an unbalanced distribution. Thus, if we take a large enough sample size of broken decryptions, we can xor the most common bits that occur with the most common bits that occur in this table and extract the flag. In this case, it happens to be the bitstring: `10` repeating.