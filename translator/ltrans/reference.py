import transliterate

LANGUAGE_NAMES_ABBR = {"Abkhazian": "ab",
                       "Afar": "aa",
                       "Afrikaans": "af",
                       "Albanian": "sq",
                       "Amharic": "am",
                       "Arabic": "ar",
                       "Armenian": "hy",
                       "Assamese": "as",
                       "Aymara": "ay",
                       "Azerbaijani": "az",
                       "Bashkir": "ba",
                       "Basque": "eu",
                       "Bengali": "bn",
                       "Bhutani": "dz",
                       "Bihari": "bh",
                       "Bislama": "bi",
                       "Breton": "br",
                       "Bulgarian": "bg",
                       "Burmese": "my",
                       "Byelorussian": "be",
                       "Cambodian": "km",
                       "Catalan": "ca",
                       "Chinese": "zh",
                       "Corsican": "co",
                       "Croatian": "hr",
                       "Czech": "cs",
                       "Danish": "da",
                       "Dutch": "nl",
                       "English": "en",
                       "Esperanto": "eo",
                       "Estonian": "et",
                       "Faeroese": "fo",
                       "Fiji": "fj",
                       "Finnish": "fi",
                       "French": "fr",
                       "Frisian": "fy",
                       "Scots Gael": "gd",
                       "Galician": "gl",
                       "Georgian": "ka",
                       "German": "de",
                       "Greek": "el",
                       "Greenlandic": "kl",
                       "Guarani": "gn",
                       "Gujarati": "gu",
                       "Hausa": "ha",
                       "Hebrew": "iw",
                       "Hindi": "hi",
                       "Hungarian": "hu",
                       "Icelandic": "is",
                       "Indonesian": "in",
                       "Interlingua": "ia",
                       "Interlingue": "ie",
                       "Inupiak": "ik",
                       "Irish": "ga",
                       "Italian": "it",
                       "Japanese": "ja",
                       "Javanese": "jw",
                       "Kannada": "kn",
                       "Kashmiri": "ks",
                       "Kazakh": "kk",
                       "Kinyarwanda": "rw",
                       "Kirghiz": "ky",
                       "Kirundi": "rn",
                       "Korean": "ko",
                       "Kurdish": "ku",
                       "Laothian": "lo",
                       "Latin": "la",
                       "Latvian": "lv",
                       "Lingala": "ln",
                       "Lithuanian": "lt",
                       "Macedonian": "mk",
                       "Malagasy": "mg",
                       "Malay": "ms",
                       "Malayalam": "ml",
                       "Maltese": "mt",
                       "Maori": "mi",
                       "Marathi": "mr",
                       "Moldavian": "mo",
                       "Mongolian": "mn",
                       "Nauru": "na",
                       "Nepali": "ne",
                       "Norwegian": "no",
                       "Occitan": "oc",
                       "Oriya": "or",
                       "Oromo, Afan": "om",
                       "Pashto": "ps",
                       "Persian": "fa",
                       "Polish": "pl",
                       "Portuguese": "pt",
                       "Punjabi": "pa",
                       "Quechua": "qu",
                       "Rhaeto-Rom": "rm",
                       "Romanian": "ro",
                       "Russian": "ru",
                       "Samoan": "sm",
                       "Sangro": "sg",
                       "Sanskrit": "sa",
                       "Serbian": "sr",
                       "Serbo-Croat": "sh",
                       "Sesotho": "st",
                       "Setswana": "tn",
                       "Shona": "sn",
                       "Sindhi": "sd",
                       "Singhalese": "si",
                       "Siswati": "ss",
                       "Slovak": "sk",
                       "Slovenian": "sl",
                       "Somali": "so",
                       "Spanish": "es",
                       "Sudanese": "su",
                       "Swahili": "sw",
                       "Swedish": "sv",
                       "Tagalog": "tl",
                       "Tajik": "tg",
                       "Tamil": "ta",
                       "Tatar": "tt",
                       "Tegulu": "te",
                       "Thai": "th",
                       "Tibetan": "bo",
                       "Tigrinya": "ti",
                       "Tonga": "to",
                       "Tsonga": "ts",
                       "Turkish": "tr",
                       "Turkmen": "tk",
                       "Twi": "tw",
                       "Ukrainian": "uk",
                       "Urdu": "ur",
                       "Uzbek": "uz",
                       "Vietnamese": "vi",
                       "Volapuk": "vo",
                       "Welsh": "cy",
                       "Wolof": "wo",
                       "Xhosa": "xh",
                       "Yiddish": "ji",
                       "Yoruba": "yo",
                       "Zulu": "zu"
                       }

LANGUAGE_ABBRS_NAMES = {v: k for k, v in LANGUAGE_NAMES_ABBR.items()}

TRANSLITERATE_LANGUAGE_NAMES = [LANGUAGE_ABBRS_NAMES.get(abbr) if LANGUAGE_ABBRS_NAMES.get(abbr) is not None else abbr
                                for abbr in transliterate.get_available_language_codes()]

print('Transliterate languages: ', TRANSLITERATE_LANGUAGE_NAMES)
