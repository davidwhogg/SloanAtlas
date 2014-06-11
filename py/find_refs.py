from lxml import html
import requests
import time
import pyfits

def scrape_references(name):

    if 'A ' and '+' in name:
        print table[names == name]['CG_RA'][0], table[names == name]['CG_DEC'][0]
        name = str(name).replace(' ', '')
        print name
        
        name = name.split('+')
        url = 'http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=%5{0}%5D+{1}%2B{2}&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES'.format('BRC2', name[0], name[1])
        print url

    elif 'MCG' in name:
        name=name.replace(' ', '+')
        print name
        url = 'http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname={0}&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES'.format(name)

    elif 'A ' and '-' in name:
        name = name.replace(' ', '')
        url = 'http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=%5{0}%5D+{1}&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES'.format('BRC2',name)
        print url

    else:
        name4url = name.replace(' ', '+')
        url = 'http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=%s&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES' %(name4url)

    page = requests.get(url)
    tree = html.fromstring(page.text)
    refs = tree.xpath('//a[@target="ned_dw"]/text()')
    #print refs
    print name, refs[0]
    return refs[0]

if __name__ == "__main__":
    table = pyfits.open('sdss_atlas_plates_quants.fits')[1].data
    names = table['NAME']
    ra = table['CG_RA']
    dec = table['CG_DEC']
    output = open('number_of_references_A.txt', 'w+')
    #scrape_references('A 0107+42')
    for name in names:
        if 'PEG' in name:
            continue
        if 'HOLM' in name:
            continue
        if 'NSA' in name:
            continue
        if 'LEO' in name:
            continue

        output.write('%s%s \n' %(name.replace(' ','_'),scrape_references(name)))
        time.sleep(2)

    # scrape_references('IC 1613')
    # scrape_references('NGC 4258')
    # scrape_references('UGC 7332')
