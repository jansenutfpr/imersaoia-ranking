import streamlit as st
import re

def load_messages(filename="messages.txt"):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    
    messages = content.split('---')
    
    projects = []
    for message in messages:
        if not message.strip():
            continue
        
        nome_match = re.search(r'Nome: (.*?)(?:\n|$)', message)
        votos_match = re.search(r'Votos: (\d+)', message)
        link_match = re.search(r'Link:\s*(https?://\S+)', message)
        desc_match = re.search(r'Descrição: (.*?)(?:\n|$)', message, re.DOTALL)
        user_match = re.search(r'Usuário: (.*?)(?:\n|$)', message)
        
        if nome_match and votos_match and link_match:
            projects.append({
                'nome': nome_match.group(1).strip(),
                'votos': int(votos_match.group(1)),
                'link': link_match.group(1).strip(),
                'descricao': desc_match.group(1).strip() if desc_match else '',
                'usuario': user_match.group(1).strip() if user_match else ''
            })
    
    return projects
  
# Define o diálogo uma única vez
@st.dialog("Detalhes do Projeto")
def show_details():
    project = st.session_state.selected_project
    st.markdown(f"### {project['nome']}")
    st.markdown(f"**Usuário Discord:** {project['usuario']}")
    st.markdown(f"**Descrição:** {project['descricao']}")
    st.markdown(f"[Abrir no GitHub]({project['link']})")

def main():
    st.set_page_config(page_title="Projetos Imersão IA", layout="centered", initial_sidebar_state="expanded", page_icon="🏆")
    
    st.title("🏆 :orange[Top Projetos] - :blue[Imersão IA]")
    st.markdown("Ranking :gray[_(não oficial)_] dos projetos mais votados da Imersão IA :blue[Alura] + **:blue[G]:red[o]:orange[o]:blue[g]:green[l]:red[e]**!")
    st.markdown("⭐ Você retribuir e :orange[curtir] meu [projeto](https://discord.com/channels/1369193715989614684/1369193716434337849/1373142479859355749)!")
    st.markdown("👾 Acesse o código desse :green[open-source] [aqui](https://github.com/matheusaudibert/projeto-aprova).")
    st.info("Os votos são atualizados a cada 5 minutos.")
    
    if "selected_project" not in st.session_state:
        st.session_state.selected_project = None

    projects = load_messages()
    sorted_projects = sorted(projects, key=lambda x: x['votos'], reverse=True)
    
    st.sidebar.error("A votação se encerra às 23:59.")
    
    # Sidebar search
    st.sidebar.title("🔎 Pesquise o seu projeto!")
    search_term = st.sidebar.text_input("Digite o nome seu nome:").lower()
    

    if search_term:
        search_results = [p for p in projects if search_term in p['nome'].lower()]
        if search_results:
            for project in search_results:
                st.sidebar.markdown("---")
                st.sidebar.markdown(f"### {project['nome']}")
                st.sidebar.markdown(f"**Votos:** {project['votos']}")
                st.sidebar.markdown(f"**Usuário Discord:** {project['usuario']}")
                st.sidebar.markdown(f"**Descrição:** {project['descricao']}")
                st.sidebar.markdown(f"[Link do Projeto]({project['link']})")
        else:
            st.sidebar.warning("Nenhum projeto encontrado.")

    cols = st.columns(3)
    for idx, project in enumerate(sorted_projects[:60]):
        col = cols[idx % 3]
        with col:
            st.markdown("""
<style>
.gradient-text {
    background: linear-gradient(
        to right,
        #ff0000,
        #ff1a1a,
        #ff0000,
        #ff1a1a,
        #8c000c,
        #ff3333,
        #940914,
        #75060f,
        #ff0000,
        #ff1a1a
    );
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: rainbow 16s linear infinite;
    background-size: 200% 100%;
    font-weight: bold;
}

@keyframes rainbow {
    0% { background-position: 0% 50%; }
    100% { background-position: -200% 50%; }
}
</style>
""", unsafe_allow_html=True)

            if project['nome'] == "Matheus Audibert":
                st.markdown(
                    f"""
                    <div style='min-height: 4em; margin-bottom: 0.5em'>
                        <h5>{idx + 1}. <span class="gradient-text">{project['nome']}</span></h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            else:
                st.markdown(
                    f"""
                    <div style='min-height: 4em; margin-bottom: 0.5em'>
                        <h5>{idx + 1}. {project['nome']}</h5>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            st.markdown(f"**Votos:** **{project['votos']}**")
            col1, col2 = st.columns(2)
            with col1:
                st.link_button("GitHub", url=project['link'], type="primary", use_container_width=True)
            with col2:
              if st.button("Detalhes", key=f"detalhes_{idx}", use_container_width=True):
                  st.session_state.selected_project = project
                  show_details()  # Chama o dialog aqui com o projeto certo
                  
    st.write("")
    st.write("")
    st.markdown("""
    <div style='text-align: center; font-family: "Segoe UI Emoji", "Apple Color Emoji", "Noto Color Emoji", sans-serif;'>
        Feito com carinho 💙 por <a href="https://github.com/matheusaudibert" target="_blank">Matheus Audibert</a>
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
