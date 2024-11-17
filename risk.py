import streamlit as st
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shap

# 加载模型
model_path = r'C:\Users\hlibi\Desktop\data2\random_forest_model.pkl'
model = joblib.load(model_path)

# 定义特征名称
selected_features = ['D-index', 'BE', 'Kmax', 'Galectin-1', 'Galectin-3', 'IL-1 beta/IL-1F2']

# Streamlit 用户界面
st.title("早期圆锥角膜风险预测")

# 创建输入框
st.write("请输入以下特征值：")
d_index = st.number_input("D-index:", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
be = st.number_input("BE:", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
kmax = st.number_input("Kmax:", min_value=0.0, max_value=100.0, value=47.0, step=0.1)
galectin_1 = st.number_input("Galectin-1:", min_value=0.0, max_value=100.0, value=2.0, step=0.1)
galectin_3 = st.number_input("Galectin-3:", min_value=0.0, max_value=100.0, value=1.5, step=0.1)
il_1_beta = st.number_input("IL-1 beta/IL-1F2:", min_value=0.0, max_value=100.0, value=0.5, step=0.1)

# 获取输入特征数组
feature_values = [d_index, be, kmax, galectin_1, galectin_3, il_1_beta]
features = np.array([feature_values])

if st.button("预测"):
    # 预测类别和概率
    predicted_proba = model.predict_proba(features)[0]
    early_keratoconus_risk = predicted_proba[2] * 100  # 假设类别2表示早期圆锥角膜
    
    # 显示结果
    st.write(f"**早期圆锥角膜的可能性:** {early_keratoconus_risk:.2f}%")
    
    # SHAP分析
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(features)
    
    # 显示SHAP值图形
    st.write("**特征重要性分析:**")
    shap.summary_plot(shap_values[2], pd.DataFrame([feature_values], columns=selected_features), plot_type="bar", show=False)
    st.pyplot(plt)