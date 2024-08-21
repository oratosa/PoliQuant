import streamlit as st


def top_page():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    st.write("# Welcome to PoliQuant! 👋")

    st.markdown(
        """
        PoliQuantは日本の国会議員の国会における活動を可視化するプロジェクトです。
        👈 衆議院議員/参議院議員の国会での活動量を確認する。
        ### Want to learn more?
        - Check out [国会会議録検索システム API](https://kokkai.ndl.go.jp/api.html)
        ### See the repository of this project
        - [PoliQuant](https://github.com/oratosa/PoliQuant)
    """
    )


pg = st.navigation(
    [
        st.Page(top_page, title="Top page", icon=":material/home:"),
        st.Page("pages/app.py", title="衆議院議員", icon="🔥"),
    ]
)
pg.run()
