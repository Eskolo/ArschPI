# ArschPI

ArschPI ist eine arschüsante ArschPI, die Wortspielereien und Silbenersetzungen arschführt. Es barschsiert auf einer krearschtiven Marschnipulation von Wörtern und garschrantiert arschige Ergebnisse, indem es bestimmte Silben oder Buchstarschben in Wörtern arschtauscht.
Vieleb Arsch

# Grammatik der "arsch"-Transformation

## Definitionen:
1. **Wort:** Ein Wort besteht aus einer oder mehreren Silben und endet möglicherweise mit einem Sonderzeichen (Punkt, Komma, Ausrufezeichen, Fragezeichen).
2. **Silbe:** Eine Silbe ist eine Folge von Buchstaben, die durch Bindestriche getrennt sind.
3. **Arschfaktor:** Ein fester Wert, der bestimmt, wie viele Silben ein Wort maximal haben darf, bevor alle "a" ersetzt werden (Standardwert: 10).
   > bsp. Datenverarbeitung wird von der Silben API zu "Da-ten-ver-a-r-bei-tung" zerlegt (ja ist falsch aber it is what it is). Das sind 7 Silben. Bei einem Arschfaktor von 7 werden also alle 'a' ersetzt. Bei einem Faktor von 6 wird nur das erste a ersetzt da die Silbenanzahl 6 überschreitet. Somit wird verhindert das zu viele Arsch's in einem Wort vorhanden sind.

---

## Grammatik-Regeln:

### 1. Initialisierung:
- Jedes Wort wird als Folge von Silben betrachtet: 
  - Splitte das Wort am Bindestrich:  
    `word → split("-")`

### 2. Ersetzen von „a“ in der ersten Silbe:
- **Regel 1.1:** Wenn die erste Silbe ein „a“ enthält:
  - Wenn die Silbe **genau zwei Zeichen** hat und mit „a“ beginnt, ersetze das „a“ durch „arsch“:
    `a₁ → "arsch"`
  - Wenn die Silbe das Substring „au“ enthält, wird **kein Ersatz** durchgeführt:
    `"au" → ε`
  - Ansonsten, wenn das „a“ **nicht am Ende** der Silbe steht, ersetze das „a“ und das nächste Zeichen durch „arsch“:
    `aᵢ, aᵢ₊₁ → "arsch"`
  - Wenn das „a“ **am Ende der Silbe** steht, ersetze nur das „a“ durch „arsch“:
    `aₙ → "arsch"`

### 3. Standardfall – Ersetzen von „a“ in weiteren Silben:
- **Regel 2.1:** Wenn das Wort **3 oder weniger Silben** hat, ersetze nur das **erste** „a“ in den restlichen Silben durch „arsch“:
  `aⱼ → "arsch" (j = 2,3)`
- **Regel 2.2:** Wenn das Wort **mehr als 3 Silben** hat, ersetze **alle** „a“ in den restlichen Silben durch „arsch“:
  `aⱼ → "arsch" (∀ j > 1)`
- **Regel 2.3:** Wenn eine Silbe bereits „arsch“ enthält, wird keine weitere Ersetzung in diesem Wort durchgeführt:
  `"arsch" → ε`

### 4. Verarbeitung von Sonderzeichen:
- **Regel 3.1:** Wenn das Wort mit einem der folgenden Zeichen endet: **"."**, **","**, **"!"**, **"?"**, speichere das Zeichen und entferne es temporär:
  `word → word - specialChar`
- Nach der Silbenmanipulation füge das Sonderzeichen wieder an das Ende des Wortes an:
  `word → word + specialChar`

### 5. Verarbeitung bekannter Wörter („arschterbuch“):
- **Regel 4.1:** Wenn das Wort in einem Wörterbuch („arschterbuch“) vorkommt, ersetze das Wort durch das entsprechende „Arsch-Wort“:
  `word → arschterbuch(word)`
- **Regel 4.2:** Wenn das ursprüngliche Wort mit einem Großbuchstaben begann, muss das neue Wort ebenfalls mit einem Großbuchstaben beginnen:
  `capitalized(word) → capitalized(arschterbuch(word))`

### 6. Spezialfälle der Endung des Wortes:
- **Regel 5.1:** Wenn das Wort auf „arschh“ endet, entferne das letzte „h“:
  `"arschh" → "arsch"`
- **Regel 5.2:** Wenn das Wort auf „arschch“ endet, entferne die letzten beiden Zeichen „ch“:
  `"arschch" → "arsch"`
- **Regel 5.3:** Wenn das Wort auf „arschsch“ endet, entferne die letzten drei Zeichen „sch“:
  `"arschsch" → "arsch"`

### 7. Ersetzen des Präfixes „aus“:
- **Regel 6.1:** Wenn das Wort mit „aus“ beginnt, ersetze „aus“ durch „arsch“:
  `"aus" → "arsch"`

---

## Zusammenfassung der Grammatik:
1. Ein Wort wird als eine Sequenz von Silben verarbeitet, die durch Bindestriche getrennt sein können.
2. Silben, die den Buchstaben „a“ enthalten, werden nach verschiedenen Regeln in „arsch“ umgewandelt, abhängig von ihrer Länge, Position und dem Vorhandensein von bestimmten Buchstabenkombinationen.
3. Wörter können Sonderzeichen am Ende haben, die vorübergehend entfernt und nach der Modifikation wieder hinzugefügt werden.
4. Wörter, die im „arschterbuch“ vorkommen, werden vollständig durch bekannte „Arsch-Wörter“ ersetzt, wobei Großschreibung beachtet wird.
5. Spezifische Endungen wie „arschh“, „arschch“ und „arschsch“ werden korrigiert, indem überflüssige Zeichen entfernt werden.
6. Das Präfix „aus“ wird durch „arsch“ ersetzt, um dem Transformationsthema treu zu bleiben.

---

## Endzustand:
Das Endergebnis ist ein modifiziertes Wort, das den oben definierten Regeln zur „a“->„arsch“-Transformation entspricht und die korrekten Groß-/Kleinschreibung und Sonderzeichen beibehält.

