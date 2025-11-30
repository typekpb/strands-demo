# Demo time:

1. Launch the `main.py`
1. 
    INPUT:
    ```
    search for thesis for keyword: "analyza legislativy pre autonomne vozidla" in CZRP and show me the abstract
    ```

    OUTPUT:
    ```
    <thinking> To find the thesis with the keyword "analyza legislativy pre autonomne vozidla" in the CZRP repository, I will use the `thesis_fetch` tool. Once I have the thesis details, I will use the `thesis_abstract_fetch` tool to retrieve the abstract. </thinking>

    Tool #1: thesis_fetch
    Found 1 RSS records
    <thinking> I have found the thesis titled "Analýza legislatívy pre autonómne vozidlá". Now, I will use the `thesis_abstract_fetch` tool to retrieve the abstract of this thesis. </thinking> 
    Tool #2: thesis_abstract_fetch
    Found 1 records
    Here is the abstract of the thesis titled "Analýza legislatívy pre autonómne vozidlá":

    ---

    **Abstract:**

    Potenciálnym nástupcom dnešných,
    ```
1. INPUT: `show me the levels of autonomy described in the thesis`
   OUTPUT (pdf reader unavailable):
   ```
   <thinking> Since I cannot directly read or analyze PDF files, I need to inform the user that I cannot provide the levels of autonomy described in the thesis. I will suggest that the user download the PDF to review it themselves. </thinking>
   ```
   OUTPUT (pdf reader available):
   ```
   <thinking> To find the levels of autonomy described in the thesis, I will need to retrieve the PDF of the thesis if it is available. Once I have the PDF, I will convert it to markdown to extract the relevant information. </thinking> 
    Tool #3: thesis_retrieve_pdf_if_available
    Cookies banner clicked.
    Downloaded to: /var/folders/yw/00997t25333_zdby24hp6j4w0000gn/T/1551b61b8274423d852e04cf1cdfe34d.pdf
    <thinking> I have retrieved the PDF of the thesis. Now, I will convert the PDF to markdown to extract the levels of autonomy described in the thesis. </thinking> 
    Tool #4: convert_pdf_to_markdown
    [11/30/25 19:55:16] INFO     Processing request of type            server.py:674
                                 CallToolRequest                                    
    Here are the levels of autonomy described in the thesis:
    
    ---
    
    **1.2 Úrovne autonómie u autonómnych vozidiel**
    
    **1.2.1 Úroveň 0**
    - Žiadna autonómia. Vozidlo je riadené vodičom bez akejkoľvek pomoci od systému.
    
    **1.2.2 Úroveň 1**
    - Čiastočná autonómia. Vozidlo môže automaticky spomaliť alebo zrýchliť, ale vodič musí stále udržiavať kontrolu nad riadením a brzdenie.
    
    **1.2.3 Úroveň 2**
    - Čiastočná autonómia s automatizovaným riadením. Vozidlo môže automaticky riadiť a brzdiť, ale vodič musí byť pripravený prevziať kontrolu v prípade potreby.
    
    **1.2.4 Úroveň 3**
    - Podmienená autonómia. Vozidlo môže úplne prevziať kontrolu v určitých situáciách, ale vodič musí byť pripravený prevziať kontrolu, keď systém požiada.
    
    **1.2.5 Úroveň 4**
    - Vysoká autonómia. Vozidlo môže úplne prevziať kontrolu vo väčšine situácií, ale vodič musí byť stále prítomný a pripravený prevziať kontrolu, keď je to potrebné.
    
    **1.2.6 Úroveň 5**
    - Plná autonómia. Vozidlo môže úplne prevziať kontrolu vo všetkých situáciách bez potreby ľudského zásahu.
 
   ```

# Development: scraping proces

1. Playwright used for scraping
    ```shell
    npx playwright codegen https://opac.crzp.sk/
    ```