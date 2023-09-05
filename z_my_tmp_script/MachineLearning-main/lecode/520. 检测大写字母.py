# -*- coding: utf-8 -*-
class Solution:
    def detectCapitalUse(self, word: str) -> bool:
        result = []
        result2 = []
        small_numbers = range(97, 123)
        big_numbers = range(65, 91)
        if word.istitle():
            return True

        for s in word:
            if ord(s) in small_numbers:
                result2.append(True)
            else:
                result2.append(False)
            if ord(s) in big_numbers:
                result.append(True)
            else:
                result.append(False)

        if all(result2):
            return True
        else:
            return all(result)


a = "Leetcode"
print(Solution().detectCapitalUse(word=a))
