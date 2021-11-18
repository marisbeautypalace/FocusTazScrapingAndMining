import Focus.FocusScraper as fc
import Taz.TazScraper as tc
import threading

allResortsUrlsFocus = [
    ['https://www.focus.de/politik/schlagzeilen/', 'Politik'],
    ['https://www.focus.de/finanzen/schlagzeilen/', 'Finanzen'],
    ['https://www.focus.de/wissen/schlagzeilen/', 'Wissen'],
    ['https://www.focus.de/gesundheit/schlagzeilen/', 'Gesundheit'],
    ['https://www.focus.de/kultur/schlagzeilen/', 'Kultur'],
    ['https://www.focus.de/panorama/schlagzeilen/', 'Panorama'],
    ['https://www.focus.de/sport/schlagzeilen/', 'Sport'],
    ['https://www.focus.de/digital/schlagzeilen/', 'Digital'],
    ['https://www.focus.de/reisen/schlagzeilen/', 'Reisen'],
    ['https://www.focus.de/auto/schlagzeilen/', 'Auto'],
]

allResortsUrlsTaz = [
    ['https://taz.de/Politik/!p4615/', 'Politik', 'Politik'],
    ['https://taz.de/!p4616/', 'Deutschland', 'Politik'],
    ['https://taz.de/!p4617/', 'Europa', 'Politik'],
    ['https://taz.de/!p4618/', 'Amerika', 'Politik'],
    ['https://taz.de/!p4621/', 'Afrika', 'Politik'],
    ['https://taz.de/!p4619/', 'Asien', 'Politik'],
    ['https://taz.de/!p4620/', 'Nahost', 'Politik'],
    ['https://taz.de/!p4622/', 'Netzpolitik', 'Politik'],
    ['https://taz.de/Oeko/!p4610/', 'Oeko', 'Oeko'],
    ['https://taz.de/!p4623/', 'Oekonomie', 'Oeko'],
    ['https://taz.de/!p4624/', 'Oekologie', 'Oeko'],
    ['https://taz.de/!p4629/', 'Arbeit', 'Oeko'],
    ['https://taz.de/!p4625/', 'Konsum', 'Oeko'],
    ['https://taz.de/!p4628/', 'Verkehr', 'Oeko'],
    ['https://taz.de/!p4636/', 'Wissenschaft', 'Oeko'],
    ['https://taz.de/!p4627/','Netzoekonomie', 'Oeko'],
    ['https://taz.de/Gesellschaft/!p4611/', 'Gesellschaft', 'Gesellschaft'],
    ['https://taz.de/!p4632/', 'Alltag', 'Gesellschaft'],
    ['https://taz.de/!p4633/', 'Debatte', 'Gesellschaft'],
    ['https://taz.de/!p4634/', 'Kolumnen', 'Gesellschaft'],
    ['https://taz.de/!p4630/', 'Medien', 'Gesellschaft'],
    ['https://taz.de/!p4635/', 'Bildung', 'Gesellschaft'],
    ['https://taz.de/!p4637/', 'Gesundheit', 'Gesellschaft'],
    ['https://taz.de/!p4638/', 'Reise', 'Gesellschaft'],
    ['https://taz.de/Kultur/!p4639/', 'Kultur'],
    ['https://taz.de/!p4640/', ' Musik', 'Kultur'],
    ['https://taz.de/!p4641/', 'Film', 'Kultur'],
    ['https://taz.de/!p4642/', 'Künste', 'Kultur'],
    ['https://taz.de/!p4643/', 'Buch', 'Kultur'],
    ['https://taz.de/!p4631/', 'Netzkultur', 'Kultur'],
    ['https://taz.de/Sport/!p4646/', 'Sport', 'Kultur'],
    ['https://taz.de/!p4647/', 'Fußball', 'Kultur'],
    ['https://taz.de/!p4648/',  'Kolumnen', 'Kultur'],
    ['https://taz.de/Berlin/!p4649/', 'Berlin', 'Berlin'],
    ['https://taz.de/Nord/!p4650/', 'Nord', 'Nord'],
    ['https://taz.de/!p4651/',  'Hamburg', 'Nord'],
    ['https://taz.de/!p4652/', 'Bremen', 'Nord'],
    ['https://taz.de/!p4653/', 'Kultur', 'Nord'],
    ['https://taz.de/Wahrheit/!p4644/', 'Wahrheit', 'Warheit'],
]

def main():
        fc.scrapeRawHtml(allResortsUrlsFocus)
        tc.scrapeRawHtml(allResortsUrlsTaz)
        # every 8h (28800.0 sek)
        threading.Timer(28800.0, main).start()

if __name__ == '__main__':
    main()