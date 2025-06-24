import streamlit as st
import numpy as np
import pandas as pd
import numpy_financial as npf

st.set_page_config(page_title="IRR 计算器", layout="wide")
st.title("📈 多功能 IRR（内部收益率）计算器")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "1. 永续等额现金流",
    "2. 永续增长现金流",
    "3. 有限等额现金流",
    "4. 有限等额 + 残值",
    "5. 多项目 IRR 比较"
])

# ---------- Tab 1 ----------
with tab1:
    st.header("永续等额现金流 IRR（Perpetual Constant CF）")
    cf = st.number_input("每期现金流", value=100.0)
    investment = st.number_input("初始投资（负数）", value=-1000.0)
    if cf != 0:
        irr = -cf / investment 
        st.success(f"IRR = {irr:.2%}")
    else:
        st.warning("现金流不能为0")

# ---------- Tab 2 ----------
with tab2:
    st.header("永续增长现金流 IRR（Gordon Growth Model）")
    cf1 = st.number_input("第一期现金流", value=100.0, key="g_cf1")
    g = st.number_input("年增长率（g）", value=0.02)
    investment2 = st.number_input("初始投资（负数）", value=-1000.0, key="g_invest")
    if g < 1:
        irr = g - cf1 / investment2
        st.success(f"IRR = {irr:.2%}")
    else:
        st.warning("增长率 g 必须 < 1")

# ---------- Tab 3 ----------
with tab3:
    st.header("有限等额现金流 IRR")
    cf = st.number_input("每期现金流", value=100.0, key="f_cf")
    n = st.number_input("期限（期数）", value=5, step=1)
    investment3 = st.number_input("初始投资（负数）", value=-1000.0, key="f_invest")
    cash_flows = [investment3] + [cf] * int(n)
    irr = npf.irr(cash_flows)
    if irr:
        st.success(f"IRR = {irr:.2%}")

# ---------- Tab 4 ----------
with tab4:
    st.header("有限期 + 最后一期残值 IRR")
    cf = st.number_input("每期现金流", value=100.0, key="fv_cf")
    n = st.number_input("期限（期数）", value=5, step=1, key="fv_n")
    final_value = st.number_input("最后一期额外残值", value=200.0)
    investment4 = st.number_input("初始投资（负数）", value=-1000.0, key="fv_invest")
    flows = [cf] * (int(n) - 1) + [cf + final_value]
    cash_flows = [investment4] + flows
    irr = npf.irr(cash_flows)
    if irr:
        st.success(f"IRR = {irr:.2%}")

# ---------- Tab 5 ----------
with tab5:
    st.header("多项目 IRR 比较（结构化输入）")

    num_projects = st.number_input("项目数量", min_value=1, max_value=5, value=2, step=1)
    all_results = []

    for i in range(int(num_projects)):
        with st.expander(f"📁 项目 {i+1}", expanded=True):
            project_name = st.text_input(f"项目名称", value=f"项目{i+1}", key=f"pname_{i}")
            num_scenarios = st.number_input("场景数量", min_value=1, max_value=5, value=2, key=f"pscen_{i}")

            for j in range(int(num_scenarios)):
                st.markdown("---")
                scen_name = st.text_input(f"场景 {j+1} 名称", value=f"场景{j+1}", key=f"sname_{i}_{j}")
                cf_type = st.selectbox("现金流类型", ["永续等额", "永续增长", "有限等额", "有限等额+残值"], key=f"cf_type_{i}_{j}")
                
                invest = st.number_input("初始投资（负数）", value=-1000.0, key=f"inv_{i}_{j}")

                if cf_type == "永续等额":
                    cf = st.number_input("每期现金流", value=100.0, key=f"cf_{i}_{j}")
                    irr = -cf / invest if cf != 0 else None

                elif cf_type == "永续增长":
                    cf1 = st.number_input("第一期现金流", value=100.0, key=f"cf1_{i}_{j}")
                    g = st.number_input("增长率（g）", value=0.02, key=f"g_{i}_{j}")
                    irr = g - cf1 / invest if invest != 0 else None

                elif cf_type == "有限等额":
                    cf = st.number_input("每期现金流", value=100.0, key=f"cf_f_{i}_{j}")
                    n = st.number_input("期限", value=5, step=1, key=f"n_{i}_{j}")
                    flows = [invest] + [cf] * int(n)
                    irr = npf.irr(flows)

                elif cf_type == "有限等额+残值":
                    cf = st.number_input("每期现金流", value=100.0, key=f"cf_fv_{i}_{j}")
                    n = st.number_input("期限", value=5, step=1, key=f"n_fv_{i}_{j}")
                    fv = st.number_input("最终残值", value=200.0, key=f"fv_{i}_{j}")
                    flows = [invest] + [cf] * (int(n)-1) + [cf + fv]
                    irr = npf.irr(flows)

                irr_display = f"{irr:.2%}" if irr is not None else "计算失败"
                all_results.append({
                    "项目": project_name,
                    "场景": scen_name,
                    "类型": cf_type,
                    "IRR": irr_display
                })

    if all_results:
        st.subheader("📊 IRR 汇总表")
        st.dataframe(pd.DataFrame(all_results))
