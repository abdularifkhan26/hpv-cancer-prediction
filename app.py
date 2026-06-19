from shiny import App, ui, render, reactive
import pandas as pd
import joblib
import os
import numpy as np


# Load trained model
model = joblib.load("hpv_paper.pkl")
#scaler = joblib.load("scaler.pkl")
training_genes = joblib.load("training_genes.pkl")


# Gene list used for prediction
genes = [
    "ADAMTS19", "DLK1", "ADH1B", "DPP6", "ZCCHC12",
    "PEG3", "HSPB7", "NCAM1", "NMU", "FOXN1",
    "LHX2", "PADI3", "ZIC2", "FOXA1", "NLRP7",
    "ABCA12", "KREMEN2", "ANGPTL1", "TMEM40", "FAM83C"
]

genes_upper = [g.upper() for g in genes]


# Create sample file if not present
os.makedirs("www", exist_ok=True)
sample_path = os.path.join("www", "sample_input.csv")

if not os.path.exists(sample_path):
    sample_data = np.random.rand(5, len(genes_upper))
    df_sample = pd.DataFrame(sample_data, columns=genes_upper)
    df_sample.insert(0, "Sample", [f"S{i+1}" for i in range(5)])
    df_sample.to_csv(sample_path, index=False)


# ---------------- UI ----------------
app_ui = ui.page_fluid(

    ui.tags.head(

        ui.tags.link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css"
        ),

        ui.tags.style("""
        body {
            background: #f4f6f9;
            font-family: Arial, sans-serif;
            color: #222;
        }

        .header-panel {
            background: white;
            padding: 30px;
            border-radius: 18px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }

        .header-title {
            font-size: 34px;
            font-weight: bold;
            color: #1f2d3d;
        }

        .content-panel {
            background: white;
            border-radius: 18px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        }

        .panel-title {
            font-size: 22px;
            font-weight: 600;
            margin-bottom: 15px;
            color: #1f2d3d;
        }

        .gene-list {
            columns: 2;
            font-size: 13px;
            color: #333;
        }

        .result-positive {
            background: #d63031;
            color: white;
            padding: 22px;
            border-radius: 14px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .result-negative {
            background: #00b894;
            color: white;
            padding: 22px;
            border-radius: 14px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .banner-image {
            width: 100%;
            max-width: 650px;
            display: block;
            margin: auto;
            border-radius: 14px;
        }

        .btn-primary {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
        }

        .info-box {
            background: #f8f9fb;
            border-radius: 14px;
            padding: 18px;
            margin-top: 15px;
            border: 1px solid #dfe6e9;
        }
        """)
    ),

    # Header
    ui.div(
        {"class": "header-panel"},
        ui.h1(
            "HPV Cancer Prediction Tool",
            {"class": "header-title"}
        ),
        ui.p("Machine learning-based classification of HPV status using transcriptomic biomarkers")
    ),

    # Tabs
    ui.navset_tab(

        ui.nav_panel(
            "Home",

            ui.layout_sidebar(

                # Sidebar
                ui.sidebar(

                    ui.div(
                        {"class": "content-panel"},

                        ui.div(
                            ui.HTML('<i class="bi bi-upload"></i> Prediction Mode'),
                            {"class": "panel-title"}
                        ),

                        # Prediction Mode
                        ui.input_radio_buttons(
                            "prediction_mode",
                            "Choose Prediction Type",
                            {
                                "manual": "Manual Prediction",
                                "batch": "Batch Prediction"
                            },
                            selected="batch"
                        ),

                        ui.hr(),

                        # Manual Input Section
                        ui.panel_conditional(
                            "input.prediction_mode == 'manual'",

                            ui.h5("Enter 20 Gene Expression Values"),

                            *[
                                ui.input_numeric(
                                    g,
                                    g,
                                    value=0.5
                                )
                                for g in genes_upper
                            ]
                        ),

                        # Batch Upload Section
                        ui.panel_conditional(
                            "input.prediction_mode == 'batch'",

                            ui.input_file("file", "Upload CSV File"),

                            ui.br(),

                            ui.markdown("""
                            **Instructions**
                            - Upload a CSV file
                            - Gene names must match
                            - Each row = one sample
                            - Avoid missing values
                            """),

                            ui.br(),

                            ui.download_button("download_sample", "Download Sample File")
                        ),

                        ui.br(),

                        ui.input_action_button(
                            "predict",
                            ui.HTML('<i class="bi bi-play-fill"></i> Run Prediction'),
                            class_="btn-primary"
                        ),

                        ui.br(), ui.br(),

                        ui.output_text("status"),

                        ui.hr(),

                        ui.h5("Genes Used"),
                        ui.output_ui("gene_list")
                    )
                ),

                # Main content
                ui.div(

                    ui.div(
                        {"class": "content-panel"},

                        ui.img(src="cancer_banner.jpeg", class_="banner-image"),

                        ui.br(),

                        ui.h3("Cancer Insight Visualization"),

                        ui.p("This application classifies HPV-associated samples using transcriptomic biomarkers selected by LASSO regression."),

                        ui.div(
                            {"class": "info-box"},
                            ui.h5("Model Information"),
                            ui.tags.ul(
                                ui.tags.li("Algorithm: LASSO Logistic Regression"),
                                ui.tags.li("Input: Gene Expression Matrix"),
                                ui.tags.li("Output: HPV Positive / HPV Negative"),
                                ui.tags.li("Features: 20 Biomarker Genes")
                            )
                        )
                    ),

                    ui.div(
                        {"class": "content-panel"},

                        ui.h3(ui.HTML('<i class="bi bi-clipboard-data"></i> Prediction Results')),

                        ui.output_table("result"),

                        ui.br(),

                        ui.output_ui("prediction_summary")
                    )
                )
            )
        ),

        # About tab
        ui.nav_panel(
            "About Model",
            ui.div(
                {"class": "content-panel"},
                ui.h2("About This System"),
                ui.p("""
                This HPV prediction platform uses machine learning
                to analyze gene expression data and classify samples
                into HPV Positive or HPV Negative categories.
                """),
                ui.h4("Packages and Dependencies"),
                ui.tags.ul(
                    ui.tags.li("Python Shiny"),
                    ui.tags.li("Scikit-learn"),
                    ui.tags.li("Pandas"),
                    ui.tags.li("LASSO Logistic Regression")
                ),
                ui.h4("Developers"),

                    ui.tags.ul(
                    ui.tags.li("Ms.Vaishnavi Anilkumar Shirpurkar"),
                    ui.tags.li("Dr. Abdul Arif Khan(ICMR-National Institute of Translational Virology and AIDS Research)"),
                   
                   
                )
            )
        )
    )
)


# ---------------- Server ----------------
training_genes = joblib.load("training_genes.pkl")
def server(input, output, session):

    # Download sample file
    @render.download(filename="sample_input.csv")
    def download_sample():
        with open(sample_path, "rb") as f:
            yield f.read()

    # Prediction logic
    @reactive.event(input.predict)
    def run_prediction():

        mode = input.prediction_mode()

        try:

            # ==============================
            # MANUAL PREDICTION
            # ==============================
            if mode == "manual":

                values = []

                for g in genes_upper:

                    val = getattr(input, g)()

                    if val is None:
                        val = 0

                    values.append(val)

                df_manual = pd.DataFrame(
                    [values],
                    columns=genes_upper
                )
                df_manual = df_manual.reindex(columns=training_genes, fill_value=0)
                predictions = model.predict(df_manual)
                probabilities = model.predict_proba(df_manual)[:, 1]
                                                
                
                results = pd.DataFrame({
                    "Sample": ["Manual_Input"],
                    "Prediction": predictions,
                    "Probability (%)": (probabilities * 100).round(2)
                })

                results["Prediction"] = results["Prediction"].map({
                    1: "HPV Positive",
                    0: "HPV Negative"
                })

                return results

            # BATCH PREDICTION
            # ==============================
            uploaded_file = input.file()

            if uploaded_file is None:
                return None

            df = pd.read_csv(
                uploaded_file[0]["datapath"],
                sep=None,
                engine="python",
                comment="#"
            )

            if df.empty:
                raise ValueError("Uploaded dataset is empty.")

            if df.columns[0].upper() not in genes_upper:
                df = pd.read_csv(
                    uploaded_file[0]["datapath"],
                    sep=None,
                    engine="python",
                    index_col=0
                )

            df.columns = df.columns.str.upper().str.strip()

            if not set(genes_upper).issubset(df.columns):
                df = df.T
                df.columns = df.columns.str.upper().str.strip()

            missing_genes = [g for g in genes_upper if g not in df.columns]

            
            

            

           
            
            df_clean = df.reindex(columns=training_genes, fill_value=0)

            predictions = model.predict(df_clean)
            probabilities = model.predict_proba(df_clean)[:, 1]

            results = pd.DataFrame({
                "Sample": df_clean.index,
                "Prediction": predictions,
                "Probability (%)": (probabilities * 100).round(2)
            })

            results["Prediction"] = results["Prediction"].map({
                1: "HPV Positive",
                0: "HPV Negative"
            })

            return results

        except Exception as error:
            return pd.DataFrame({"Error": [str(error)]})

    @output
    @render.text
    def status():

        mode = input.prediction_mode()

        if mode == "manual":
            return "Manual prediction mode selected."

        return (
            "No file uploaded."
            if input.file() is None
            else "Dataset uploaded successfully."
        )

    @output
    @render.table
    def result():
        results = run_prediction()

        if results is None:
            return pd.DataFrame({
                "Message": ["Upload dataset and run prediction."]
            })

        return results

    @output
    @render.ui
    def prediction_summary():

        results = run_prediction()

        if results is None or "Prediction" not in results.columns:
            return ui.div("No prediction available.")

        prediction = results["Prediction"].iloc[0]
        probability = results["Probability (%)"].iloc[0]

        if prediction == "HPV Positive":
            return ui.div(
                {"class": "result-positive"},
                ui.HTML(
                    f"<img src='positive.png' width='70'><br><br>"
                    f"HPV POSITIVE<br><br>"
                    f"Confidence Score: {probability}%"
                )
            )

        return ui.div(
            {"class": "result-negative"},
            ui.HTML(
                f"<img src='negative.png' width='70'><br><br>"
                f"HPV NEGATIVE<br><br>"
                f"Confidence Score: {probability}%"
            )
        )

    @output
    @render.ui
    def gene_list():
        return ui.div(
            {"class": "gene-list"},
            *[ui.div(g) for g in genes_upper]
        )


# Run app
app = App(
    app_ui,
    server,
    static_assets=os.path.join(os.path.dirname(__file__), "www")
)
# Note:This code was refined and reviewed with the assistance of an AI-based Large Language Model (LLM).
