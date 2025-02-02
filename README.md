## Overview
Notre outil réalise une analyse de sentiment à partir des articles de journaux traitant d'Enedis. Il convertit une revue de presse au format PDF en un tableau de bord exploitable. De plus, il permet d'exporter les données au format .xlsx conforme aux normes établies par Enedis.

![image](https://github.com/user-attachments/assets/842fe4dc-ed07-42a5-a441-b158fa6d6cdf)

Vidéo de démonstration : [Voir la démo](https://screen.studio/share/b5VosBEt)

## Lancement de l'application
Version requise : Python 3.12.3
```bash
python -m venv venv
pip install -r requirements.txt
cd prompt
```
Ajoutez soit le fichier PDF "articles.pdf", soit le fichier CSV "Data.xlsx", puis exécutez l'une des commandes suivantes :
```bash
python get_sentiment_csv.py
python get_sentiment_pdf.py
```

### Visualisation des données

Github du front-end : https://github.com/theocerdan/ae42front
Le front-end de visualisation se lance avec les commandes suivantes :
```bash
npm install
npm run build
```

## Architecture
![schema](https://github.com/user-attachments/assets/b0091adb-b780-4ed4-a933-becaec880419)
Amazon Bedrock intègre une configuration Guardrails qui minimise les hallucinations et garantit que seules les données des articles sont prises en compte.

## Benchmark
Nous avons testé plusieurs modèles :
- `mistral.mistral-large-2407-v1:0`
- `us.amazon.nova-pro-v1:0`
- `us.amazon.nova-lite-v1:0`
- `anthropic.claude-3-5-sonnet-20240620-v1:0`

Parmi eux, nous avons sélectionné :
- **Nova-Pro** pour l'analyse de sentiment
- **Nova-Lite** pour le traitement des articles de la revue de presse

Un pastebin contenant l'ensemble des prompts benchmark utilisés lors du hackathon est disponible : https://pastebin.com/A8r9BAtL

Le Quadratic Weighted Kappa (QWK) est une métrique statistique évaluant l’accord entre deux évaluateurs, souvent utilisée dans les classifications ordinales. Il pénalise davantage les erreurs éloignées de la vérité. Le score varie de -1 (désaccord total) à 1 (accord parfait), avec 0 représentant un accord aléatoire.

**Score QWK obtenu : 0.651**
(-1 = pire, 1 = parfait, 0 = aléatoire)

![image](https://github.com/user-attachments/assets/e92b2fdc-8b2f-4ece-9811-f9f2b23c0875)

Le taux d'hallucination mesuré lors de nos tests est de **0.7%**.

## Prochaines étapes
Mise en place des requêtes batch pour Amazon Bedrock.
