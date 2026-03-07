# Running local, that is, downloading the model. Jeg valgte ikke at gøre dette, da jeg havde håbet at kunne se vægtene, men det var besværligt med en tensor-fil.
# Faktisk droppede jeg API'en igen  fordi det ikke virkede optimalt (og meget langsomt) og jeg tænkte, at klassificeringen af nyhederne indtil videre virker fint bare at have gjort i udviklingsmiljø.
# import os
# from huggingface_hub import InferenceClient
# client = InferenceClient(api_key=os.getenv("HF_TOKEN"))
# response = client.zero_shot_classification(
#     model="facebook/bart-large-mnli",
#     text= "Krigen i mellemøsten kan få betydning for olieprisen",
#     candidate_labels = ["energibranchen", "medicinalindustrien", "detailhandel"]
# )
# print(response)
################
# from transformers import pipeline
# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# # lav et eksempel på brug af den her classifier, hvor vi klassificerer en nyhedstekst i forhold til tre mulige kategorier: "energibranchen", "medicinalindustrien", "detailhandel"
# text = "Krigen i mellemøsten kan få betydning for olieprisen"
# candidate_labels = ["energibranchen", "medicinalindustrien", "detailhandel"]
# result = classifier(text, candidate_labels)
# print(result)
# jeg endte med at droppe text klassificering, fordi den ikke kunne ræssonere (fx ikke forstå sammenhæng "yields drops" nyhed og "Ørsted affected by interest rates")
# har både brugt modellen "facebook/bart-large-mnli" og "sentence-transformers/all-MiniLM-L6-v2" til at teste forskellige tilgange

# et datasæt med finansielle nyheder
from datasets import load_dataset
ds = load_dataset("danidanou/Reuters_Financial_News", split="train[-100:]")
import os
from openai import OpenAI
import pandas as pd
from stocks.models import aktier

#start a dataframe with one column for each aktie in the aktier model?

aktierne = aktier.objects.all()
selskaber = ["DSV A/S", "Pandora A/S", "Vestas Wind Systems A/S", "Ørsted A/S", "Novo Nordisk B A/S"]
aktierne = aktierne.filter(selskab__in=selskaber)




# en funktion til at definere relevansen af nyheder for ovenstående udvalgte aktier.
def vurder_nyheder():
    df = pd.DataFrame()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY2"))
    for i, data in enumerate(ds):
        df.loc[i, "summary"] = data["Summary"]
        for obj in aktierne:  # skip the "summary" column
            col = obj.selskab
            prompt = f"""{col} påvirkes generelt af: {obj.paavirkningsfaktorer}. Påvirker denne nyhed virksomheden {data["Summary"]}? Inddrag gerne egne antagelse. Angiv KUN et tal mellem 0 og 5, hvor 0 betyder ingen påvirkning og 5 betyder stor påvirkning."""
            response = client.chat.completions.create(
                model="gpt-5.2-chat-latest",
                messages=[
                    {"role": "system", "content": "Du skal vurdere, hvorvidt en nyhed har relevans for en virksomhed"},
                    {"role": "user", "content": prompt}
                ]
            )
            df.loc[i, col] = response.choices[0].message.content
    df.to_excel("aktie_nyheder.xlsx", index=False)
    return df


#funktion til at opssummere de fem mest relevante nyheder
def opsummer_relevante_nyheder():
    df_copy = pd.read_excel("aktie_nyheder.xlsx")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY2"))
    summaries_df = pd.DataFrame()
    for selskab in selskaber:
        top_5 = df_copy[selskab].astype(float).nlargest(5)
        #gør de fem rækker i "summary" kolonnen klar til at blive sendt med som prompt til openai, så vi kan få en opsummering af de fem mest relevante nyheder for hver virksomheder
        summaries = []
        for index in top_5.index:
            summaries.append(df_copy.loc[index, "summary"])
        prompt = f"""Du skal lave en kort opsummering af de fem mest relevante nyheder for virksomheden {selskab}. Her er de fem nyheder: {summaries}. Lav en kort opsummering på ca. tre linjer."""
        response = client.chat.completions.create(
            model="gpt-5.2-chat-latest",
            messages=[
                {"role": "system", "content": f"Du skal lave en kort opsummering på ca. 100 tegn af de fem mest relevante nyheder for en virksomhed. Det må gerne være prioriteret, hvis du kan. Du kan eventuelt opremse nyheder ekstremt kort med komma imellem. Nyhederne er: {summaries}"},
                {"role": "user", "content": prompt}
            ]
        )
        summaries_df[selskab] = [response.choices[0].message.content]
        summaries_df.to_excel("aktie_nyheder_summaries.xlsx", index=False)
    return summaries_df