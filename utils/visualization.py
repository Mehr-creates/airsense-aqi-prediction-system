import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class AQIVisualizer:
    """
    Wraps all Plotly graph generation into reusable methods.
    Maintains a consistent global color palette ensuring UI uniformity.
    """
    def __init__(self):
        # Dark Navy Blue Color Scheme
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#3b82f6',
            'accent': '#60a5fa',
            'background': '#0f172a',
            'card_bg': '#111827',
            'text': '#e5e7eb',
            'text_secondary': '#9ca3af',
            'success': '#16a34a',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'grid': '#1f2937'
        }
    
    def create_gauge_chart(self, aqi_value):
        """Create AQI gauge chart with clean zones"""
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = aqi_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [1, 5], 'tickwidth': 1, 'tickcolor': self.colors['grid'], 'tickfont': {'color': self.colors['text_secondary']}},
                'bar': {'color': 'rgba(0,0,0,0)'},
                'bgcolor': self.colors['card_bg'],
                'steps': [
                    {'range': [1, 2], 'color': self.colors['success']},
                    {'range': [2, 3], 'color': self.colors['warning']},
                    {'range': [3, 4], 'color': self.colors['danger']},
                    {'range': [4, 5], 'color': '#7f1d1d'}],
                'threshold': {
                    'line': {'color': self.colors['text'], 'width': 4},
                    'thickness': 0.75,
                    'value': aqi_value}}))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': self.colors['text'], 'family': "Inter"},
            height=250,
            margin=dict(l=30, r=30, t=30, b=30)
        )
        
        return fig
    
    def create_mini_trend(self, historical_data):
        """Create a minimal 24-hr trend chart"""
        df = historical_data.tail(24) if len(historical_data) >= 24 else historical_data
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['date'] if 'date' in df.columns else df.index,
            y=df['aqi'],
            mode='lines',
            line=dict(color=self.colors['primary'], width=3),
            fill='tozeroy',
            fillcolor='rgba(37, 99, 235, 0.1)'
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=self.colors['text'], family="Inter"),
            height=250,
            xaxis=dict(showgrid=True, gridcolor=self.colors['grid'], showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor=self.colors['grid'], zeroline=False),
            margin=dict(l=10, r=10, t=20, b=10),
            showlegend=False
        )
        return fig

    def create_historical_trend(self, historical_data):
        """Create historical AQI trend chart with new colors"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=historical_data['date'],
            y=historical_data['aqi'],
            mode='lines+markers',
            name='AQI Trend',
            line=dict(color=self.colors['primary'], width=4),
            marker=dict(size=8, color=self.colors['secondary'])
        ))
        
        fig.update_layout(
            title={'text': 'Historical AQI Trend (30 Days)', 'font': {'color': self.colors['text'], 'size': 20}},
            xaxis_title='Date',
            yaxis_title='AQI Level',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            height=450,
            xaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            yaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            showlegend=False
        )
        
        return fig
    
    def create_forecast_chart(self, forecast_data):
        """Create forecast comparison chart with new colors"""
        days = ['Today', 'Tomorrow', 'Day After']
        fig = go.Figure()
        
        # Define colors for different models
        model_colors = {
            'linear_regression': '#F59E0B',
            'xgboost': self.colors['primary'],
            'lightgbm': self.colors['secondary'], 
            'lstm': self.colors['accent']
        }
        
        for model, values in forecast_data.items():
            fig.add_trace(go.Scatter(
                x=days,
                y=values,
                mode='lines+markers',
                name=model.upper(),
                line=dict(width=4, color=model_colors.get(model, self.colors['primary'])),
                marker=dict(size=10)
            ))
        
        fig.update_layout(
            title={'text': '3-Day AQI Forecast - Model Comparison', 'font': {'color': self.colors['text'], 'size': 20}},
            xaxis_title='Day',
            yaxis_title='Predicted AQI',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            height=450,
            xaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            yaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            legend=dict(
                bgcolor=self.colors['card_bg'],
                bordercolor=self.colors['grid'],
                borderwidth=1
            )
        )
        
        return fig
    
    def create_pollutants_chart(self, current_data):
        """Create pollutants breakdown chart with new colors"""
        pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']
        values = [
            current_data['pm2_5'],
            current_data['pm10'],
            current_data['no2'],
            current_data['so2'],
            current_data['co'],
            current_data['o3']
        ]
        
        fig = px.bar(
            x=pollutants,
            y=values,
            color=pollutants,
            color_discrete_sequence=[
                self.colors['primary'],
                self.colors['secondary'],
                self.colors['accent'],
                self.colors['success'],
                self.colors['warning'],
                self.colors['danger']
            ]
        )
        
        fig.update_layout(
            title={'text': 'Pollutants Concentration', 'font': {'color': self.colors['text'], 'size': 20}},
            xaxis_title='Pollutant',
            yaxis_title='Concentration (μg/m³)',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            showlegend=False,
            height=450,
            xaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            yaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid'])
        )
        
        return fig
    
    def create_model_performance(self, performance_data):
        """Create model performance comparison with new colors"""
        models = list(performance_data.keys())
        scores = list(performance_data.values())
        
        colors = [
            self.colors['success'] if score > 0.9 
            else self.colors['warning'] if score > 0.8 
            else self.colors['danger']
            for score in scores
        ]
        
        fig = go.Figure(data=[
            go.Bar(
                x=models,
                y=scores,
                marker_color=colors,
                text=[f'{score:.4f}' for score in scores],
                textposition='auto',
                textfont=dict(color=self.colors['text'], size=14)
            )
        ])
        
        fig.update_layout(
            title={
                'text': 'Model Performance (R² Score)',
                'font': {'color': self.colors['text'], 'size': 20}
            },
            xaxis_title='Model',
            yaxis_title='R² Score',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            height=450,
            xaxis=dict(
                gridcolor=self.colors['grid'],
                linecolor=self.colors['grid']
            ),
            yaxis=dict(
                range=[0, 1.1],
                gridcolor=self.colors['grid'],
                linecolor=self.colors['grid']
            )
        )
        
        return fig

    def create_research_grouped_metrics(self, perf_data):
        """1. Grouped Bar Chart of ALL metrics for research paper"""
        models = list(perf_data.keys())
        models_upper = [m.upper() for m in models]
        
        mae_scores = [perf_data[m].get('MAE', 0) for m in models]
        rmse_scores = [perf_data[m].get('RMSE', 0) for m in models]
        r2_scores = [perf_data[m].get('R2', 0) for m in models]
        
        fig = go.Figure()
        
        # Consistent professional colors
        fig.add_trace(go.Bar(name='MAE', x=models_upper, y=mae_scores, marker_color='#3B82F6'))
        fig.add_trace(go.Bar(name='RMSE', x=models_upper, y=rmse_scores, marker_color='#8B5CF6'))
        fig.add_trace(go.Bar(name='R² Score', x=models_upper, y=r2_scores, marker_color='#10B981'))
        
        fig.update_layout(
            barmode='group',
            title={'text': 'Performance Metrics Comparison across Models', 'font': {'color': self.colors['text'], 'size': 20}},
            xaxis_title='Model',
            yaxis_title='Score',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor='rgba(0,0,0,0)'),
            xaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            yaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            height=500
        )
        return fig

    def create_actual_vs_predicted_scatter(self, perf_data):
        """2. Actual vs Predicted Scatter with reference line"""
        num_models = len(perf_data)
        fig = make_subplots(rows=1, cols=num_models, subplot_titles=[m.upper().replace('_', ' ') for m in perf_data.keys()])
        
        model_colors = ['#F59E0B', '#3B82F6', '#8B5CF6', '#10B981']
        
        for i, (model_name, metrics) in enumerate(perf_data.items()):
            if 'y_true' in metrics and 'y_pred' in metrics:
                y_true = metrics['y_true']
                y_pred = metrics['y_pred']
                
                if y_true and y_pred:
                    # Scatter points
                    fig.add_trace(
                        go.Scatter(x=y_true, y=y_pred, mode='markers', 
                                   marker=dict(color=model_colors[i % len(model_colors)], size=6, opacity=0.6),
                                   name=model_name.upper(), showlegend=False),
                        row=1, col=i+1
                    )
                    
                    # Diagonal reference line y=x
                    min_val = min(min(y_true), min(y_pred))
                    max_val = max(max(y_true), max(y_pred))
                    fig.add_trace(
                        go.Scatter(x=[min_val, max_val], y=[min_val, max_val], mode='lines',
                                   line=dict(color='white', dash='dash'), showlegend=False),
                        row=1, col=i+1
                    )
        
        fig.update_layout(
            title={'text': 'Actual vs. Predicted AQI Values', 'font': {'color': self.colors['text'], 'size': 20}},
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            height=400,
            showlegend=False
        )
        
        for i in range(1, len(perf_data) + 1):
            fig.update_xaxes(title_text="Actual AQI", gridcolor=self.colors['grid'], row=1, col=i)
            fig.update_yaxes(title_text="Predicted AQI" if i==1 else "", gridcolor=self.colors['grid'], row=1, col=i)
            
        return fig

    def create_residual_distribution(self, perf_data):
        """3. Residual Distribution to check for error bias"""
        fig = go.Figure()
        model_colors = ['#F59E0B', '#3B82F6', '#8B5CF6', '#10B981']
        
        for i, (model_name, metrics) in enumerate(perf_data.items()):
            if 'y_true' in metrics and 'y_pred' in metrics:
                if metrics['y_true'] and metrics['y_pred']:
                    residuals = np.array(metrics['y_true']) - np.array(metrics['y_pred'])
                    
                    fig.add_trace(go.Histogram(
                        x=residuals,
                        name=model_name.upper(),
                        opacity=0.6,
                        marker_color=model_colors[i % len(model_colors)],
                        nbinsx=30
                    ))
        
        fig.update_layout(
            barmode='overlay',
            title={'text': 'Distribution of Residuals (Errors)', 'font': {'color': self.colors['text'], 'size': 20}},
            xaxis_title='Residual (Actual - Predicted)',
            yaxis_title='Count',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            legend=dict(bgcolor='rgba(0,0,0,0)'),
            xaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            yaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            height=450
        )
        
        # Add a zero line
        fig.add_vline(x=0, line_width=2, line_dash="dash", line_color="white")
        
        return fig

    def create_prediction_overlay(self, perf_data):
        """4. Time-series overlay of Actual vs Predicted for each model"""
        fig = go.Figure()
        model_colors = {'linear_regression': '#F59E0B', 'xgboost': '#3B82F6', 'lightgbm': '#8B5CF6', 'lstm': '#10B981'}
        
        # Use the first model's y_true as the ground truth line
        first_model = list(perf_data.keys())[0]
        if 'y_true' in perf_data[first_model] and perf_data[first_model]['y_true']:
            y_true = perf_data[first_model]['y_true']
            n_samples = len(y_true)
            x_axis = list(range(1, n_samples + 1))
            
            # Sort by actual value for cleaner visualization
            sorted_indices = np.argsort(y_true)
            y_true_sorted = np.array(y_true)[sorted_indices]
            
            # Actual (ground truth) line
            fig.add_trace(go.Scatter(
                x=x_axis, y=y_true_sorted,
                mode='lines',
                name='Actual AQI',
                line=dict(color='white', width=3),
            ))
            
            # Each model's predictions
            for model_name, metrics in perf_data.items():
                if 'y_pred' in metrics and metrics['y_pred']:
                    y_pred_sorted = np.array(metrics['y_pred'])[sorted_indices]
                    fig.add_trace(go.Scatter(
                        x=x_axis, y=y_pred_sorted,
                        mode='lines',
                        name=f'{model_name.upper()} Predicted',
                        line=dict(color=model_colors.get(model_name, '#F59E0B'), width=2, dash='dot'),
                    ))
        
        fig.update_layout(
            title={'text': 'Prediction Overlay: Actual vs. Model Predictions', 'font': {'color': self.colors['text'], 'size': 20}},
            xaxis_title='Test Sample (sorted by actual AQI)',
            yaxis_title='AQI Value',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['card_bg'],
            font=dict(color=self.colors['text'], family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, bgcolor='rgba(0,0,0,0)'),
            xaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            yaxis=dict(gridcolor=self.colors['grid'], linecolor=self.colors['grid']),
            height=500
        )
        
        return fig