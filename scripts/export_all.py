from dictionaries.abt.abt_glossary import main as abt
from dictionaries.bhs.bhs import main as bhs
from dictionaries.bold_def.bold_definitions import BoldDefinitions
from dictionaries.cone.cone import main as cone
from dictionaries.cpd.cpd import main as cpd
from dictionaries.dppn.dppn import main as dppn
from dictionaries.dpr.dpr import main as dpr
from dictionaries.mw.mw_from_cologne import main as mw
from dictionaries.peu.peu import main as peu
from dictionaries.simsapa.simsapa_combined import main as simsapa
from dictionaries.sin_eng_sin.sin_eng_sin import main as sin_eng_sin
from dictionaries.whitney.whitney import main as whitney

from vendor.dpd_tools.printer import printer as pr


def main():
    pr.title("exporting all dictionaries in goldendict and mdict format")

    # Decompress sources first
    from scripts.decompress_sources import decompress_sources

    decompress_sources()

    abt()
    bhs()
    BoldDefinitions().run()
    cone()
    cpd()
    dppn()
    dpr()
    mw()
    peu()
    simsapa()
    sin_eng_sin()
    whitney()

    pr.green_title("all dictionaries exported successfully!")


if __name__ == "__main__":
    main()
