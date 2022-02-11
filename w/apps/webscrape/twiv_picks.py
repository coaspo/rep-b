#!/usr/bin/env python3
import re

import requests
import webbrowser

TWIV_URL = 'https://www.microbe.tv/twiv/weekly-picks/'


def get_web_page(url: str):
    try:
        page = requests.get(url)
        txt = page.text
        if '<title>Page Not Found</title>' in txt:
            return 'NOT FOUND'
        return txt
    except Exception as exc:
        return 'NOT FOUND'


def scrape_pick_links(html: str):
    pick_links ={'BOOK':[], 'EDU':[], 'GOV':[], 'VIDEO':[], 'COM':[], 'MISC':[] }
    pick_types = [('amazon.com', 'BOOK'),
            ('amzn.', 'BOOK'),
            ('youtu.be', 'VIDEO'),
            ('nasa.gov', 'NASA'),
            ('napr.org', 'NPR'),
            ('wikipedia.org', 'WIKI'),
            ('.gov', 'GOV'),
            ('.com', 'COM'),
            ('.net', 'COM'),
            ('.org', 'ORG'),
            ('.edu', 'EDU')]  # .com is filtered out
    lines=html.split('\n')
    print('will scan', len(lines), 'lines')
    start_scanig = False
    special_urls = ['microbe.tv','virology.ws','nyti.ms','twit.tv']
    for line in lines:
       if not start_scanig:
          start_scanig = 'Weekly Science Picks' in line
       if  start_scanig:
         i = line.find('<a href="http')
         if i > -1:
            i2 = line.find('</a>', i)
            if i2 > -1:
               link = line[i: i2+4]
               if 'astore.amazon.com' in link:
                 # skip link because it does not work
                 i = link.find('">')
                 i2 = link.find('</a', i)
                 pick_links.get('BOOK').append(link[i+2:i2]+ ' BOOK')
               else:
                 known_link = False
                 for pick_type in pick_types:
                   if pick_type[0] in link:
                     link = link + ' '+ pick_type[1]
                     if pick_type[1] == 'BOOK':
                        pick_links.get('BOOK').append(link)
                     elif pick_type[1] == 'EDU' or pick_type[1] == 'WIKI':
                        pick_links.get('EDU').append(link)
                     elif pick_type[1] == 'NASA' or pick_type[1] == 'GOV':
                        pick_links.get('GOV').append(link)
                     elif pick_type[1] == 'VIDEO':
                        pick_links.get('VIDEO').append(link)
                     elif pick_type[1] == 'COM' or pick_type[1] == 'ORG':
                        pick_links.get('COM').append(link)
                     else:
                       print('err; invalid pick type:', pick_type[1], 'link=', link)
                     known_link = True
                     break
                     #https://twit.tv/
                 if not known_link:
                    for url in special_urls:
                      if url in link:
                        link = link + ' ' + url
                        break
                    else:
                      # for example find uk in: http://www.bbc.co.uk/programmes/b00bw51j
                      i = link.find('//') + 4
                      i2 = link.find('/', i)
                      i = link.rfind('.', i2-5, i2) + 1  #http://www.overv.eu/
                      domain = link[i:i2]
                      country = DOMAINS.get(domain)
                      link = link + ' '+ (domain if country is None else country)
                    pick_links.get('MISC').append(link)
    return pick_links


def create_web_page(pick_links,link_type):
    html = '<html><title>Scannable TWIV picks</title>\n<body>'
    html += link_type + " picks from: "
    html += "<a href=\"{0}\">{1}</a><pre>".format(TWIV_URL, TWIV_URL)
    i = 0
    for link in pick_links:
        i += 1
        html += str(i)+ '  '+link +'\n'
    html += '</pre></body></html>'
    return html


def main():
    try:
        print('start')
        html = get_web_page(TWIV_URL)
        print('read ', len(html), 'characters from', TWIV_URL)
        pick_links = scrape_pick_links(html)
        link_types =['BOOK', 'EDU', 'GOV', 'VIDEO', 'COM', 'MISC']
        for link_type in link_types:
           links = pick_links.get(link_type)
           if len(links) == 0:
             print('did not find', link_type, 'links')
           html_page = create_web_page(links, link_type)
           file_path = './twiv_picks_'+link_type+'.html'
           with open(file_path, 'w') as f:
              f.write(html_page)
           #webbrowser.open_new_tab(file_path)
           print('created', file_path)
        print('done')
    except Exception as exc:
        print(exc)
        import traceback
        traceback.print_exc()
DOMAINS ={
'ac':'Ascension Island',
'ad':'Andorra',
'ae':'UAE',
'af':'Afghanistan',
'ag':'Antigua',
'ai':'Anguilla',
'al':'Albania',
'am':'Armenia',
'ao':'Angola',
'aq':'Antarctica',
'ar':'Argentina',
'as':'American Samoa',
'at':'Austria',
'au':'Australia',
'aw':'Aruba',
'ax':'Åland',
'az':'Azerbaijan',
'ba':'Bosniaa',
'bb':'Barbados',
'bd':'Bangladesh',
'be':'Belgium',
'bf':'Burkina Faso',
'bg':'Bulgaria',
'bh':'Bahrain',
'bi':'Burundi',
'bj':'Benin',
'bl':'Saint Barthélemy',
'bm':'Bermuda',
'bn':'Brunei',
'bo':'Bolivia',
'bq':'Bonaire',
'br':'Brazil',
'bs':'Bahamas',
'bt':'Bhutan',
'bv':'Bouvet Island',
'bw':'Botswana',
'by':'Belarus',
'bz':'Belize',
'ca':'Canada',
'cat':'Catalonia',
'cc':'Cocos Islands',
'cd':'Congo, DRC',
'cf':'Central Africa',
'cg':'Congo, RC',
'ch':'Switzerland',
'ci':'Côte d’Ivoire',
'ck':'Cook Islands',
'cl':'Chile',
'cm':'Cameroon',
'cn':'China',
'co':'Colombia',
'cr':'Costa Rica',
'cu':'Cuba',
'cv':'Cape Verde',
'cw':'Curaçao',
'cx':'Christmas Island',
'cy':'Cyprus',
'cz':'Czechia',
'de':'Germany',
'dj':'Djibouti',
'dk':'Denmark',
'dm':'Dominica',
'do':'Dominican Republic',
'dz':'Algeria',
'ec':'Ecuador',
'ee':'Estonia',
'eg':'Egypt',
'eh':'Western Sahara',
'er':'Eritrea',
'es':'Spain',
'et':'Ethiopia',
'eu':'European Union',
'eus':'Basque Country',
'fg':'French Guiana',
'fi':'Finland',
'fj':'Fiji',
'fk':'Falkland Islands',
'fm':'Micronesia',
'fo':'Faeroe Islands',
'fr':'France',
'ga':'Gabon',
'gal':'Galicia',
'gd':'Grenada',
'ge':'Georgia',
'gg':'Guernsey',
'gh':'Ghana',
'gi':'Gibraltar',
'gl':'Greenland',
'gm':'Gambia',
'gn':'Guinea',
'gp':'Guadeloupe',
'gp':'Saint Martin',
'gq':'Equatorial Guinea',
'gr':'Greece',
'gs':'South Georgia',
'gt':'Guatemala',
'gu':'Guam',
'gw':'Guinea-Bissau',
'gy':'Guyana',
'hk':'Hong Kong',
'hm':'Heard Island',
'hn':'Honduras',
'hr':'Croatia',
'ht':'Haiti',
'hu':'Hungary',
'id':'Indonesia',
'ie':'Ireland',
'il':'Israel',
'im':'Isle of Man',
'in':'India',
'io':'British Indian Territory',
'iq':'Iraq',
'ir':'Iran',
'is':'Iceland',
'it':'Italy',
'je':'Jersey',
'jm':'Jamaica',
'jo':'Jordan',
'jp':'Japan',
'ke':'Kenya',
'kg':'Kyrgyzstan',
'kh':'Cambodia',
'ki':'Kiribati',
'km':'Comoros',
'kn':'Saint Kitts and Nevis',
'kp':'North Korea',
'kr':'Korea, South',
'kr':'South Korea',
'kw':'Kuwait',
'ky':'Cayman Islands',
'kz':'Kazakhstan',
'la':'Laos',
'lb':'Lebanon',
'lc':'Saint Lucia',
'li':'Liechtenstein',
'lk':'Sri Lanka',
'lr':'Liberia',
'ls':'Lesotho',
'lt':'Lithuania',
'lu':'Luxembourg',
'lv':'Latvia',
'ly':'Libya',
'ma':'Morocco',
'mc':'Monaco',
'md':'Moldova',
'me':'Montenegro',
'mg':'Madagascar',
'mh':'Marshall Islands',
'mk':'Macedonia, North',
'mk':'North Macedonia',
'ml':'Mali',
'mm':'Burma',
'mm':'Myanmar',
'mn':'Mongolia',
'mo':'Macau',
'mp':'Northern Mariana Islands',
'mq':'Martinique',
'mr':'Mauritania',
'ms':'Montserrat',
'mt':'Malta',
'mu':'Mauritius',
'mv':'Maldives',
'mw':'Malawi',
'mx':'Mexico',
'my':'Malaysia',
'mz':'Mozambique',
'na':'Namibia',
'nc':'New Caledonia',
'ne':'Niger',
'nf':'Norfolk Island',
'ng':'Nigeria',
'ni':'Nicaragua',
'nl':'Holland',
'nl':'Netherlands',
'no':'Norway',
'np':'Nepal',
'nr':'Nauru',
'nu':'Niue',
'nz':'New Zealand',
'om':'Oman',
'pa':'Panama',
'pe':'Peru',
'pf':'Tahiti',
'pg':'Papua New Guinea',
'ph':'Philippines',
'pk':'Pakistan',
'pl':'Poland',
'pm':'Saint-Pierre',
'pn':'Pitcairn Islands',
'pr':'Puerto Rico',
'ps':'Palestine',
'pt':'Portugal',
'pw':'Palau',
'py':'Paraguay',
'qa':'Qatar',
're':'Réunion',
'ro':'Romania',
'rs':'Serbia',
'ru':'Russia',
'rw':'Rwanda',
'sa':'Saudi Arabia',
'sb':'Solomon Islands',
'sc':'Seychelles',
'sd':'Sudan',
'se':'Sweden',
'sg':'Singapore',
'sh':'Saint Helena',
'si':'Slovenia',
'sj':'Svalbard',
'sk':'Slovakia',
'sl':'Sierra Leone',
'sm':'San Marino',
'sn':'Senegal',
'so':'Somalia',
'sr':'Suriname',
'ss':'South Sudan',
'st':'São Tomé',
'sv':'El Salvador',
'sx':'Sint Maarten',
'sy':'Syria',
'sz':'Swaziland',
'tc':'Turks',
'td':'Chad',
'tf':'French Southern Lands',
'tg':'Togo',
'th':'Thailand',
'tj':'Tajikistan',
'tk':'Tokelau',
'tl':'East Timor',
'tm':'Turkmenistan',
'tn':'Tunisia',
'to':'Tonga',
'tr':'Turkey',
'tt':'Trinidad',
'tv':'Tuvalu',
'tw':'Taiwan',
'tz':'Tanzania',
'ug':'Uganda',
'uk':'UK',
'us':'USA',
'uy':'Uruguay',
'uz':'Uzbekistan',
'va':'Vatican City',
'vc':'Saint Vincen',
've':'Venezuela',
'vg':'British Virgin Islands',
'vi':'US Virgin Islands',
'vn':'Vietnam',
'vu':'Vanuatu',
'wf':'Wallis',
'ws':'Samoa',
'ye':'Yemen',
'yt':'Mayotte',
'za':'South Africa',
'zm':'Zambia',
'zw':'Zimbabwe'
}

main()
