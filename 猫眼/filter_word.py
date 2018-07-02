from fontTools.ttLib import TTFont
import pymongo
import woff2otf
def map_rule():
    woff2otf.convert("maoyan.woff", "maoyan.otf")
    baseFont = TTFont('base.otf')
    maoyanFont = TTFont('maoyan.otf')
    uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()
    numList = []
    baseNumList = ['.', '3', '5', '1', '2', '7', '0', '6', '9', '8', '4']
    baseUniCode = ['x', 'uniE64B', 'uniE183', 'uniED06', 'uniE1AC', 'uniEA2D', 'uniEBF8',
    'uniE831', 'uniF654', 'uniF25B', 'uniE3EB']
    for i in range(1, 12):
        maoyanGlyph = maoyanFont['glyf'][uniList[i]]
        for j in range(11):
            baseGlyph = baseFont['glyf'][baseUniCode[j]]
            if maoyanGlyph == baseGlyph:
                numList.append(baseNumList[j])
                break
    uniList = [i.lower() for i in uniList]
    return dict(zip(uniList[2:], numList[1:]))
def rule_(content):
    f = open("maoyan.woff","wb")
    f.write(content)
    f.close()
    return map_rule()
if __name__ == '__main__':
    # get_rule()
    pass
