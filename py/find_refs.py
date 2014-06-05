from lxml import html
import requests

def scrape_references(name):
    name4url = name.replace(' ', '+')

    url = 'http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=%s&extend=no&hconst=73&omegam=0.27&omegav=0.73&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=YES' %(name4url)

    page = requests.get(url)
    tree = html.fromstring(page.text)
    refs = tree.xpath('//a[@target="ned_dw"]/text()')
    print name
    print 'there are%s references for this galaxy' %(refs[0])
    return refs[0]

if __name__ == "__main__":

    scrape_references('IC 1613')
    scrape_references('NGC 4258')
    scrape_references('UGC 7332')
