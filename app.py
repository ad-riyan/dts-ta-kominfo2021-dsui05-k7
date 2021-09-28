import pickle
import numpy as np
import streamlit as st

# opt_foundation = {"Bambu/Kayu": 0,
#                   "Semen/Batu/Bata/Beton": 1,
#                   "Mortar lumpur, batu, dan bata": 2}
# opt_superstructure = {"Mortar lumpur dan batu": 0,
#                       "Kayu": 1,
#                       "Lainnya": 2}
opt_area_assess = {"Eksterior-Interior": 0,
                   "Reruntuhan bangunan sudah dibuang": 1}
opt_collapse = {"Tidak rusak": 0,
                "Rusak ringan/tidak signifikan": 1,
                "Rusak menengah s/d berat": 2,
                "Rusat sangat berat s/d hancur": 3}
opt_leaning = {"Tidak ada": 0,
               "Rendah/tidak signifikan": 1,
               "Menengah s/d berat": 2,
               "Berat s/d hancur": 3}
# opt_adj_risk = {"Tidak ada": 0,
#                 "Rendah/tidak signifikan": 1,
#                 "Menengah s/d berat": 2,
#                 "Berat s/d hancur": 3}
opt_dgts = {0: ["1", "Tidak perlu"],
            1: ["2", "Minor"],
            2: ["3", "Mayor"],
            3: ["4", "Rekonstruksi"],
            4: ["5", "Rekonstruksi"]}


def do_prediction(_doc, _dol, _cf_ratio, _h_ratio, _aa_both, _aa_build_rem):
    model = pickle.load(open("model.pkl", "rb"))
    X = np.array([_doc, _dol, _h_ratio, _cf_ratio, _aa_both, _aa_build_rem]).reshape((1, -1))
    return model.predict(X)


def display_prediction(ypr):
    dg, ts = opt_dgts[ypr]
    col1, col2 = st.columns(2)
    with col1:
        st.header("Tingkat kerusakan")
        if ypred <= 1:
            disp_text_col1 = '<p style="font-family:Lato; color:Blue; font-size:96px;' \
                             'font-weight:bold;">%s</p>' % (dg, )
        elif ypred == 2:
            disp_text_col1 = '<p style="font-family:Lato; color:DarkGoldenRod; font-size:96px;' \
                             'font-weight:bold;">%s</p>' % (dg,)
        else:
            disp_text_col1 = '<p style="font-family:Lato; color:Red; font-size:96px;' \
                             'font-weight:bold;">%s</p>' % (dg,)
        st.markdown(disp_text_col1, unsafe_allow_html=True)

    with col2:
        st.header("Usul perbaikan")
        disp_text_col2 = '<p style="font-family:Lato; color:Blue; font-size:36px;' \
                         'font-weight:bold;">%s</p>' % (ts,)
        st.markdown(disp_text_col2, unsafe_allow_html=True)


st.title("Prediksi Kerusakan Bangunan dan Rekomendasi Perbaikan")
st.empty()
st.markdown("*Aplikasi ini ditujukan untuk memprediksi kerusakan bangunan pasca gempa berikut "
            "dengan rekomendasi perbaikan.*")
st.empty()
st.write("*Silakan diisi **Parameter**-nya dan kemudian tekan tombol **Prediksi**!*")
st.empty()
text_ = "Project Tugas Akhir DTS-TA Kominfo 2021 -- Data Scientist: Artificial Intelligence " \
        "untuk Dosen dan Instruktur"
st.info(text_)
st.empty()


with st.sidebar:
    st.title("Parameter:")
    area = st.selectbox(label="Area bangunan yang disurvey:",
                        options=[key for key in opt_area_assess.keys()])
    aa_both = 0
    aa_build_rem = 0
    if opt_area_assess[area] == 0:
        aa_both = 1
    elif opt_area_assess[area] == 0:
        aa_build_rem = 1

    do_collapse = st.selectbox(label="Penilaian kondisi kerusakan bangunan secara keseluruhan:",
                               options=[key for key in opt_collapse.keys()],
                               index=len(opt_collapse) - 1)
    doc = opt_collapse[do_collapse]

    do_leaning = st.selectbox(label="Penilaian kondisi perampingan bangunan secara keseluruhan:",
                              options=[key for key in opt_leaning.keys()],
                              index=len(opt_leaning) - 1)
    dol = opt_leaning[do_leaning]

    # do_adj_risk = st.selectbox(label="Penilaian kondisi resiko bangunan yang berdampingan secara "
    #                                  "keseluruhan:",
    #                            options=[key for key in opt_adj_risk.keys()],
    #                            index=len(opt_adj_risk) - 1)
    # doaj = opt_adj_risk[do_adj_risk]

    cf_ratio = st.slider(label="Rasio jumlah lantai bangunan:",
                         min_value=0.,
                         max_value=1.,
                         step=0.01,
                         help="Perbandingan jumlah lantai bangunan pasca gempa dengan sebelum "
                             "gempa.")

    h_ratio = st.slider(label="Rasio ketinggian bangunan:",
                        min_value=0.,
                        max_value=1.,
                        step=0.01,
                        help="Perbandingan ketinggian bangunan pasca gempa dengan sebelum gempa.")

    predict_button = st.button(label="Prediksi")

if predict_button:
    st.empty()
    ypred = do_prediction(doc, dol, cf_ratio, h_ratio, aa_both, aa_build_rem)
    display_prediction(ypred[0])

