import streamlit as st
import pandas as pd

# Judul aplikasi 
st.title('Asset UnSchedule Maintenance')

# upload file 
upload_prev = st.sidebar.file_uploader("Upload file Preventive", type=["xlsx"])
upload_asset = st.sidebar.file_uploader("Upload file asset", type=["xlsx"])

# cek jika ada file yang diupload

if upload_prev is not None and upload_asset is not None:
    # baca file 
    df1 = pd.read_excel(upload_prev)
    df2 = pd.read_excel(upload_asset)

    df_prev = df1[['Ticket ID', 'Item ID']]
    df_asset = df2[['ID','Name','Category','Location']]
    df_asset = df_asset.rename(columns={'ID': 'Item ID', 'Name':'Item Name', 'Category':'Item Category'})
    df_merged = pd.merge(df_prev, df_asset, on='Item ID', suffixes=('_prev','_asset'), how='right')
    
    #--df untuk data ticket == null #
    unschedule_asset = df_merged[df_merged['Ticket ID'].isnull()]
    
    # ---Filter--- untuk unschedule_asset #
    filter_category = ["All"] + unschedule_asset['Item Category'].unique().tolist()
    select_category = st.sidebar.selectbox("Pilih Category", options=filter_category )
    if select_category != "All":
        filterdf = unschedule_asset[unschedule_asset['Item Category']==select_category]
    else:
        filterdf = unschedule_asset

    #----------Filter end ---------------#

    if not df_merged.empty:
        # st.dataframe(row_isna, hide_index=True, use_container_width=True)
        st.dataframe(filterdf, hide_index=True, use_container_width=True)
    else:
        st.write("Tidak ada asset yang belum")

else:
    st.write(" Upload File yang akan di Compare")