"""
Automation script to programmatically draw and export custom architecture diagrams 
using matplotlib's low-level drawing APIs.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_fig1():
    """Fig 1: System Architecture"""
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Styles
    box_style = dict(boxstyle='round,pad=0.5', facecolor='#F8FAFC', edgecolor='#1E40AF', linewidth=1.5)
    header_font = {'fontsize': 12, 'fontweight': 'bold', 'color': '#1E40AF', 'family': 'serif'}
    item_font = {'fontsize': 10, 'family': 'serif'}

    # 1. DATA SOURCES
    ax.text(5, 9.5, 'DATA SOURCES', ha='center', **header_font)
    ax.add_patch(patches.FancyBboxPatch((1.5, 8.2), 3, 0.8, **box_style))
    ax.text(3, 8.6, "CPCB CAAQM Network\n(Ground-truth hourly)", ha='center', **item_font)
    ax.add_patch(patches.FancyBboxPatch((5.5, 8.2), 3, 0.8, **box_style))
    ax.text(7, 8.6, "OpenWeatherMap API\n(Meteorological data)", ha='center', **item_font)

    # 2. PREPROCESSING LAYER
    ax.text(5, 7.5, 'PREPROCESSING LAYER', ha='center', **header_font)
    ax.add_patch(patches.FancyBboxPatch((1.5, 6.2), 7, 0.8, **box_style))
    ax.text(5, 6.6, "Missing Value Imputation | IQR Outlier Removal | Min-Max Normalization | 24h Windowing", ha='center', **item_font)

    # 3. MODEL LAYER
    ax.text(5, 5.5, 'MODEL LAYER (COMPARATIVE ANALYSIS)', ha='center', **header_font)
    ax.add_patch(patches.FancyBboxPatch((1, 4.2), 1.8, 0.8, **box_style))
    ax.text(1.9, 4.6, "Linear\nRegression", ha='center', **item_font)
    ax.add_patch(patches.FancyBboxPatch((3.2, 4.2), 1.8, 0.8, **box_style))
    ax.text(4.1, 4.6, "XGBoost\nRegressor", ha='center', **item_font)
    ax.add_patch(patches.FancyBboxPatch((5.4, 4.2), 1.8, 0.8, **box_style))
    ax.text(6.3, 4.6, "LightGBM\nRegressor", ha='center', **item_font)
    ax.add_patch(patches.FancyBboxPatch((7.6, 4.2), 1.8, 0.8, **box_style))
    ax.text(8.5, 4.6, "LSTM\n(RNN)", ha='center', **item_font)

    # 4. PRESENTATION LAYER
    ax.text(5, 3.5, 'PRESENTATION LAYER', ha='center', **header_font)
    ax.add_patch(patches.FancyBboxPatch((1.5, 2.2), 3, 0.8, **box_style))
    ax.text(3, 2.6, "Interactive Dashboard\n(Streamlit UI)", ha='center', **item_font)
    ax.add_patch(patches.FancyBboxPatch((5.5, 2.2), 3, 0.8, **box_style))
    ax.text(7, 2.6, "Multi-Horizon Forecasts\n(1h, 6h, 12h, 24h)", ha='center', **item_font)

    # Arrows
    arrow_props = dict(arrowstyle='->', lw=1.5, color='#64748B')
    ax.annotate('', xy=(5, 8.2), xytext=(5, 7.7), arrowprops=arrow_props) # Logic check: arrow direction
    # Fix arrows directions
    ax.annotate('', xy=(5, 7.55), xytext=(5, 8.2), arrowprops=arrow_props) # Down to preprocessing
    ax.annotate('', xy=(5, 5.55), xytext=(5, 6.2), arrowprops=arrow_props) # Down to models
    ax.annotate('', xy=(5, 3.55), xytext=(5, 4.2), arrowprops=arrow_props) # Down to presentation

    plt.tight_layout()
    plt.savefig('fig1_system_architecture.png', bbox_inches='tight', transparent=False)
    plt.close()

def draw_fig2():
    """Fig 2: Training workflow - XGBoost no down arrows"""
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    box_style = dict(boxstyle='round,pad=0.5', facecolor='#F0F9FF', edgecolor='#0369A1', linewidth=1.2)
    font = {'fontsize': 10, 'family': 'serif'}

    # Blocks
    ax.add_patch(patches.FancyBboxPatch((0.5, 2), 2, 1, **box_style))
    ax.text(1.5, 2.5, "Input Features\n(Pollutants + Met)", ha='center', **font)

    # XGBoost Block - No down arrows allowed
    ax.add_patch(patches.FancyBboxPatch((4, 2), 2, 1, **box_style))
    ax.text(5, 2.5, "XGBoost\nLearning Stage", ha='center', **font, weight='bold')

    ax.add_patch(patches.FancyBboxPatch((7.5, 2), 2, 1, **box_style))
    ax.text(8.5, 2.5, "Evaluation Metrics\n(MAE, RMSE, R²)", ha='center', **font)

    # Horizontal Flow Arrows only
    arrow_props = dict(arrowstyle='->', lw=2, color='#0369A1')
    ax.annotate('', xy=(4, 2.5), xytext=(2.5, 2.5), arrowprops=arrow_props)
    ax.annotate('', xy=(7.5, 2.5), xytext=(6, 2.5), arrowprops=arrow_props)

    plt.title("XGBoost Model Training and Evaluation Flow", fontsize=12, fontweight='bold', family='serif', pad=20)
    plt.savefig('fig2_training_workflow.png', bbox_inches='tight', transparent=False)
    plt.close()

def draw_fig3():
    """Fig 3: Experimental Pipeline - Stages above boxes"""
    fig, ax = plt.subplots(figsize=(12, 4), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 4)
    ax.axis('off')

    box_style = dict(boxstyle='round,pad=0.4', facecolor='#F5F3FF', edgecolor='#4338CA', linewidth=1.2)
    stage_font = {'fontsize': 10, 'fontweight': 'bold', 'color': '#4338CA', 'family': 'serif'}
    item_font = {'fontsize': 9, 'family': 'serif'}

    stages = [
        "Data Collection", "Prep & Cleaning", "Chronological Split",
        "Model Training", "Evaluation", "Forecasting", "Deployment"
    ]
    
    details = [
        "CPCB/OpenWeather", "Imputation/Norm", "80/20 Time-Split",
        "LR/XGB/LGB/LSTM", "MAE/RMSE/R²", "Multi-Step recursive", "Streamlit App"
    ]

    for i in range(7):
        x_pos = i * 2 + 0.2
        # Stage label ABOVE the box
        ax.text(x_pos + 0.8, 3.2, f"Stage {i+1}", ha='center', **stage_font)
        ax.text(x_pos + 0.8, 2.8, stages[i], ha='center', **item_font, fontweight='bold')
        
        # Box
        ax.add_patch(patches.FancyBboxPatch((x_pos, 1.5), 1.6, 1, **box_style))
        ax.text(x_pos + 0.8, 2, details[i], ha='center', **item_font)

        # Arrow to next stage
        if i < 6:
            ax.annotate('', xy=(x_pos + 2, 2), xytext=(x_pos + 1.6, 2),
                        arrowprops=dict(arrowstyle='->', lw=1.5, color='#4338CA'))

    plt.savefig('fig3_experimental_pipeline.png', bbox_inches='tight', transparent=False)
    plt.close()

if __name__ == "__main__":
    draw_fig1()
    draw_fig2()
    draw_fig3()
    print("All diagrams regenerated successfully.")
