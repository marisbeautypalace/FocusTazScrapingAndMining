import Focus.FocusDataExtractor as fde
import Taz.TazDataExtractor as tde

def main():
    try:
        fde.extractData()
    except:
        print('cant extract focus data')

    try:
        tde.extractData()
    except:
        print('cant extract focus data')

if __name__ == '__main__':
    main()