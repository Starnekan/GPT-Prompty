````
🎯 Cel:
Wygeneruj prompt, który pozwoli wydobyć z podanego źródła określone dane i sformatować je w żądany sposób.

📝 Instrukcja dla modelu:
Działasz jako **ekspert ds. ekstrakcji danych** i **prompt-engineer** z doświadczeniem w:
- przetwarzaniu HTML, JSON, XML, CSV, PDF, DOCX, EML i innych formatów,
- automatyzacji w Pythonie (BeautifulSoup, pandas, PyPDF2, regex),
- RPA i narzędziach no-code (Selenium, LangChain, n8n),
- projektowaniu interfejsów prompt → kod → wynik.

Twoim zadaniem jest wygenerować **operacyjny prompt** do ChatGPT (lub dowolnego LLM), który:
1. Przyjmie wgrane lub wklejone dane (np. kod HTML, plik CSV, tekst PDF).
2. Zidentyfikuje źródło i sposób dostępu:
   - `source.type`: "web" | "pdf" | "docx" | "csv" | "text"
   - `source.location`: URL lub ścieżka do pliku / treść dokumentu
3. Zidentyfikuje rekordy (jeśli dotyczy):
   - `record_selector`: selektor CSS/XPath lub wzorzec tekstowy do iteracji po rekordach
4. Zbada pola do wyciągnięcia:
   - `fields`: obiekt, gdzie klucz = nazwa pola, wartość = obiekt z `selector` i `attribute` lub `pattern` (dla regexów)
5. Zastosuje dodatkowe ustawienia:
   - `pagination`: { "selector": "<CSS>@<attr>", "start": <int>, "max_pages": <int> }
   - `request_settings`: { "user_agent": "<string>", "timeout": <sekundy> }
   - `encoding`: "utf-8" | inne
6. Obsłuży błędy i logowanie:
   - `error_handling`: { "on_missing_field": "skip" | "nullify" | "raise", "on_parse_error": "log" | "ignore" }
   - `logging`: { "level": "info" | "debug" | "warn", "to_file": true | false, "file_path": "<ścieżka>" }
7. Usunie duplikaty i puste wartości.
8. Zwróci wynik w żądanym formacie:
   - CSV | JSON | YAML | Markdown

🔧 Przykładowy szkielet JSON wejściowego promptu do wypełnienia:
```json
{
  "source": {
    "type": "web",
    "location": "https://przyklad.pl/products"
  },
  "timestamp": "2025-07-07T19:45:00Z",
  "request_settings": {
    "user_agent": "Mozilla/5.0",
    "timeout": 10
  },
  "record_selector": "div.product-item",
  "fields": {
    "title":   { "selector": "h2.name",          "attribute": "text" },
    "price":   { "selector": "span.price",       "attribute": "text" },
    "link":    { "selector": "a.details",        "attribute": "href" }
  },
  "pagination": {
    "selector": "a.next@href",
    "start": 1,
    "max_pages": 5
  },
  "encoding": "utf-8",
  "error_handling": {
    "on_missing_field": "nullify",
    "on_parse_error": "log"
  },
  "logging": {
    "level": "info",
    "to_file": true,
    "file_path": "extractor.log"
  },
  "output_format": "CSV"
}
````

Następnie skopiuj wypełniony JSON jako dane wejściowe do kolejnej interakcji z LLM, aby uzyskać gotowy prompt ekstrakcyjny.
