from __future__ import unicode_literals

from .bases import _StandardStemmer


class SpanishStemmer(_StandardStemmer):

    """
    The Spanish Snowball stemmer.

    :cvar __vowels: The Spanish vowels.
    :type __vowels: unicode
    :cvar __step0_suffixes: Suffixes to be deleted in step 0 of the algorithm.
    :type __step0_suffixes: tuple
    :cvar __step1_suffixes: Suffixes to be deleted in step 1 of the algorithm.
    :type __step1_suffixes: tuple
    :cvar __step2a_suffixes: Suffixes to be deleted in step 2a of the algorithm.
    :type __step2a_suffixes: tuple
    :cvar __step2b_suffixes: Suffixes to be deleted in step 2b of the algorithm.
    :type __step2b_suffixes: tuple
    :cvar __step3_suffixes: Suffixes to be deleted in step 3 of the algorithm.
    :type __step3_suffixes: tuple
    :note: A detailed description of the Spanish
           stemming algorithm can be found under
           http://snowball.tartarus.org/algorithms/spanish/stemmer.html

    """

    __vowels = "aeiou\xE1\xE9\xED\xF3\xFA\xFC"
    __step0_suffixes = ("selas", "selos", "sela", "selo", "las",
                        "les", "los", "nos", "me", "se", "la", "le",
                        "lo")
    __step1_suffixes = ('amientos', 'imientos', 'amiento', 'imiento',
                        'aciones', 'uciones', 'adoras', 'adores',
                        'ancias', 'log\xEDas', 'encias', 'amente',
                        'idades', 'anzas', 'ismos', 'ables', 'ibles',
                        'istas', 'adora', 'aci\xF3n', 'antes',
                        'ancia', 'log\xEDa', 'uci\xf3n', 'encia',
                        'mente', 'anza', 'icos', 'icas', 'ismo',
                        'able', 'ible', 'ista', 'osos', 'osas',
                        'ador', 'ante', 'idad', 'ivas', 'ivos',
                        'ico',
                        'ica', 'oso', 'osa', 'iva', 'ivo')
    __step2a_suffixes = ('yeron', 'yendo', 'yamos', 'yais', 'yan',
                         'yen', 'yas', 'yes', 'ya', 'ye', 'yo',
                         'y\xF3')
    __step2b_suffixes = ('ar\xEDamos', 'er\xEDamos', 'ir\xEDamos',
                         'i\xE9ramos', 'i\xE9semos', 'ar\xEDais',
                         'aremos', 'er\xEDais', 'eremos',
                         'ir\xEDais', 'iremos', 'ierais', 'ieseis',
                         'asteis', 'isteis', '\xE1bamos',
                         '\xE1ramos', '\xE1semos', 'ar\xEDan',
                         'ar\xEDas', 'ar\xE9is', 'er\xEDan',
                         'er\xEDas', 'er\xE9is', 'ir\xEDan',
                         'ir\xEDas', 'ir\xE9is',
                         'ieran', 'iesen', 'ieron', 'iendo', 'ieras',
                         'ieses', 'abais', 'arais', 'aseis',
                         '\xE9amos', 'ar\xE1n', 'ar\xE1s',
                         'ar\xEDa', 'er\xE1n', 'er\xE1s',
                         'er\xEDa', 'ir\xE1n', 'ir\xE1s',
                         'ir\xEDa', 'iera', 'iese', 'aste', 'iste',
                         'aban', 'aran', 'asen', 'aron', 'ando',
                         'abas', 'adas', 'idas', 'aras', 'ases',
                         '\xEDais', 'ados', 'idos', 'amos', 'imos',
                         'emos', 'ar\xE1', 'ar\xE9', 'er\xE1',
                         'er\xE9', 'ir\xE1', 'ir\xE9', 'aba',
                         'ada', 'ida', 'ara', 'ase', '\xEDan',
                         'ado', 'ido', '\xEDas', '\xE1is',
                         '\xE9is', '\xEDa', 'ad', 'ed', 'id',
                         'an', 'i\xF3', 'ar', 'er', 'ir', 'as',
                         '\xEDs', 'en', 'es')
    __step3_suffixes = ("os", "a", "e", "o", "\xE1",
                        "\xE9", "\xED", "\xF3")

    def stem(self, word):
        """
        Stem a Spanish word and return the stemmed form.

        :param word: The word that is stemmed.
        :type word: str or unicode
        :return: The stemmed form.
        :rtype: unicode

        """
        word = word.lower()

        step1_success = False

        r1, r2 = self._r1r2_standard(word, self.__vowels)
        rv = self._rv_standard(word, self.__vowels)

        # STEP 0: Attached pronoun
        for suffix in self.__step0_suffixes:
            if word.endswith(suffix):
                if rv.endswith(suffix):
                    if rv[:-len(suffix)].endswith(("i\xE9ndo",
                                                   "\xE1ndo",
                                                   "\xE1r", "\xE9r",
                                                   "\xEDr")):
                        word = (word[:-len(suffix)].replace("\xE1", "a")
                                                   .replace("\xE9", "e")
                                                   .replace("\xED", "i"))
                        r1 = (r1[:-len(suffix)].replace("\xE1", "a")
                                               .replace("\xE9", "e")
                                               .replace("\xED", "i"))
                        r2 = (r2[:-len(suffix)].replace("\xE1", "a")
                                               .replace("\xE9", "e")
                                               .replace("\xED", "i"))
                        rv = (rv[:-len(suffix)].replace("\xE1", "a")
                                               .replace("\xE9", "e")
                                               .replace("\xED", "i"))

                    elif rv[:-len(suffix)].endswith(("ando", "iendo",
                                                     "ar", "er", "ir")):
                        word = word[:-len(suffix)]
                        r1 = r1[:-len(suffix)]
                        r2 = r2[:-len(suffix)]
                        rv = rv[:-len(suffix)]

                    elif (rv[:-len(suffix)].endswith("yendo") and
                          word[:-len(suffix)].endswith("uyendo")):
                        word = word[:-len(suffix)]
                        r1 = r1[:-len(suffix)]
                        r2 = r2[:-len(suffix)]
                        rv = rv[:-len(suffix)]
                break

        # STEP 1: Standard suffix removal
        for suffix in self.__step1_suffixes:
            if word.endswith(suffix):
                if suffix == "amente" and r1.endswith(suffix):
                    step1_success = True
                    word = word[:-6]
                    r2 = r2[:-6]
                    rv = rv[:-6]

                    if r2.endswith("iv"):
                        word = word[:-2]
                        r2 = r2[:-2]
                        rv = rv[:-2]

                        if r2.endswith("at"):
                            word = word[:-2]
                            rv = rv[:-2]

                    elif r2.endswith(("os", "ic", "ad")):
                        word = word[:-2]
                        rv = rv[:-2]

                elif r2.endswith(suffix):
                    step1_success = True
                    if suffix in ("adora", "ador", "aci\xF3n", "adoras",
                                  "adores", "aciones", "ante", "antes",
                                  "ancia", "ancias"):
                        word = word[:-len(suffix)]
                        r2 = r2[:-len(suffix)]
                        rv = rv[:-len(suffix)]

                        if r2.endswith("ic"):
                            word = word[:-2]
                            rv = rv[:-2]

                    elif suffix in ("log\xEDa", "log\xEDas"):
                        word = word.replace(suffix, "log")
                        rv = rv.replace(suffix, "log")

                    elif suffix in ("uci\xF3n", "uciones"):
                        word = word.replace(suffix, "u")
                        rv = rv.replace(suffix, "u")

                    elif suffix in ("encia", "encias"):
                        word = word.replace(suffix, "ente")
                        rv = rv.replace(suffix, "ente")

                    elif suffix == "mente":
                        word = word[:-5]
                        r2 = r2[:-5]
                        rv = rv[:-5]

                        if r2.endswith(("ante", "able", "ible")):
                            word = word[:-4]
                            rv = rv[:-4]

                    elif suffix in ("idad", "idades"):
                        word = word[:-len(suffix)]
                        r2 = r2[:-len(suffix)]
                        rv = rv[:-len(suffix)]

                        for pre_suff in ("abil", "ic", "iv"):
                            if r2.endswith(pre_suff):
                                word = word[:-len(pre_suff)]
                                rv = rv[:-len(pre_suff)]

                    elif suffix in ("ivo", "iva", "ivos", "ivas"):
                        word = word[:-len(suffix)]
                        r2 = r2[:-len(suffix)]
                        rv = rv[:-len(suffix)]
                        if r2.endswith("at"):
                            word = word[:-2]
                            rv = rv[:-2]
                    else:
                        word = word[:-len(suffix)]
                        rv = rv[:-len(suffix)]
                break

        # STEP 2a: Verb suffixes beginning 'y'
        if not step1_success:
            for suffix in self.__step2a_suffixes:
                if (rv.endswith(suffix) and
                    word[-len(suffix) - 1:-len(suffix)] == "u"):
                    word = word[:-len(suffix)]
                    rv = rv[:-len(suffix)]
                    break

        # STEP 2b: Other verb suffixes
            for suffix in self.__step2b_suffixes:
                if rv.endswith(suffix):
                    if suffix in ("en", "es", "\xE9is", "emos"):
                        word = word[:-len(suffix)]
                        rv = rv[:-len(suffix)]

                        if word.endswith("gu"):
                            word = word[:-1]

                        if rv.endswith("gu"):
                            rv = rv[:-1]
                    else:
                        word = word[:-len(suffix)]
                        rv = rv[:-len(suffix)]
                    break

        # STEP 3: Residual suffix
        for suffix in self.__step3_suffixes:
            if rv.endswith(suffix):
                if suffix in ("e", "\xE9"):
                    word = word[:-len(suffix)]
                    rv = rv[:-len(suffix)]

                    if word[-2:] == "gu" and rv[-1] == "u":
                        word = word[:-1]
                else:
                    word = word[:-len(suffix)]
                break

        word = (word.replace("\xE1", "a").replace("\xE9", "e")
                    .replace("\xED", "i").replace("\xF3", "o")
                    .replace("\xFA", "u"))
        return word
