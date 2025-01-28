Process
1. The 1,244 journals were copied from ERIC Journal and NonJournal Sources by Topic Area (https://eric.ed.gov/?journaltopics) into ``ERIC-journals-list.xlsx``.
2. ISSN-L for each journal was obtained from OpenAlex or ISSN Poral.
3. Using the ISSN-L, six Python scripts in ``data_collection`` were run to extract bibliographic metadata for each journal. All metadata saved to ``dataset-full.xlsx``.
4. Analysis of characteristics and publishing models of ERIC-indexed journals completed in ``analysis.py``.

``ERIC-journals-list.xlsx``
List of 1,244 journals, and their collection topic area, indexed by ERIC (https://eric.ed.gov/?journaltopics).

``data_collection``
Six Python scripts used to extract bibliographic metadata for each ERIC-indexed journals from: 
- OpenAlex: https://openalex.org/
- Directory of Open Access Journals: https://doaj.org/
- Jisc Open Policy Finder: https://openpolicyfinder.jisc.ac.uk/
- EZB: https://ezb.ur.de/
- OpenAPC: https://openapc.net/

``dataset-full.xlsx``
The bibliographic metadata for the 1,244 ERIC-indexed journals resulting from the six scripts.

``analysis.py``
Analyzes the characteristics and publishing models of ERIC-indexed journals and compares the adoption rates of Diamond and other open access models.