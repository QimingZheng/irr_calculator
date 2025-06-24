import streamlit as st
import pandas as pd
import numpy_financial as npf

st.set_page_config(page_title="IRR 计算器", layout="wide")
st.title("📈 多项目 IRR 计算器")

st.markdown("为每个项目/场景输入以下参数：")

num_projects = st.number_input("项目数量", min_value=0, max_value=10, value=0, step=1)

results = []

for i in range(int(num_projects)):
    # with st.expander(f"📁 项目 {i+1} 配置", expanded=True):
    #     project_name = st.text_input("项目名称", value=f"项目{i+1}", key=f"pname_{i}")
    #     scenario_name = st.text_input("场景名称", value="基础场景", key=f"scname_{i}")

    #     invest = st.number_input("初始投入（负数）", value=-1000.0, key=f"inv_{i}")
    #     cf = st.number_input("每期现金流", value=100.0, key=f"cf_{i}")
    #     n = st.number_input("期数（0 表示永续）", min_value=0, step=1, value=5, key=f"n_{i}")
    #     g = st.number_input("现金流增长率（如 5% 填 0.05）", value=0.0, key=f"g_{i}")
    #     rv = st.number_input("残值（仅限有限期）", value=0.0, key=f"rv_{i}")
    with st.expander(f"📁 项目 {i+1} 配置", expanded=True):
        cola, colb = st.columns(2)
        with cola:
            project_name = st.text_input("项目名称", value=f"项目{i+1}", key=f"pname_{i}")
        with colb:
            scenario_name = st.text_input("场景名称", value="基础场景", key=f"scname_{i}")

        # 第一行横排：初始投入、每期现金流、增长率
        # 第二行横排：期数、残值
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            invest = st.number_input("初始投入（负数）", value=-1000.0, key=f"inv_{i}")
        with col2:
            cf = st.number_input("每期现金流", value=100.0, key=f"cf_{i}")
        with col3:
            g = st.number_input("增长率（如0.05）", value=0.0, key=f"g_{i}")
        with col4:
            n = st.number_input("期数（0表示永续）", min_value=0, step=1, value=5, key=f"n_{i}")
        with col5:
            rv = st.number_input("残值", value=0.0, key=f"rv_{i}")

        irr = None
        try:
            if n == 0:  # 永续
                if g == 0:
                    irr = -cf / invest
                else:
                    irr = g - cf / invest
            else:
                flows = []
                for t in range(int(n)):
                    flows.append(cf * ((1 + g) ** t))
                flows[-1] += rv  # 加残值
                cashflows = [invest] + flows
                irr = npf.irr(cashflows)
        except Exception as e:
            irr = None

        irr_display = f"{irr:.2%}" if irr is not None else "计算失败"
        results.append({
            "项目": project_name,
            "场景": scenario_name,
            "IRR": irr_display
        })

if results:
    st.subheader("📊 IRR 计算结果汇总")
    st.dataframe(pd.DataFrame(results))
