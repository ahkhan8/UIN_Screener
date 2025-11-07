# sectors.py
# PSX sector → tickers mapping (lists are taken from the screenshots you provided)

SECTOR_MAP = {
    "AUTOMOBILE ASSEMBLER": [
        "AGTL","ATLH","DFML","GAL","GHNI","HCAR","HINO","INDU","MTL","SAZEW"
    ],
    "AUTOMOBILE PARTS & ACCESSORIES": [
        "AGIL","ATBA","BELA","BWHL","DWAE","EXIDE","GTYR","LOADS","PTL","TBL","THALL"
    ],
    "CABLE & ELECTRICAL GOODS": [
        "EMCO","FCL","PAEL","PCAL","SIEM","WAVES","WAVESAPP"
    ],
    "CEMENT": [
        "ACPL","BWCL","CHCC","DBCI","DCL","DGKC","DNCC","FCCL","FECTC","FLYNG",
        "GWLC","KOHC","LUCK","MLCF","PIOC","POWER","SMCPL","THCCL","ZELP"
    ],
    "CHEMICAL": [
        "ARPL","BAPL","BERG","BIFO","BUXL","DAAG","DOL","DYNO","EPCL","GCIL","GCWL",
        "GGL","ICL","LCI","LOTCHEM","LPGL","NICL","NRSL","PAKOXY","PPVC","SARC",
        "SHCI","SITC","SPL","WAHN"
    ],
    "CLOSE - END MUTUAL FUND": ["HGFA","HIFA","INMF","PUDF","TSMF"],
    "COMMERCIAL BANKS": [
        "ABL","AKBL","BAFL","BAHL","BIPL","BML","BOK","BOP","FABL","HBL","HMB","JSBL",
        "MCB","MEBL","NBP","SBL","SCBPL","SNBL","UBL"
    ],
    "ENGINEERING": [
        "AGHA","ASL","ASTL","BCL","BECO","CSAP","DADX","DSL","HSPI","INIL","ISL",
        "ITTEFAQ","KSBP","MSCL","MUGHAL","MUGHALC","PECO"
    ],
    "FERTILIZER": ["AGL","AHCL","EFERT","FATIMA","FFC"],
    "FOOD & PERSONAL CARE PRODUCTS": [
        "ASC","BBFL","BFAGRO","BNL","CLOV","COLG","FCEPL","FFL","GIL","GLPL","ISIL",
        "MFFL","MFL","MUREB","NATF","NESTLE","NMFL","PREMA","QUICE","RMPL","SCL",
        "SHEZ","TOMCL","TREET","UNITY","UPFL","ZIL"
    ],
    "GLASS & CERAMICS": ["BGL","FRCL","GGGL","GHGL","GVGL","KCL","REGAL","STCL","TGL"],
    "INSURANCE": [
        "AGIC","AICL","ALAC","ALIFE","ASIC","ATIL","BIIC","CENI","CSIL","EFUG","EFUL",
        "EWIC","HICL","IGIHL","IGIL","JGICL","JLICL","PAKRI","PIL","PINL","PKGI","PRIC",
        "RICL","SHNI","SSIC","SWL","TPLI","TPLL","UNIC","UVIC"
    ],
    "INV. BANKS / INV. COS. / SECURITIES COS.": [
        "786","AHL","AKDSL","AMBL","AMSL","CASH","CYAN","DEL","DHPL","DLL","ENGROH","ESBL",
        "FCEL","FCIBL","FCSC","FDPL","FNEL","ICIBL","IML","IMS","JSCL","JSGCL","JSIL",
        "LSECL","LSEFSL","LSEVL","MCBIM","NEXT","OLPL","PASL","PIAHCLA","PIAHCLB","PRIB",
        "PSX","SIBL","TRIBL","TSBL"
    ],
    "JUTE": ["CJPL","SUHJ"],
    "LEASING COMPANIES": ["ENGL","GRYL","PGLC","PICL","SLCL","SLL","SPCL"],
    "LEATHER & TANNERIES": ["BATA","FIL","LEUL","PAKL","SGF","SRVI"],
    "MISCELLANEOUS": [
        "AKDHL","AKGL","ARPAK","DCTL","DIIL","ECOP","GAMON","GEMPACRA","GOC","HADC",
        "MWMP","OML","PABC","PHDL","PSEL","SHFA","STPL","TRIPF","UBDL","UDIL","UDPL"
    ],
    "MODARABAS": [
        "BFMOD","FANM","FCONM","FECM","FEM","FFLM","FHAM","FIBLM","FIMM","FIMW","FNBM",
        "FPJM","FPRM","FTMM","FTSM","GEMBCEM","OLPM","ORM","PIM","SINDM","TRSM","UCAPM","WASL"
    ],
    "OIL & GAS EXPLORATION COMPANIES": ["MARI","OGDC","POL","PPL"],
    "OIL & GAS MARKETING COMPANIES": ["APL","BPL","HASCOL","HTL","OBOY","PSO","SNGP","SSGC","WAFI"],
    "PAPER, BOARD & PACKAGING": [
        "ABSON","CEPB","CPPL","DBSL","GEMMAPL","IPAK","MACFL","MERIT","PKGS","PPP","RPL","SEPL","SPEL"
    ],
    "PHARMACEUTICALS": [
        "ABOT","AGP","BFBIO","CPHL","FEROZ","GLAXO","HALEON","HINOON","HPL","IBLHL","LIVEN","MACTER","OTSU","SEARL"
    ],
    "POWER GENERATION & DISTRIBUTION": [
        "ALTN","EPQL","GEMMEL","HUBC","KAPCO","KEL","KOHE","KOHP","LPL","NCPL","NPL","PKGP","SEL","SGPL","SPWL","TSPL"
    ],
    "PROPERTY": ["BRRG","HUSI","JVDC","PACE","TPLP"],
    "REFINERY": ["ATRL","CNERGY","NRL","PRL"],
    "REAL ESTATE INVESTMENT TRUST": ["DCR","GRR","IREIT","TPLRF1"],
    "SUGAR & ALLIED INDUSTRIES": [
        "AABS","ADAMS","AGSML","ALNRS","ANSM","BAFS","CHAS","DWSM","FRSM","HABSM","HRPL",
        "HWQS","JDWS","JSML","KPUS","MIRKS","MRNS","NONS","PMRS","SANSM","SASML","SHJS",
        "SHSM","SKRS","SML","TCORP","TICL","TSML"
    ],
    "SYNTHETIC & RAYON": [
        "AASM","DSFL","GATI","IBFL","IMAGE","NAFL","NSRM","PSYL","RUPL","SGABL"
    ],
    "TECHNOLOGY & COMMUNICATION": [
        "AIRLINK","AVN","GEMNETS","GEMSPNL","HUMNL","MDTL","NETSOL","OCTOPUS","PAKD","PTC",
        "STL","SYM","SYS","TELE","TPL","TPLT","TRG","WTL","ZAL"
    ],
    "TEXTILE COMPOSITE": [
        # (Long list — include any you need most; add more later as desired)
        "ADMM","ANL","ANTM","ARUJ","BHAT","BTL","CHBL","CLOPS","CRTM","FASM","FML","FSPWL",
        "FTHM","FZCM","GATI","GFL","HAEL","HAFR","HATM","ILP","INKL","ITNAZ","JUBS","KAKL",
        "KAYT","KML","KOTL","KTML","MEHT","MFTM","MSOT","MUGT","NCL","NIKA","NML","PASM","QUET",
        "REDCO","REWM","SAPT","SGT","SGTL","SFLT","STML","STYLERS","SURC","TAJT","TOWL","USMT","ZAHID"
    ],
    "TEXTILE SPINNING": [
        "AAL","AATM","AMTEX","ANNT","APOT","ARCTM","ASTM","AWTX","AZMT","CCM","CFL","CTM",
        "CWSM","DFSM","DINT","DKTM","DMC","DMTM","DSIL","DWTM","ELCM","ELSM","FAEL","GADT",
        "GLOT","GSPM","GUSM","GUTM","HAJT","HIRAT","HMIM","IDRT","IDSM","IDYM","JATM","JDMT",
        "JKSM","KOHTM","KOSM","KSTM","MQTM","NAGC","NATM","NCML","PRET","RCML","RUBY","SAIF",
        "SANE","SERT","SHCM","SHDT","SLYT","SNAI","SSML","SUTM","SZTM","TATM","ZUMA"
    ],
    "TEXTILE WEAVING": ["ASHT","HKKT","ICCI","MOHE","PRWM","SDOT","STJT","YOUW","ZTL"],
    "TRANSPORT": ["CLVL","GEMBLUEX","PIBTL","PICT","PNSC","SLGL"],
    "TOBACCO": ["KHTC","PAKT"],
    "VANASPATI & ALLIED INDUSTRIES": ["POML","SSOM","SURAJ"],
    "WOOLLEN": ["BNWM"],
    "EXCHANGE TRADED FUNDS": [
        "ACIETF","HBLTETF","JSGBETF","JSMFETF","MIIETF","MZNPETF","NBGPETF","NITGETF","UBLPEETF"
    ],
}
# Convenience: symbol → sector
SYMBOL_TO_SECTOR = {sym: sector for sector, syms in SECTOR_MAP.items() for sym in syms}
