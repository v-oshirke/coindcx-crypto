import streamlit as st
import pandas as pd
import requests
import time
import ta
import numpy as np

# --- Constants ---
futures_pairs = ['VTHO_USDT', 'APT_USDT', 'QNT_USDT', 'ORCA_USDT', 'FIDA_USDT', 'GLM_USDT', 'CFX_USDT', 'YFI_USDT', 'ARKM_USDT', 'STX_USDT', 'IMX_USDT', 'ACH_USDT', 'PERP_USDT', 'ARB_USDT', 'SUI_USDT', 'ENS_USDT', 'WLD_USDT', 'ETC_USDT', 'JUP_USDT', 'PORTAL_USDT', 'BOME_USDT', 'ETHFI_USDT', 'SHELL_USDT', 'KAITO_USDT', 'OM_USDT', 'BMT_USDT', 'NIL_USDT', 'PARTI_USDT', 'PAXG_USDT', 'ICP_USDT', 'ENA_USDT', 'BIO_USDT', 'S_USDT', 'ANIME_USDT', 'TIA_USDT', 'BB_USDT', 'CRV_USDT', 'NOT_USDT', 'CAKE_USDT', 'AR_USDT', 'SUPER_USDT', 'ZK_USDT', 'MANTA_USDT', 'IOTX_USDT', 'ORDI_USDT', 'WIF_USDT', 'IO_USDT', 'ILV_USDT', 'COW_USDT', 'GAS_USDT', 'DYDX_USDT', 'BNB_USDT', 'KAVA_USDT', 'USDC_USDT', 'ALICE_USDT', 'BTC_USDT', 'XRP_USDT', 'SUSHI_USDT', 'COTI_USDT', 'XTZ_USDT', 'THETA_USDT', 'LRC_USDT', 'SNX_USDT', 'REZ_USDT', 'DOT_USDT', 'XAI_USDT', 'STORJ_USDT', 'W_USDT', 'LISTA_USDT', 'HIGH_USDT', 'ZRO_USDT', 'LINK_USDT', 'XLM_USDT', 'RENDER_USDT', 'BANANA_USDT', 'ADA_USDT', 'G_USDT', 'UMA_USDT', 'NMR_USDT', 'CHR_USDT', 'SUN_USDT', 'DOGS_USDT', 'NEO_USDT', 'BICO_USDT', 'STRK_USDT', 'DYM_USDT', 'GMT_USDT', 'TLM_USDT', 'HMSTR_USDT', 'EIGEN_USDT', 'SCR_USDT', 'ZEC_USDT', 'PNUT_USDT', 'ATOM_USDT', 'RONIN_USDT', 'ACX_USDT', 'IOST_USDT', 'ME_USDT', 'MINA_USDT', 'TRX_USDT', 'SYS_USDT', 'ALGO_USDT', 'TWT_USDT', 'COMP_USDT', 'DOGE_USDT', 'RLC_USDT', 'MKR_USDT', 'TRB_USDT', 'EGLD_USDT', 'SOL_USDT', 'UNI_USDT', 'VANA_USDT', 'AXS_USDT', 'AVAX_USDT', 'KSM_USDT', 'NEAR_USDT', 'AAVE_USDT', 'PIXEL_USDT', 'MASK_USDT', 'LPT_USDT', 'PEOPLE_USDT', 'SKL_USDT', 'USUAL_USDT', 'METIS_USDT', 'LUMIA_USDT', 'CELO_USDT', 'APE_USDT', 'OMNI_USDT', 'ONE_USDT', 'GRT_USDT', 'SYN_USDT', 'TNSR_USDT', 'BLUR_USDT', 'RSR_USDT', 'PENGU_USDT', 'CTSI_USDT', 'NFP_USDT', 'PHA_USDT', 'PROM_USDT', 'SOLV_USDT', 'WOO_USDT', 'SEI_USDT', 'RVN_USDT', 'HBAR_USDT', 'JASMY_USDT', 'MEME_USDT', 'POLYX_USDT', 'ROSE_USDT', 'CELR_USDT', 'INJ_USDT', 'NKN_USDT', 'MOVR_USDT', 'LDO_USDT', 'FIL_USDT', 'ZIL_USDT', 'DENT_USDT', 'OGN_USDT', 'POL_USDT', 'BCH_USDT', 'SXP_USDT', 'ETH_USDT']

# --- Function to fetch data and compute RSI ---
def data_downloader(name, interval="5m"):
    url = f"https://public.coindcx.com/market_data/candles?pair=B-{name}&interval={interval}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        df = pd.DataFrame(data, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
        if df.empty or len(df) < 20:
            return None

        df['date_time'] = df['time'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(str(x)[:10]))))
        df['date_time'] = pd.to_datetime(df['date_time']).dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')

        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)

        df = df.sort_values(by='date_time').reset_index(drop=True)
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)

        latest_row = df.iloc[-1]
        return {
            "symbol": name,
            "datetime": latest_row['date_time'].strftime("%Y-%m-%d %H:%M:%S"),
            "rsi": round(latest_row['rsi'], 2) if pd.notna(latest_row['rsi']) else None
        }

    except Exception as e:
        return {"symbol": name, "error": str(e)}
# --- Streamlit UI ---
st.title("📈 Crypto $$$")
st.markdown("Live RSI-based signal for crypto futures pairs on **CoinDCX**")

if st.button("🔄 Run RSI Scan"):
    results = []
    for symbol in futures_pairs:
        row = data_downloader(symbol)
        if row:
            results.append(row)

    df_result = pd.DataFrame(results)

    if not df_result.empty and "rsi" in df_result.columns:
        df_result["signal"] = np.where(df_result["rsi"] <= 30, "BUY",
                                np.where(df_result["rsi"] >= 70, "SELL", "NEUTRAL"))
        filtered_df = df_result[df_result['signal'] != 'NEUTRAL']

        if not filtered_df.empty:
            st.success("📊 Signals generated!")
            st.dataframe(filtered_df.reset_index(drop=True))
        else:
            st.info("No BUY/SELL signals right now. All pairs are in NEUTRAL zone.")
    else:
        st.warning("No data available.")
else:
    st.info("Click the button above to scan for RSI signals.")
