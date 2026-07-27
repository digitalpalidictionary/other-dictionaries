"""Path definitions for the other-dictionaries repository."""

from pathlib import Path
from typing import Optional


class RepoPaths:
    """Paths for the standalone other-dictionaries repository."""

    def __init__(self, base_dir: Optional[Path] = None, create_dirs: bool = True):
        if base_dir is None:
            base_dir = Path(__file__).resolve().parent.parent.parent

        self.base_dir = base_dir
        self.dictionaries_dir = base_dir / "dictionaries"

        self.build_dir = base_dir / "build"
        self.goldendict_path = self.build_dir / "goldendict"
        self.mdict_path = self.build_dir / "mdict"

        self.bmp_files_path = base_dir / "bmp_files"

        self._setup_abt_paths()
        self._setup_apte_paths()
        self._setup_bhs_paths()
        self._setup_bold_def_paths()
        self._setup_cone_paths()
        self._setup_cpd_paths()
        self._setup_dppn_paths()
        self._setup_dpr_paths()
        self._setup_mw_paths()
        self._setup_nyanatiloka_paths()
        self._setup_peu_paths()
        self._setup_simsapa_paths()
        self._setup_sin_eng_sin_paths()
        self._setup_whitney_paths()
        self._setup_wordnet_paths()

        if create_dirs:
            self.create_dirs()

    def _setup_abt_paths(self):
        d = self.dictionaries_dir / "abt"
        self.abt_source_path = d / "source" / "CPED.csv"
        self.abt_gd_path = self.goldendict_path
        self.abt_mdict_path = self.mdict_path

    def _setup_apte_paths(self):
        d = self.dictionaries_dir / "apte"
        self.apte_source_dir = d / "source" / "web" / "sqlite"
        self.apte_zip_path = d / "source" / "ap90web1.zip"
        self.apte_json_path = d / "source" / "apte.json"
        self.apte_css_path = d / "apte.css"
        self.apte_gd_path = self.goldendict_path
        self.apte_mdict_path = self.mdict_path

    def _setup_bhs_paths(self):
        d = self.dictionaries_dir / "bhs"
        self.bhs_source_path = d / "source" / "bhs.xml"
        self.bhs_gd_path = self.goldendict_path
        self.bhs_mdict_path = self.mdict_path

    def _setup_bold_def_paths(self):
        d = self.dictionaries_dir / "bold_def"
        self.bold_def_source_path = d / "source" / "bold_definitions.tsv"
        self.bold_def_template_path = d / "bold_definitions.html"
        self.bold_def_gd_path = self.goldendict_path
        self.bold_def_mdict_path = self.mdict_path

    def _setup_cone_paths(self):
        d = self.dictionaries_dir / "cone"
        self.cone_source_path = d / "source" / "cone_dict.json"
        self.cone_front_matter_path = d / "source" / "cone_front_matter.json"
        self.cone_css_path = d / "cone.css"
        self.cone_gd_path = self.goldendict_path
        self.cone_mdict_path = self.mdict_path

    def _setup_cpd_paths(self):
        d = self.dictionaries_dir / "cpd"
        self.cpd_source_path = d / "source" / "cpd_clean.db"
        self.cpd_css_path = d / "cpd.css"
        self.cpd_gd_path = self.goldendict_path
        self.cpd_mdict_path = self.mdict_path

    def _setup_dppn_paths(self):
        d = self.dictionaries_dir / "dppn"
        self.dppn_source_path = d / "source" / "DPPN.json"
        self.dppn_css_path = d / "dppn.css"
        self.dppn_gd_path = self.goldendict_path
        self.dppn_mdict_path = self.mdict_path

    def _setup_dpr_paths(self):
        d = self.dictionaries_dir / "dpr"
        self.dpr_source_path = d / "source" / "dpr.json"
        self.dpr_css_path = d / "dpr.css"
        self.dpr_gd_path = self.goldendict_path
        self.dpr_mdict_path = self.mdict_path

    def _setup_mw_paths(self):
        d = self.dictionaries_dir / "mw"
        self.mw_source_dir = d / "source" / "web" / "sqlite"
        self.mw_zip_path = d / "source" / "mwweb1.zip"
        self.mw_json_path = d / "source" / "mw.json"
        self.mw_css_path = d / "mw.css"
        self.mw_gd_path = self.goldendict_path
        self.mw_mdict_path = self.mdict_path

    def _setup_nyanatiloka_paths(self):
        d = self.dictionaries_dir / "nyanatiloka"
        self.nyanatiloka_source_path = d / "source" / "nyanatiloka.json"
        self.nyanatiloka_css_path = d / "nyanatiloka.css"
        self.nyanatiloka_gd_path = self.goldendict_path
        self.nyanatiloka_mdict_path = self.mdict_path

    def _setup_peu_paths(self):
        d = self.dictionaries_dir / "peu"
        self.peu_source_path = d / "source" / "peu_dump.js"
        self.peu_gd_path = self.goldendict_path
        self.peu_mdict_path = self.mdict_path

    def _setup_simsapa_paths(self):
        d = self.dictionaries_dir / "simsapa"
        self.simsapa_source_path = d / "source" / "simsapa.json"
        self.simsapa_gd_path = self.goldendict_path
        self.simsapa_mdict_path = self.mdict_path

    def _setup_sin_eng_sin_paths(self):
        d = self.dictionaries_dir / "sin_eng_sin"
        self.sin_eng_source_path = d / "source" / "sinhala-english.tab"
        self.eng_sin_source_path = d / "source" / "english-sinhala.tab"
        self.sin_eng_sin_gd_path = self.goldendict_path
        self.sin_eng_sin_mdict_path = self.mdict_path

    def _setup_whitney_paths(self):
        d = self.dictionaries_dir / "whitney"
        self.whitney_source_dir = d / "source"
        self.whitney_css_path = d / "whitney.css"
        self.whitney_gd_path = self.goldendict_path
        self.whitney_mdict_path = self.mdict_path

    def _setup_wordnet_paths(self):
        d = self.dictionaries_dir / "wordnet"
        self.wordnet_data_path = d / "source"

    def create_dirs(self):
        for d in [self.goldendict_path, self.mdict_path]:
            d.mkdir(parents=True, exist_ok=True)
