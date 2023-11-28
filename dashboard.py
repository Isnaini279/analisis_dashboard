#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 10:49:54 2023

@author: isnainibarochatun
"""

import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Analisis Data Order Product')

# side tab menu
tab2, tab3 = st.tabs(["Visualisasi 1", "Visualisasi 2"])

# section untuk menganalisis statistik data

all_trx_df = pd.read_csv("all_trx_df.csv")


with tab2:
    st.header("Visualisasi 1")

    st.write("Visualisasi berikut merupakan hasil dari analisis data sesuai dengan pertanyaan **Kategori produk mana saja yang memiliki jumlah pemesanan paling sedikit dan paling banyak?**")

    summary_count_order = all_trx_df.groupby(by="product_category_name").agg({
        "order_id": "nunique"
    }).reset_index()

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
 
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(x="order_id", y="product_category_name", data=summary_count_order.head(5), palette=colors, ax=ax[0])
    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Best Performing Product", loc="center", fontsize=15)
    ax[0].tick_params(axis ='y', labelsize=12)
    
    sns.barplot(x="order_id", y="product_category_name", data=summary_count_order.sort_values(by="order_id", ascending=True).head(5), palette=colors, ax=ax[1])
    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].invert_xaxis()
    ax[1].yaxis.set_label_position("right")
    ax[1].yaxis.tick_right()
    ax[1].set_title("Worst Performing Product", loc="center", fontsize=15)
    ax[1].tick_params(axis='y', labelsize=12)
    
    plt.suptitle("Best and Worst Performing Category Product by Number of Order", fontsize=20)
    st.pyplot(fig)

with tab3:
    st.header("Visualisasi 2")

    st.write("Visualisasi berikut merupakan hasil dari analisis data sesuai dengan pertanyaan **Apa saja kategori produk dengan rating review di bawah rata-rata?**")

    # membuat table yang memuat informasi product_category_name dan jumlah ordernya dalam kolom order_count
    byreview_df = all_trx_df.groupby(by="product_category_name")["review_score"].nunique().reset_index()
    byreview_df.rename(columns={"review_score": "review_count"}, inplace=True)

    # mencari rata-rata pesanan dengan data order_count
    mean_review_count = byreview_df["review_count"].mean()
    st.write(byreview_df)
    st.write('Berdasarkan perhitungan, rata-rata review score: ', mean_review_count)

    st.write("Maka kategori produk yang mendapatkan review score di bawah rata-rata yaitu:")

    # membuat visualisasi bar chart berdasarkan nama kategori produk

    category_below_range = byreview_df[byreview_df["review_count"] < mean_review_count]
    
    plt.figure(figsize=(10, 5))
    colors = ["#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(
        x="review_count", 
        y="product_category_name",
        data=category_below_range.sort_values(by="review_count", ascending=False),
        palette=colors
    )
    plt.title("Number of Product Category Name By Under Average Review", loc="center", fontsize=15)
    plt.ylabel(None)
    plt.xlabel(None)
    plt.tick_params(axis='x', labelsize=12)
    st.pyplot(plt)
