import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuration de la page - plein écran avec thème sombre
st.set_page_config(
    page_title="Analyse de Questionnaire",
    layout="wide",
    initial_sidebar_state="collapsed",
    
)

GRAPH_SIZE=(4.5,4.5)

# CSS pour thème sombre et mise en page améliorée
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #f5f5f5;
}
.stApp {
    max-width: 1200px !important;
    margin: 0 auto !important;
}

/* Modifier la taille des conteneurs de graphiques */
.chart-container {
    padding: 15px !important;  /* Réduit de 30px à 15px */
    margin: 15px 0 !important;  /* Réduit de 40px à 15px */
}

/* Normaliser la taille des graphiques */
.element-container:has(.js-plotly-plot),
.element-container:has(.matplotlib-container) {
    max-width: 450px !important;
    height: auto !important;
    margin: auto !important;
}

.stApp {
    background: linear-gradient(135deg, #141821 0%, #1e2026 100%);
    animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

h1, h2, h3, h4 {
    color: #ffffff;
    font-weight: 800;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 6px rgba(0,0,0,0.6);
    margin-top: 0;
    padding-bottom: 12px;
    border-bottom: 2px solid #00FFA1;
}

@keyframes slideDown {
  from { transform: translateY(-15px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 2px solid #00D4FF;
    justify-content: center;
}
.stTabs [data-baseweb="tab"] {
    background-color: #2a2f3c;
    color: #ffffff;
    padding: 14px 28px;
    border-radius: 18px 18px 0 0;
    transition: all 0.3s ease;
    font-weight: 600;
    font-size: 17px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(to right, #00D4FF, #00FFA1);
    color: #1e2026;
    font-weight: 800;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

div.stButton > button:first-child {
    background: linear-gradient(135deg, #00FFA1, #00D4FF);
    color: #1e2026;
    font-weight: 800;
    padding: 16px 30px;
    border: none;
    border-radius: 14px;
    font-size: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    transition: all 0.3s ease;
}
div.stButton > button:first-child:hover {
    transform: scale(1.03);
    box-shadow: 0 10px 28px rgba(0,0,0,0.5);
}

div[data-testid="stMetricValue"] {
    font-size: 40px;
    color: #ffffff;
    font-weight: 900;
}
div[data-testid="stMetricLabel"] {
    font-size: 18px;
    color: #aaaaaa;
}

.chart-container {
    background: linear-gradient(to top left, #2f3545, #3c4254);
    padding: 30px;
    border-radius: 20px;
    margin: 40px 0;
    box-shadow: 0px 8px 32px rgba(0,0,0,0.5);
    animation: fadeIn 1s ease-in-out;
}

.chart-container h3 {
    margin-top: 0;
    color: #00FFA1;
    font-weight: 900;
    margin-bottom: 25px;
    font-size: 24px;
    text-align: center;
    border-bottom: 2px dashed #00D4FF;
    padding-bottom: 12px;
}

.dataframe {
    background-color: #2b303a;
    color: #f5f5f5;
    border-radius: 12px;
    padding: 18px;
    font-size: 15px;
    border: 1px solid #444;
    box-shadow: inset 0 0 12px rgba(0,0,0,0.3);
    margin-top: 30px;
}

/* Ajustement pour le camembert et tableau */
.element-container:has(.js-plotly-plot),
.element-container:has(.matplotlib-container) {
    max-width: 600px;
    margin: auto;
}

text {
    font-size: 16px !important;
    font-weight: bold;
}

table {
    font-size: 15px;
    border-collapse: separate;
    border-spacing: 0 10px;
    width: 100%;
}
thead th {
    color: #00FFA1;
    font-size: 16px;
    border-bottom: 2px solid #00D4FF;
}
tbody td {
    padding: 10px;
    background-color: #2a2f3c;
    border-radius: 8px;
}

footer {
    visibility: hidden;
}
[data-testid="stVerticalBlock"] h4 {
    font-size: 18px;
    margin-top: 10px;
    padding-bottom: 8px;
    border-bottom: 1px solid #00D4FF;
    color: #00FFA1;
}

/* Animation pour les graphiques dans la vue d'ensemble */
.element-container:has(.js-plotly-plot),
.element-container:has(.matplotlib-container) {
    transition: transform 0.3s ease;
}

.element-container:has(.js-plotly-plot):hover,
.element-container:has(.matplotlib-container):hover {
    transform: scale(1.03);
}
</style>
""", unsafe_allow_html=True)

# Charger les données
@st.cache_data
def load_data():
    try:
        df = pd.read_excel('quu_cleaned(2).xlsx')

        # Méthode améliorée pour supprimer les colonnes timestamp
        # 1. Supprimer les colonnes de type datetime explicite
        datetime_columns = df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns

        # 2. Identifier les colonnes qui contiennent probablement des timestamps par leur nom
        timestamp_keywords = ['time', 'date', 'timestamp', 'start', 'end', 'submit', 'created', 'modified']
        potential_timestamp_cols = [col for col in df.columns if any(keyword in str(col).lower() for keyword in timestamp_keywords)]

        # 3. Combiner toutes les colonnes à supprimer
        columns_to_drop = list(datetime_columns) + [col for col in potential_timestamp_cols if col not in datetime_columns]

        if columns_to_drop:
            st.sidebar.write(f"Colonnes timestamp supprimées: {', '.join(columns_to_drop)}")
            df = df.drop(columns=columns_to_drop)

        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return pd.DataFrame()

original_df = load_data()
short_labels = {
    "1. Quel est votre âge ?": "Âge",
    "2. Quel est votre genre ?": "Genre",
    "3. Quelle est votre situation actuelle ?": "Situation",
    "4. Quel est votre revenu mensuel net ?": "Revenu",
    "5. À quelle fréquence utilisez-vous les réseaux sociaux ? (Par jour)": "Fréquence RS",
    "6. Quelles plateformes utilisez-vous le plus souvent ? ": "Plateformes utilisées",
    "7. Quels types de contenus vous attirent le plus sur ces plateformes ? (max 3 choix)": "Contenus attirants",
    "8.Quels types de produits ou services achetez-vous suite à du contenu vu sur les réseaux ?": "Produits influencés",
    "9 . Avez-vous déjà acheté un produit après l’avoir vu sur un réseau social ?": "Achat après RS",
    "10 . Si oui, qu’est-ce qui vous a le plus influencé ? (max 2 choix)": "Influence RS",
    "11. Pourquoi êtes-vous influencé par ce type de contenus ? (max 3 choix)": "Raisons d'influence",
    "12.  Diriez-vous que les réseaux sociaux influencent régulièrement vos décisions d’achat ?": "Influence achat",
}

reverse_labels = {v: k for k, v in short_labels.items()}



# Configuration des filtres
with st.sidebar:
    st.markdown('<h3 style="color: white;">Filtres</h3>', unsafe_allow_html=True)

    # Initialiser dataframe filtré
    filtered_df = original_df.copy()

    # Filtres pour colonnes catégorielles pertinentes
    if not original_df.empty:
        filter_columns = original_df.select_dtypes(include=['object']).columns
        filter_columns = [col for col in filter_columns if original_df[col].nunique() < 10]

        for col in filter_columns:
            options = ['Tous'] + sorted(list(original_df[col].dropna().unique()))
            selected = st.selectbox(f'{col}:', options)

            if selected != 'Tous':
                filtered_df = filtered_df[filtered_df[col] == selected]

        # Métrique de données filtrées
        st.metric("Réponses", f"{len(filtered_df)}/{len(original_df)}")

        # Téléchargement des données filtrées
        st.markdown('<h3 style="color: white;">Exporter</h3>', unsafe_allow_html=True)
        if not filtered_df.empty:
            csv = filtered_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Télécharger (CSV)",
                data=csv,
                file_name="donnees_filtrees.csv",
                mime="text/csv"
            )

# Fonction pour séparer les choix multiples
def split_multiple_choices(df, column):
    if column in df.columns:
        return df[column].str.split(';').explode().str.strip()
    return pd.Series()

# Configuration des styles pour graphiques en thème sombre - TAILLE RÉDUITE
plt.style.use('dark_background')
colors = [
    '#3498db',  # Bleu clair
    '#e74c3c',  # Rouge
    '#2ecc71',  # Vert
    '#f39c12',  # Orange
    '#9b59b6',  # Violet
    '#1abc9c',  # Turquoise
    '#34495e',  # Bleu foncé
    '#95a5a6'   # Gris
]
plt.rcParams.update({
    'figure.figsize': (GRAPH_SIZE[0] * 1.3, GRAPH_SIZE[1]),
    'figure.autolayout': False,  # Désactiver autolayout pour contrôler manuellement
    'figure.subplot.bottom': 0.2,  # Laisser plus d'espace en bas
    'figure.subplot.right': 0.75,  # Laisser plus d'espace à droite pour les légendes# Taille standardisée pour tous les graphiques
    'figure.dpi': 100,
    'figure.facecolor': '#1a1a1a',
    'axes.facecolor': '#1a1a1a',
    'axes.edgecolor': '#444444',
    'axes.labelcolor': 'white',
    'axes.titlecolor': 'white',
    'axes.grid': False,
    'axes.labelsize': 9,
    'axes.titlesize': 11,
    'xtick.color': '#cccccc',
    'ytick.color': '#cccccc',
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'legend.fontsize': 8,
    'text.color': 'white',
    'font.family': 'sans-serif'
})

# Titre de l'application avec emoji
st.markdown("# 📊 Dashboard: Analyse de Questionnaire")

# Organisation en onglets - avec des icônes
tab1, tab2, tab3, tab4 = st.tabs(["📈 Analyse", "🔄 Croisements", "📋 Données", "🔍 Vue d'ensemble"])


# Onglet 1: Analyse graphique
with tab1:
    if not filtered_df.empty:
        # Sélection de question et type de graphique en deux colonnes distinctes
        col1, col2 = st.columns([3, 1])
        with col1:
            question_display = st.selectbox(
                'Sélectionner une question:',
                options=[short_labels.get(col, col) for col in filtered_df.columns]
            ) 
            question = reverse_labels.get(question_display, question_display)       
        with col2:
            chart_type = st.radio(
                "Type:",
                ["Camembert", "Barres"],
                horizontal=True
            )
        if question:    
            # Utiliser des colonnes pour une mise en page plus compacte
            col_left, col_right = st.columns([3, 2])

            with col_left:
                # Conteneur pour le graphique
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)

                # Analyser la colonne sélectionnée
                if filtered_df[question].dtype == 'object' and filtered_df[question].str.contains(';', na=False).any():
                    # Traitement pour choix multiples
                    choices = split_multiple_choices(filtered_df, question)
                    if not choices.empty:
                        counts = choices.value_counts()

                        # Créer graphique avec taille réduite
                        if chart_type == "Barres":
                            fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                            bars = sns.barplot(x=counts.index, y=counts.values, palette=colors, ax=ax)
                            plt.xlabel('')
                            plt.ylabel('')
                            plt.xticks(rotation=30, ha='right', color='white', fontsize=8)

                            # Labels sur les barres - plus petits
                            for bar in bars.patches:
                                bars.annotate(f"{int(bar.get_height())}", 
                                    (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='white')
                            
                            # Style épuré
                            ax.spines['top'].set_visible(False)
                            ax.spines['right'].set_visible(False)
                            plt.tight_layout(rect=[0, 0, 0.85, 1])
                        else:  # Camembert
                            fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                            wedges, texts, autotexts = ax.pie(
                                counts.values, 
                                labels=None,  # Enlever les labels du graphique
                                autopct='%1.1f%%',
                                textprops={'fontsize': 8, 'color': 'white'},
                                colors=colors,
                                explode=[0.01] * len(counts),  # Réduire l'écart
                                shadow=False
                            )
                            plt.setp(autotexts, weight="bold", color="white", fontsize=9)
                            # Ajouter une légende à côté
                            ax.legend(wedges, counts.index, 
                                loc="center left",
                                bbox_to_anchor=(1, 0.5),
                                fontsize=7)
                            ax.set_aspect('equal')

                        st.pyplot(fig)
                else:
                    # Traitement pour choix unique
                    counts = filtered_df[question].value_counts()

                    if chart_type == "Barres":
                        fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                        bars = sns.barplot(x=counts.index, y=counts.values, palette=colors, ax=ax)
                        plt.xlabel('')
                        plt.ylabel('')
                        plt.xticks(rotation=30, ha='right', color='white', fontsize=8)

                        # Labels sur les barres - plus petits
                        for bar in bars.patches:
                            bars.annotate(f"{int(bar.get_height())}", 
                                (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                                ha='center', va='bottom', fontsize=9, fontweight='bold', color='white')

                        # Style épuré
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        plt.tight_layout(rect=[0, 0, 0.85, 1])

                    else:  # Camembert
                        fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                        wedges, texts, autotexts = ax.pie(
                            counts.values, 
                            labels=None,  # Enlever les labels du graphique
                            autopct='%1.1f%%',
                            textprops={'fontsize': 10, 'color': 'white'},
                            colors=colors,
                            explode=[0.01] * len(counts),  # Réduire l'écart
                            shadow=False
                        )
                        plt.setp(autotexts, weight="bold", color="white", fontsize=9)
                        # Ajouter légende à côté
                        ax.legend(wedges, counts.index, 
                            loc="center left", 
                            bbox_to_anchor=(1, 0.5),
                            fontsize=7)
                        ax.set_aspect('equal')

                    st.pyplot(fig)

                st.markdown('</div>', unsafe_allow_html=True)

            with col_right:
                # Tableau de données
                if filtered_df[question].dtype == 'object' and filtered_df[question].str.contains(';', na=False).any():
                    choices = split_multiple_choices(filtered_df, question)
                    if not choices.empty:
                        counts = choices.value_counts()
                        table_data = pd.DataFrame({
                            'Réponse': counts.index,
                            'Nombre': counts.values,
                            '%': np.round(counts.values / counts.sum() * 100, 1)
                        })
                        st.dataframe(table_data, use_container_width=True, hide_index=True)
                else:
                    counts = filtered_df[question].value_counts()
                    table_data = pd.DataFrame({
                        'Réponse': counts.index,
                        'Nombre': counts.values,
                        '%': np.round(counts.values / counts.sum() * 100, 1)
                    })
                    st.dataframe(table_data, use_container_width=True, hide_index=True)
    else:
        st.warning("Aucune donnée disponible pour l'analyse.")

# Onglet 2: Croisements
with tab2:
    if not filtered_df.empty and len(filtered_df.columns) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            var_x_display = st.selectbox(
                'Variable 1 :',
                options=[short_labels.get(col, col) for col in filtered_df.columns],
                key='var_x'
            )
            var_x = reverse_labels.get(var_x_display, var_x_display)

        with col2:
            var_y_display = st.selectbox(
                'Variable 2 :',
                options=[short_labels.get(col, col) for col in filtered_df.columns],
                key='var_y',
                index=min(1, len(filtered_df.columns)-1)
            )
            var_y = reverse_labels.get(var_y_display, var_y_display)

        if var_x != var_y:
            # Créer un tableau croisé
            try:
                # Vérifier si les variables contiennent des choix multiples
                x_is_multi = filtered_df[var_x].dtype == 'object' and filtered_df[var_x].str.contains(';', na=False).any()
                y_is_multi = filtered_df[var_y].dtype == 'object' and filtered_df[var_y].str.contains(';', na=False).any()

                # Si l'une des variables est un choix multiple, on doit traiter différemment
                if x_is_multi or y_is_multi:
                    st.warning("Attention: Une ou les deux variables sélectionnées contiennent des choix multiples. Le croisement peut présenter des doublons.")

                # Créer un dataframe pour le croisement avec traitement des choix multiples
                if x_is_multi and not y_is_multi:
                    # Exploser les valeurs de var_x
                    exploded_df = filtered_df.copy()
                    exploded_df[var_x] = exploded_df[var_x].str.split(';')
                    exploded_df = exploded_df.explode(var_x).reset_index(drop=True)
                    exploded_df[var_x] = exploded_df[var_x].str.strip()
                    crosstab = pd.crosstab(exploded_df[var_x], exploded_df[var_y])

                elif not x_is_multi and y_is_multi:
                    # Exploser les valeurs de var_y
                    exploded_df = filtered_df.copy()
                    exploded_df[var_y] = exploded_df[var_y].str.split(';')
                    exploded_df = exploded_df.explode(var_y).reset_index(drop=True)
                    exploded_df[var_y] = exploded_df[var_y].str.strip()
                    crosstab = pd.crosstab(exploded_df[var_x], exploded_df[var_y])

                else:
                    # Les deux variables sont des choix multiples
                    # Ce cas est complexe et peut générer des doublons
                    # Une solution simple est de créer une combinaison unique pour chaque répondant
                    exploded_df = filtered_df.copy()

                    # Exploser d'abord var_x puis var_y
                    exploded_df[var_x] = exploded_df[var_x].str.split(';')
                    exploded_df = exploded_df.explode(var_x).reset_index(drop=True)
                    exploded_df[var_x] = exploded_df[var_x].str.strip()

                    exploded_df[var_y] = exploded_df[var_y].str.split(';')
                    exploded_df = exploded_df.explode(var_y).reset_index(drop=True)
                    exploded_df[var_y] = exploded_df[var_y].str.strip()

                    # Supprimer les doublons de combinaisons pour un même répondant
                    exploded_df = exploded_df.drop_duplicates([var_x, var_y])

                    crosstab = pd.crosstab(exploded_df[var_x], exploded_df[var_y])
                
                # Correction de la structure conditionnelle ici - suppression de 'else:'
                if not x_is_multi and not y_is_multi:
                    # Cas standard pour variables à choix unique
                    crosstab = pd.crosstab(filtered_df[var_x], filtered_df[var_y])

                # Afficher le tableau croisé
                st.dataframe(crosstab, use_container_width=True, height=200)

                # Conteneur pour les graphiques
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)

                # Utiliser des colonnes pour les graphiques côte à côte
                col1, col2 = st.columns(2)

                with col1:
                    # Heatmap - taille réduite
                    fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                    sns.heatmap(
                        crosstab, 
                        annot=True, 
                        cmap="Blues", 
                        linewidths=.5, 
                        fmt="d",
                        cbar_kws={"shrink": .8},
                        annot_kws={"size": 10, "weight": "bold", "color": "white"}
                    )
                    ax.set_xlabel("")  # Supprime le titre de l'axe X
                    ax.set_ylabel("")  # Supprime le titre de l'axe Y 
                    plt.tight_layout(rect=[0.05, 0.05, 0.95, 0.95])
                    st.pyplot(fig)
                    

                with col2:
                    # Barres empilées - taille réduite avec légende simplifiée
                    fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                    crosstab_percent = crosstab.div(crosstab.sum(axis=1), axis=0)

                    # Limiter le nombre de catégories affichées dans la légende
                    max_categories = 10  # Nombre maximal de catégories à afficher
                    if crosstab_percent.shape[1] > max_categories:
                        # Garder les max_categories les plus importantes et regrouper le reste
                        cols_to_show = crosstab_percent.sum().nlargest(max_categories).index
                        crosstab_percent_limited = crosstab_percent[cols_to_show]
                        crosstab_percent_limited.plot(
                            kind='bar', 
                            stacked=True, 
                            ax=ax,
                            color=colors[:max_categories]
                        )
                        st.warning(f"Seules les {max_categories} catégories les plus fréquentes sont affichées pour améliorer la lisibilité.")
                    else:
                        # Afficher toutes les catégories
                        crosstab_percent.plot(
                            kind='bar', 
                            stacked=True, 
                            ax=ax,
                            color=colors
                        )

                    plt.xlabel('')
                    plt.ylabel('')

                    # Légende avec taille réduite et placée en dehors du graphique
                    plt.legend( 
                        bbox_to_anchor=(1.05, 0.5), 
                        loc='upper left', 
                        fontsize=6,  # Taille de police plus petite
                        title_fontsize=7,
                        ncol=1)

                    plt.xticks(rotation=30, ha='right', color='white', fontsize=8)

                    # Style amélioré
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    plt.grid(axis='y', alpha=0.3)
                    plt.tight_layout(rect=[0, 0, 0.85, 1])
                    plt.subplots_adjust(bottom=0.2)

                    st.pyplot(fig)

                st.markdown('</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Impossible de créer le croisement: {e}")
        else:
            st.warning("Veuillez sélectionner deux variables différentes.")
    else:  
        st.warning("Données insuffisantes pour effectuer un croisement.")

# Onglet 3: Aperçu des données brutes
with tab3:
    st.dataframe(filtered_df, use_container_width=True, height=400)

    # Statistiques descriptives uniquement pour les colonnes numériques
    numeric_df = filtered_df.select_dtypes(include=['int64', 'float64'])
    if not numeric_df.empty:
        st.subheader("Statistiques")
        st.dataframe(numeric_df.describe(), use_container_width=True)
        
# Dans l'onglet Vue d'ensemble
with tab4:
    st.markdown("## Vue d'ensemble de tous les graphiques")
    
    if not filtered_df.empty:
        # Option pour choisir le type de graphique global
        global_chart_type = st.radio(
            "Type de graphiques:",
            ["Camembert", "Barres"],
            horizontal=True,
            key='global_chart_type'
        )
        
        # Bouton pour générer tous les graphiques
        if st.button("Générer tous les graphiques"):
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.markdown(f"<h3>Vue d'ensemble des résultats</h3>", unsafe_allow_html=True)
            
            # Obtenir les colonnes qui sont des questions (exclure les colonnes techniques)
            question_columns = [col for col in filtered_df.columns if col in short_labels.keys()]
            
            # Créer un design multi-colonnes responsive
            num_cols = 2  # Nombre de colonnes pour l'affichage
            
            # Diviser les questions en groupes pour le multi-colonnes
            for i in range(0, len(question_columns), num_cols):
                cols = st.columns(num_cols)
                
                # Pour chaque colonne dans la rangée actuelle
                for j in range(num_cols):
                    col_idx = i + j
                    if col_idx < len(question_columns):
                        question = question_columns[col_idx]
                        question_display = short_labels.get(question, question)
                        
                        with cols[j]:
                            st.markdown(f"<h4>{question_display}</h4>", unsafe_allow_html=True)
                            
                            # Vérifier si la colonne contient des choix multiples
                            if filtered_df[question].dtype == 'object' and filtered_df[question].str.contains(';', na=False).any():
                                # Traitement pour choix multiples
                                choices = split_multiple_choices(filtered_df, question)
                                if not choices.empty:
                                    counts = choices.value_counts()
                                    
                                    # Créer graphique
                                    if global_chart_type == "Barres":
                                        fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                                        bars = sns.barplot(x=counts.index, y=counts.values, palette=colors, ax=ax)
                                        plt.xlabel('')
                                        plt.ylabel('')
                                        plt.xticks(rotation=45, ha='right', color='white', fontsize=7)
                                        
                                        # Labels sur les barres - plus petits
                                        for bar in bars.patches:
                                            bars.annotate(f"{int(bar.get_height())}", 
                                                (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                                                ha='center', va='bottom', fontsize=8, fontweight='bold', color='white')
                                        
                                        # Style épuré
                                        ax.spines['top'].set_visible(False)
                                        ax.spines['right'].set_visible(False)
                                        plt.tight_layout(rect=[0, 0, 0.85, 1])
                                    
                                    else:  # Camembert
                                        fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                                        wedges, texts, autotexts = ax.pie(
                                            counts.values, 
                                            labels=None,
                                            autopct='%1.1f%%',
                                            textprops={'fontsize': 8, 'color': 'white'},
                                            colors=colors,
                                            explode=[0.01] * len(counts),
                                            shadow=False,
                                            
                                        )
                                        plt.setp(autotexts, weight="bold", color="white", fontsize=8)
                                        ax.legend(wedges, counts.index, 
                                            loc="center left", 
                                            bbox_to_anchor=(1, 0.5), 
                                            fontsize=7,
                                            ncol=1)
                                        ax.set_aspect('equal')
                                    
                                    st.pyplot(fig)
                            else:
                                # Traitement pour choix unique
                                counts = filtered_df[question].value_counts()
                                
                                if global_chart_type == "Barres":
                                    fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                                    bars = sns.barplot(x=counts.index, y=counts.values, palette=colors, ax=ax)
                                    plt.xlabel('')
                                    plt.ylabel('')
                                    plt.xticks(rotation=45, ha='right', color='white', fontsize=7)
                                    
                                    # Labels sur les barres - plus petits
                                    for bar in bars.patches:
                                        bars.annotate(f"{int(bar.get_height())}", 
                                            (bar.get_x() + bar.get_width() / 2, bar.get_height()), 
                                            ha='center', va='bottom', fontsize=8, fontweight='bold', color='white')
                                    
                                    # Style épuré
                                    ax.spines['top'].set_visible(False)
                                    ax.spines['right'].set_visible(False)
                                    plt.tight_layout(rect=[0, 0, 0.85, 1])
                                
                                else:  # Camembert
                                    fig, ax = plt.subplots(figsize=GRAPH_SIZE)
                                    wedges, texts, autotexts = ax.pie(
                                        counts.values, 
                                        labels=None,
                                        autopct='%1.1f%%',
                                        textprops={'fontsize': 8, 'color': 'white'},
                                        colors=colors,
                                        explode=[0.01] * len(counts),
                                        shadow=False,
                                        
                                    )
                                    plt.setp(autotexts, weight="bold", color="white", fontsize=8)
                                    ax.legend(wedges, counts.index, 
                                        loc="center left", 
                                        bbox_to_anchor=(1, 0.5), 
                                        fontsize=7,
                                        ncol=1)
                                    ax.set_aspect('equal')
                                
                                st.pyplot(fig)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Ajouter un bouton pour télécharger tous les graphiques (futur développement)
            st.info("💡 Conseil: Utilisez la capture d'écran (Print Screen) pour enregistrer tous les graphiques.")
    else:
        st.warning("Aucune donnée disponible pour l'analyse.")

# Footer minimal - sans année/timestamp
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 0.8em;'>Dashboard d'analyse</p>", unsafe_allow_html=True)
