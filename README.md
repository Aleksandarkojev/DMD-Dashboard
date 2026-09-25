# Dashboard – template

En enkel Streamlit-dashboard som visar data från MySQL, via CSV-filer.

---

## Kom igång

**1. Forka det här repot** till ditt eget GitHub-konto (knappen **Fork** uppe till höger).

**2. Klona ditt fork till datorn.** I VS Code: `Ctrl+Shift+P` → *Git: Clone* → klistra in adressen till **ditt** fork.

**3. Installera det som behövs.** Öppna terminalen i VS Code och kör:

```bash
pip install -r requirements.txt
```

**4. Starta appen:**

```bash
streamlit run app.py
```

Sidan öppnas i webbläsaren. Den uppdateras automatiskt varje gång du sparar `app.py`.

---

## Lägg in din egen data

**1. Kör din SQL-fråga** i MySQL Workbench.

**2. Exportera resultatet som CSV.** Klicka på exportikonen ovanför resultatgriden och spara filen i mappen `data/`.

**3. Lägg till en analys i `app.py`.** Kopiera mallen längst ner i filen och byt ut filnamn och kolumnnamn:

```python
st.header("Din rubrik")
st.write("En mening om vad analysen visar.")

df = las("din_fil.csv")

st.dataframe(df, hide_index=True)
st.bar_chart(df, x="kolumn_med_kategorier", y="kolumn_med_siffror")
```

**4. Spara.** Sidan uppdateras direkt.

---

## De kommandon du behöver

| Kommando | Gör |
|---|---|
| `st.title("...")` | Stor rubrik |
| `st.header("...")` | Underrubrik |
| `st.write("...")` | Vanlig text |
| `st.dataframe(df)` | Visar en tabell |
| `st.bar_chart(df, x=..., y=...)` | Stapeldiagram |
| `st.line_chart(df, x=..., y=...)` | Linjediagram — bra för utveckling över tid |
| `st.metric("Rubrik", värde)` | En stor siffra |
| `st.divider()` | En linje mellan avsnitten |
| `st.columns(2)` | Delar upp sidan i kolumner |

---

## Välj rätt diagram

Du kan hitta inspiration om fler datavisualiseringar här https://streamlit.io/gallery

| Frågan du svarar på | Diagram |
|---|---|
| Hur fördelar sig något på kategorier? | `st.bar_chart` |
| Hur utvecklas något över tid? | `st.line_chart` |
| En enskild viktig siffra | `st.metric` |
| Detaljer som ska gå att läsa av | `st.dataframe` |

---

## Om något går fel

**`ModuleNotFoundError: No module named 'streamlit'`**
Du har inte installerat paketen. Kör `pip install -r requirements.txt`.

**`Hittar inte filen: data/...`**
Filnamnet stämmer inte, eller så ligger CSV-filen någon annanstans än i `data/`.

**Diagrammet är tomt**
Kolumnnamnen i `x=` och `y=` måste stämma exakt med rubrikerna i CSV-filen. Kolla med `st.dataframe(df)` först — då ser du vad kolumnerna heter.

**Åäö ser konstiga ut**
Exportera CSV:n som UTF-8 från Workbench.

---

## Spara ditt arbete

```bash
git add .
git commit -m "La till min analys"
git push
```
