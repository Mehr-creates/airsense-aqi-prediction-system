import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from datetime import datetime

class ModelExplainer:
    def __init__(self):
        self.colors = {
            'primary': '#8A2BE2',
            'secondary': '#FF69B4', 
            'background': '#F8F8FF',
            'text': '#4B0082'
        }
    
    def generate_shap_explanation(self, model, X, feature_names):
        """Generate SHAP explanations for model predictions"""
        try:
            # For demo, create simulated SHAP values
            np.random.seed(42)
            shap_values = np.random.normal(0, 0.5, (X.shape[0], X.shape[1]))
            
            # Create summary plot
            fig = self._create_shap_summary_plot(shap_values, X, feature_names)
            return fig, None
            
        except Exception as e:
            st.warning(f"SHAP explanation failed: {e}")
            return self._create_dummy_shap_plot(feature_names), None
    
    def _create_shap_summary_plot(self, shap_values, X, feature_names):
        """Create SHAP summary plot"""
        feature_importance = np.abs(shap_values).mean(0)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=feature_names,
            x=feature_importance,
            orientation='h',
            marker_color=self.colors['primary'],
            name='Feature Importance'
        ))
        
        fig.update_layout(
            title='SHAP Feature Importance',
            xaxis_title='Mean |SHAP Value|',
            yaxis_title='Features',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor='white',
            font=dict(color=self.colors['text']),
            height=400
        )
        
        return fig
    
    def _create_dummy_shap_plot(self, feature_names):
        """Create dummy SHAP plot for demo"""
        feature_importance = np.random.uniform(0, 1, len(feature_names))
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=feature_names,
            x=feature_importance,
            orientation='h',
            marker_color=self.colors['primary']
        ))
        
        fig.update_layout(
            title='SHAP Feature Importance (Demo)',
            xaxis_title='Mean |SHAP Value|',
            yaxis_title='Features',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor='white',
            font=dict(color=self.colors['text']),
            height=400
        )
        
        return fig
    
    def generate_lime_explanation(self, model, X, feature_names, instance_idx=0):
        """Generate LIME explanation for a specific instance"""
        try:
            # For demo, create simulated LIME explanation
            explanation_data = list(zip(feature_names, np.random.uniform(-1, 1, len(feature_names))))
            
            # Create visualization
            fig = self._create_lime_plot(explanation_data, feature_names)
            return fig
            
        except Exception as e:
            st.warning(f"LIME explanation failed: {e}")
            return self._create_dummy_lime_plot(feature_names)
    
    def _create_lime_plot(self, explanation_data, feature_names):
        """Create LIME explanation plot"""
        features = [x[0] for x in explanation_data]
        weights = [x[1] for x in explanation_data]
        
        colors = [self.colors['primary'] if w > 0 else self.colors['secondary'] for w in weights]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weights,
            y=features,
            orientation='h',
            marker_color=colors
        ))
        
        fig.update_layout(
            title='LIME Feature Contribution',
            xaxis_title='Feature Weight',
            yaxis_title='Features',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor='white',
            font=dict(color=self.colors['text']),
            height=400
        )
        
        return fig
    
    def _create_dummy_lime_plot(self, feature_names):
        """Create dummy LIME plot for demo"""
        weights = np.random.uniform(-1, 1, len(feature_names))
        colors = [self.colors['primary'] if w > 0 else self.colors['secondary'] for w in weights]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weights,
            y=feature_names,
            orientation='h',
            marker_color=colors
        ))
        
        fig.update_layout(
            title='LIME Feature Contribution (Demo)',
            xaxis_title='Feature Weight',
            yaxis_title='Features',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor='white',
            font=dict(color=self.colors['text']),
            height=400
        )
        
        return fig

class AlertSystem:
    def __init__(self):
        self.alert_history = []
    
    def check_hazardous_aqi(self, current_data, forecast_data, threshold=4.0):
        """Check for hazardous AQI conditions"""
        alerts = []
        
        # Check current AQI
        current_aqi = current_data.get('aqi', 0)
        if current_aqi >= threshold:
            alerts.append({
                'type': 'CURRENT_HAZARDOUS',
                'severity': 'HIGH',
                'message': f'Current AQI ({current_aqi:.1f}) is HAZARDOUS! Take immediate precautions.',
                'timestamp': datetime.now(),
                'value': current_aqi
            })
        
        # Check forecast
        for model, predictions in forecast_data.items():
            for i, prediction in enumerate(predictions):
                if prediction >= threshold:
                    alerts.append({
                        'type': 'FORECAST_HAZARDOUS',
                        'severity': 'MEDIUM',
                        'message': f'{model.upper()} predicts hazardous AQI ({prediction:.1f}) in {i+1} day(s)',
                        'timestamp': datetime.now(),
                        'model': model,
                        'day': i + 1,
                        'value': prediction
                    })
        
        # Add to history
        self.alert_history.extend(alerts)
        
        # Keep only last 50 alerts
        self.alert_history = self.alert_history[-50:]
        
        return alerts
    
    def get_alert_stats(self):
        """Get alert statistics"""
        if not self.alert_history:
            return {'total': 0, 'high': 0, 'medium': 0}
        
        total = len(self.alert_history)
        high = len([a for a in self.alert_history if a['severity'] == 'HIGH'])
        medium = len([a for a in self.alert_history if a['severity'] == 'MEDIUM'])
        
        return {'total': total, 'high': high, 'medium': medium}